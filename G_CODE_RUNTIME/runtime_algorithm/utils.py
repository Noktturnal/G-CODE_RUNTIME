import re
import os
import math
import sys

# Configurable parameters for the machine
MACHINE_TYPE = 'lathe'  # Options: 'mill' or 'lathe'
MAX_G0_SPEED = 5000  # Maximum speed for G0 (rapid positioning) in mm/min
MAX_G1_SPEED = 3000  # Maximum speed for G1 (cutting) in mm/min

# Set default feed mode based on machine type
DEFAULT_FEED_MODE = 'G98' if MACHINE_TYPE == 'mill' else 'G99'

def parse_gcode(file_path):
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file.readlines() if line.strip()]
    except Exception as e:
        print(f"Error reading file: {str(e)}")
        return []

def calculate_feedspeed(distance, feed_rate, spindle_speed, feed_mode, css_active=False, css_speed=0, diameter=0):
    try:
        if feed_mode == 'G98':  # Feed per minute
            return distance / (feed_rate / 60)  # Convert to seconds
        elif feed_mode == 'G99':  # Feed per revolution
            if css_active and diameter > 0:
                # For constant surface speed, calculate actual spindle speed based on diameter
                actual_spindle_speed = (css_speed * 1000) / (math.pi * diameter)
                if actual_spindle_speed > 0:
                    return distance / (feed_rate * actual_spindle_speed / 60)
            elif spindle_speed > 0:
                return distance / (feed_rate * spindle_speed / 60)
            
            print(f'Warning: Using feed per revolution with:'
                  f'\n  CSS active: {css_active}'
                  f'\n  CSS speed: {css_speed}'
                  f'\n  Diameter: {diameter}'
                  f'\n  Spindle speed: {spindle_speed}')
            return 0
    except Exception as e:
        print(f'Error in calculate_feedspeed: {str(e)}')
        return 0

def calculate_distance(x1, y1, z1, c1, x2, y2, z2, c2):
    try:
        # Calculate linear distance
        linear_distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)
        
        # Calculate C axis movement (rotary)
        if c1 is not None and c2 is not None:
            avg_diameter = abs(x1 + x2) / 2  # Average diameter
            c_distance = abs(c2 - c1) * math.pi * avg_diameter / 360  # Arc length
            return linear_distance + c_distance
        
        return linear_distance
    except Exception as e:
        print(f'Error in calculate_distance: {str(e)}')
        return 0

