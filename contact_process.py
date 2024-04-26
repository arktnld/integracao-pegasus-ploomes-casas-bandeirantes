from monit.core import Monitor as monit
from monit.error import SetupError, DataCreateError, DataUpdateError

from api.ploomes import PloomesAPI
from utils.sqlite import SQLiteManager
from database.oracle import DatabaseConnector
from database.queries import contacts_query
from database.sqlite_temp_tables import create_contacts_temp_table
import utils.config as config
from core.contact import ContactCreate, ContactUpdater


def inital_setup():
    try:
        print("Initial setup")

        # Setup SQLite database
        db = SQLiteManager('ploomes.db')
        db.create_table('clientes', config.columns)

        # Setup Oracle database connection
        oracle = DatabaseConnector(
            host=config.host,
            port=config.port,
            service_name=config.service_name,
            user=config.user,
            password=config.password
        )

        # Setup PloomesAPI
        ploomes_api = PloomesAPI()

        return db, oracle, ploomes_api

    except Exception as e:
        monit.notify_and_exit(SetupError, e)


def create_new_contacts(db, ploomes_api, cursor):
    try:
        print("Create new contacts")

        # Logic to create new contacts on Ploomes #
        contact_creator = ContactCreate(db, ploomes_api)
        contact_creator.process(cursor)

    except Exception as e:
        monit.notify_and_exit(DataCreateError, e)


def update_existing_contacts(db, ploomes_api, cursor):
    try:
        print("Update existing contacts")

        # Logic to update existing contacts on Ploomes #
        create_contacts_temp_table(db, config.select_columns, cursor, 'temp_clientes')
        new_data = db.compare_data('clientes', 'temp_clientes', "cnpj", config.select_columns)
        updater = ContactUpdater(db, ploomes_api)
        updater.update_contacts(new_data)

    except Exception as e:
        monit.notify_and_exit(DataUpdateError, e)


def main():
    db, oracle, ploomes_api = inital_setup()

    # Execute query to fetch contacts from Oracle
    cursor = oracle.execute_query(contacts_query)

    create_new_contacts(db, ploomes_api, cursor)
    update_existing_contacts(db, ploomes_api, cursor)

    oracle.close()

if __name__ == "__main__":
    main()
