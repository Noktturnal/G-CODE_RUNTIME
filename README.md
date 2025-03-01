# G-CODE Runtime Analysis Application

## Overview

The **G-CODE Runtime Analysis Application** is a Django-based web application designed to analyze G-code files, estimate machining time, and provide insights into tool usage. This project was developed as part of my final Python Developer course at **Coders Lab**.

### Project Motivation

In my previous job, I programmed CNC machines, many of which were very old and lacked modern software support. This inspired me to create a tool that can assist in **cost estimation and production planning** by analyzing G-code files and calculating runtime based on speeds and feeds.

## Features

- **User Authentication**: Users can sign up, log in, and manage their profiles.
- **G-code Upload**: Users can upload G-code files for analysis.
- **Machining Time Estimation**: The application calculates the estimated runtime based on the provided G-code.
- **Tool Usage Analysis**: Provides detailed information on which tools are used and for how long.
- **Project and Task Management**: Users can create projects, assign tasks, and track progress.
- **Data Persistence**: Users can save their analyzed results for future reference.

## Project Structure

```
G_CODE_RUNTIME/       # Main project directory
├── core/             # Core functionality (models, views, forms, templates)
├── runtime_algorithm/ # G-code parsing and analysis logic
├── users/            # User authentication and profile management
├── templates/        # HTML templates for the web interface
├── static/           # Static files (CSS, JavaScript, images)
├── tests/            # Unit tests for application functionality
├── manage.py         # Django's management script
└── requirements.txt  # Required dependencies
```

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/g-code-runtime-analysis.git
    cd g-code-runtime-analysis
    ```

2. **Create a virtual environment and activate it**:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Configure the database**:
    - Ensure **MySQL** is installed and running.
    - Update database settings in `settings.py` with your MySQL credentials.
    - Run database migrations:
    ```sh
    python manage.py migrate
    ```

5. **Create a superuser**:
    ```sh
    python manage.py createsuperuser
    ```

6. **Run the development server**:
    ```sh
    python manage.py runserver
    ```

7. **Access the application**:
    Open your browser and go to `http://127.0.0.1:8000`.

## Running Tests

To run tests, use:
```sh
pytest
```

## Contributing

Contributions are welcome! Feel free to fork the repository and submit a pull request with your improvements.

## License

This project is licensed under the **MIT License**. See the `LICENSE` file for more details.

## Acknowledgements

- **Django** – The web framework used.
- **PyMySQL** – MySQL database driver.

## Contact

For questions or suggestions, open an issue or contact me on GitHub.

