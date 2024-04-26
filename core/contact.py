from api.contact_json import construct_contact_data_json
from utils.strtools import remove_non_digits, is_valid_cnpj


class ContactCreate:
    def __init__(self, db, ploomes_service):
        self.db = db
        self.ploomes_service = ploomes_service

    def process(self, cursor):
        for row_tuple in cursor:
            if row_tuple:
                row = list(row_tuple)
                self._process_row(row)

    def _process_row(self, row):
        row[2] = remove_non_digits(row[2])  # Cnpj
        row[4] = remove_non_digits(row[4])  # CEP

        cnpj = row[2]
        if is_valid_cnpj(cnpj):
            exists = self.db.value_exists('clientes', 'cnpj', cnpj)
            if not exists:
                self._create_contact(row)

    def _create_contact(self, row):
        city_id = self.ploomes_service.get_city_id_by_name(row[8])
        data = construct_contact_data_json(row, city_id)
        response_data = self.ploomes_service.create_contact(data)
        if response_data['value']:
            ploomes_id = response_data['value'][0]['Id']
            row.append(ploomes_id)
            self.db.insert_data('clientes', row)
            print(response_data)

class ContactUpdater:
    def __init__(self, db, ploomes_service):
        self.db = db
        self.ploomes_service = ploomes_service

    def update_contacts(self, new_data):
        print("Update contacts")
        for row_tuple in new_data:
            if row_tuple:
                self._process_row(row_tuple)

    def _process_row(self, row_tuple):
        row = list(row_tuple)
        ploomes_id = self.db.get_ploomes_id(row[2], "clientes")[0][0]
        city_id = self.ploomes_service.get_city_id_by_name(row[8])
        data = construct_contact_data_json(row, city_id)
        response_data = self.ploomes_service.update_contact(data, ploomes_id)
        if response_data['value']:
            ploomes_id = response_data['value'][0]['Id']
            row.append(ploomes_id)
            self._update_db(row)

    def _update_db(self, row):
        cnpj = row[2]
        self.db.delete_data('clientes', "cnpj", cnpj)
        self.db.insert_data('clientes', row)
        # print(response_data)