def analyze_gcode(lines):
    current_position = {'X': 0, 'Y': 0, 'Z': 0, 'C': 0}
    total_time = 0
    g0_time = 0
    g1_time = 0
    tool_times = {}
    current_tool = None
    spindle_speed = 0
    feed_mode = DEFAULT_FEED_MODE
    feed_rate = None
    css_active = False
    css_speed = 0

    print("\n=== Starting G-code Analysis ===")
    print(f"Initial settings:")
    print(f"Feed mode: {feed_mode}")
    print(f"Machine type: {MACHINE_TYPE}\n")

    g76_params = {}

    for line_number, line in enumerate(lines, 1):
        try:
            line = line.strip()
            if not line or line.startswith('(') or line.startswith('O') or line.startswith('%'):
                continue

            print(f"\nProcessing line {line_number}: {line}")
            time = 0

            # Feed mode - now explicitly set and maintained
            if 'G98' in line:
                feed_mode = 'G98'
                print(f"Feed mode changed to: {feed_mode} (feed per minute)")
            elif 'G99' in line:
                feed_mode = 'G99'
                print(f"Feed mode changed to: {feed_mode} (feed per revolution)")

            # CSS control
            if 'G96' in line:
                css_active = True
                css_match = re.search(r'S(\d+)', line)
                if css_match:
                    css_speed = float(css_match.group(1))
                print(f"CSS activated with speed: {css_speed}")
            elif 'G97' in line:
                css_active = False
                print("CSS deactivated")

            # Kontrola parametru F v řádku
            f_match = re.search(r'F([-+]?\d*\.?\d+)', line)
            if f_match:
                feed_rate = float(f_match.group(1))
                print(f"Feed rate found in line: {feed_rate}")

            # G0 or G1 movement
            if re.search(r'G0|G1', line):
                command = 'G0' if 'G0' in line else 'G1'
                
                # Extract X, Y, Z, C parameters
                params = {}
                for axis in ['X', 'Y', 'Z', 'C']:
                    match = re.search(rf'{axis}([-+]?\d*\.?\d+)', line)
                    if match:
                        params[axis] = float(match.group(1))

                new_position = current_position.copy()
                for axis in ['X', 'Y', 'Z', 'C']:
                    if axis in params:
                        new_position[axis] = params[axis]

                distance = calculate_distance(
                    current_position['X'], current_position['Y'], current_position['Z'], current_position['C'],
                    new_position['X'], new_position['Y'], new_position['Z'], new_position['C']
                )

                if command == 'G0':
                    time = distance / (MAX_G0_SPEED / 60)
                elif command == 'G1':
                    if feed_rate is None:
                        print(f"Warning: No feed rate specified for G1 movement in line {line_number}")
                        continue
                    current_diameter = abs(current_position['X'] * 2)
                    time = calculate_feedspeed(distance, feed_rate, spindle_speed, feed_mode, 
                                            css_active, css_speed, current_diameter)

                print(f"Movement details:")
                print(f"  Command: {command}")
                print(f"  Parameters: {params}")
                print(f"  From position: {current_position}")
                print(f"  To position: {new_position}")
                print(f"  Distance: {distance:.4f} mm")
                print(f"  Current feed rate: {feed_rate if feed_rate is not None else 'Not specified'}")
                print(f"  Feed mode: {feed_mode}")
                print(f"  CSS active: {css_active}")
                if css_active:
                    print(f"  CSS speed: {css_speed}")
                print(f"  Spindle speed: {spindle_speed}")
                print(f"  Calculated time: {time:.4f} seconds")

                if command == 'G0':
                    g0_time += time
                    if current_tool:
                        tool_times[current_tool]['G0'] += time
                elif command == 'G1':
                    g1_time += time
                    if current_tool:
                        tool_times[current_tool]['G1'] += time

                total_time += time
                if current_tool:
                    tool_times[current_tool]['total'] += time

                current_position = new_position

            # Tool change
            elif re.match(r'^T\d+', line):
                current_tool = re.match(r'^T\d+', line).group(0)
                if current_tool not in tool_times:
                    tool_times[current_tool] = {'G0': 0, 'G1': 0, 'total': 0}
                print(f"Tool change: {current_tool}")

            # Spindle speed (when not in CSS mode)
            elif re.search(r'S\d+', line) and not css_active and not 'G96' in line:
                speed_match = re.search(r'S(\d+)', line)
                if speed_match:
                    spindle_speed = int(speed_match.group(1))
                    print(f"Spindle speed set to: {spindle_speed} RPM")

            # G76 threading cycle
            elif re.search(r'G76', line):
                if 'P' in line and 'Q' in line and 'R' in line:
                    # First G76 line
                    p_match = re.search(r'P(\d+)', line)
                    q_match = re.search(r'Q(\d+)', line)
                    r_match = re.search(r'R([-+]?\d*\.?\d+)', line)
                    if p_match and q_match and r_match:
                        g76_params['P'] = int(p_match.group(1))
                        g76_params['Q'] = int(q_match.group(1)) / 1000  # Convert microns to mm
                        g76_params['R'] = float(r_match.group(1))
                        print(f"G76 first line parameters: P={g76_params['P']}, Q={g76_params['Q']}, R={g76_params['R']}")
                elif 'X' in line and 'Z' in line and 'P' in line and 'Q' in line and 'R' in line and 'F' in line:
                    # Second G76 line
                    x_match = re.search(r'X([-+]?\d*\.?\d+)', line)
                    z_match = re.search(r'Z([-+]?\d*\.?\d+)', line)
                    p_match = re.search(r'P(\d+)', line)
                    q_match = re.search(r'Q(\d+)', line)
                    r_match = re.search(r'R([-+]?\d*\.?\d+)', line)
                    f_match = re.search(r'F([-+]?\d*\.?\d+)', line)
                    if x_match and z_match and p_match and q_match and r_match and f_match:
                        x_value = float(x_match.group(1))
                        z_value = float(z_match.group(1))
                        p_value = int(p_match.group(1)) / 1000  # Convert microns to mm
                        q_value = int(q_match.group(1)) / 1000  # Convert microns to mm
                        r_value = float(r_match.group(1))
                        f_value = float(f_match.group(1))
                        print(f"G76 second line parameters: X={x_value}, Z={z_value}, P={p_value}, Q={q_value}, R={r_value}, F={f_value}")

                        # Calculate threading time
                        threading_length = abs(z_value - current_position['Z'])
                        threading_passes = int(g76_params['P'] / g76_params['Q'])
                        threading_time = threading_length / (f_value * spindle_speed / 60) * threading_passes
                        total_time += threading_time
                        g1_time += threading_time  # Add threading time to G1 time
                        if current_tool:
                            tool_times[current_tool]['G1'] += threading_time  # Add threading time to tool's G1 time
                            tool_times[current_tool]['total'] += threading_time
                        print(f"Threading time: {threading_time:.4f} seconds")

        except Exception as e:
            print(f"Error processing line {line_number}: {str(e)}")
            continue

    return total_time, g0_time, g1_time, tool_times

def main(file_path):
    print(f"Analyzing G-code file: {file_path}")
    print(f"Machine type: {MACHINE_TYPE}, Default feed mode: {DEFAULT_FEED_MODE}")
    
    try:
        lines = parse_gcode(file_path)
        if not lines:
            print("Error: No lines read from file")
            return
            
        total_time, g0_time, g1_time, tool_times = analyze_gcode(lines)

        print("\n            ===== RESULTS =====")
        print(f"Total runtime: {total_time:.4f} seconds ({total_time/60:.2f} minutes)")
        print(f"G0 time: {g0_time:.4f} seconds ({g0_time/60:.2f} minutes)")
        print(f"G1 time: {g1_time:.4f} seconds ({g1_time/60:.2f} minutes)")
        
        print("\n           ===== TOOL TIMES =====")
        for tool, times in tool_times.items():
            print(f"Tool {tool}:")
            print(f"  G0 time: {times['G0']:.4f} seconds ({times['G0']/60:.2f} minutes)")
            print(f"  G1 time: {times['G1']:.4f} seconds ({times['G1']/60:.2f} minutes)")
            print(f"  Total time: {times['total']:.4f} seconds ({times['total']/60:.2f} minutes)")
    
    except Exception as e:
        print(f"Error during execution: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python utils.py <file_path>")
    else:
        file_path = sys.argv[1]
        main(file_path)