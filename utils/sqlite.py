import sqlite3

class SQLiteManager:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_table(self, table_name, columns):
        columns_str = ', '.join(columns)
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_str})")
        self.conn.commit()

    def remove_table(self, table_name):
        self.cursor.execute(f"DROP TABLE {table_name}")
        self.conn.commit()

    def insert_data(self, table_name, data):
        placeholders = ', '.join(['?' for _ in range(len(data))])
        self.cursor.execute(f"INSERT INTO {table_name} VALUES ({placeholders})", data)
        self.conn.commit()

    def delete_data(self, table_name, column_name, value):
        query = f"DELETE FROM {table_name} WHERE {column_name} = ?"
        self.cursor.execute(query, (value,))
        self.conn.commit()

    def fetch_data(self, table_name, columns="*", condition=None):
        if condition:
            self.cursor.execute(f"SELECT {columns} FROM {table_name} WHERE {condition}")
        else:
            self.cursor.execute(f"SELECT {columns} FROM {table_name}")
        return self.cursor.fetchall()

    def value_exists(self, table_name, column_name, value):
        self.cursor.execute(f"SELECT COUNT(*) FROM {table_name} WHERE {column_name}=?", (value,))
        count = self.cursor.fetchone()[0]
        return count > 0

    def compare_data(self, table_name, temp_table_name, key, columns="*"):

        table_values = self.fetch_data(temp_table_name, key)

        different_records = []
        for value in table_values:
            temp_table_records = self.fetch_data(temp_table_name, columns, f"WHERE {key}={value}")
            table_records = self.fetch_data(table_name, columns, f"WHERE {key}={value}")

            if temp_table_records:
                for temp_table_record, table_record in zip(temp_table_records, table_records):
                    if temp_table_record != table_record:
                        different_records.append(temp_table_record)

        return different_records

    def close_connection(self):
        self.conn.close()

# Assuming you have already defined the SQLiteDB, TableManager, and DataManipulator classes as shown in the refactored code

# Initialize the SQLite database connection
# db = SQLiteDB("example.db")

# # Initialize TableManager and DataManipulator instances
# table_manager = TableManager(db)
# data_manipulator = DataManipulator(db)

# # Create a table
# table_name = "example_table"
# columns = ["id INTEGER PRIMARY KEY", "name TEXT", "age INTEGER"]
# table_manager.create_table(table_name, columns)

# # Insert data into the table
# data = (1, "John", 30)
# table_manager.insert_data(table_name, data)

# # Fetch data from the table
# fetched_data = table_manager.fetch_data(table_name)
# print("Fetched data:", fetched_data)

# # Create a temporary table and manipulate data
# temp_table_name = "temp_example_table"
# cursor = [(1, "Alice", 25), (2, "Bob", 35)]
# temp_columns = ["id INTEGER PRIMARY KEY", "name TEXT", "age INTEGER"]
# data_manipulator.create_temp_table(temp_columns, cursor, temp_table_name)

# # Compare data between tables
# different_records = data_manipulator.compare_data(table_name, temp_table_name)
# print("Different records:", different_records)

# # Remove a table
# table_manager.remove_table(table_name)

# # Close the database connection
# db.close_connection()
