import pytest
from django.db import connection
from django.core.management import call_command

@pytest.fixture(scope='session')
def setup_db():
    """Fixture for resetting database and clearing sequences"""
    # Proveď reset databáze před testy
    call_command('flush', '--no-input')
    
    # Resetování sekvencí pro generování nových ID
    with connection.cursor() as cursor:
        cursor.execute('SELECT setval(pg_get_serial_sequence(\'core_project\', \'id\'), max(id)) FROM core_project')
        cursor.execute('SELECT setval(pg_get_serial_sequence(\'core_task\', \'id\'), max(id)) FROM core_task')
        # Přidejte pro další tabulky podle potřeby

    yield
    # Můžete přidat cleanup po testech, pokud to bude potřeba
