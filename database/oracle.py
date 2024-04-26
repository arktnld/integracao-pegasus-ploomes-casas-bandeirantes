import cx_Oracle

class DatabaseConnector:
    def __init__(self, host, port, service_name, user, password):
        cx_Oracle.init_oracle_client(lib_dir='C:\\Users\\Admin\\Documents\\ploomes\\clientes\\drivers')
        dsn = cx_Oracle.makedsn(host, port, service_name)
        self.connection = cx_Oracle.connect(
            user=user,
            password=password,
            dsn=dsn
        )

    def close(self):
        if self.connection:
            self.connection.close()

    def execute_query(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        return cursor

# class DataProcessor:
#     @staticmethod
#     def process_row(row):
#         # Process the row here
#         # You can add more processing logic as needed
#         return {
#             "nomefantasia": row[0],
#             "razaosocial": row[1],
#             "cnpj": row[2],
#             "cnae": row[3],
#             "cep": row[4],
#             "endereco": row[5],
#             "bairro": row[6],
#             "estado": row[7],
#             "cidade": row[8],
#             "telefone": row[9],
#             "email": row[10],
#             "vendedor": row[11],
#             "promotor": row[12],
#             "classificacaopessoa": row[13]
#         }

# class DataPrinter:
#     @staticmethod
#     def print_data(data):
#         for key, value in data.items():
#             print(f"{key}: {value}")

