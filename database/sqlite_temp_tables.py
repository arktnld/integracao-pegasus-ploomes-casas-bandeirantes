from utils.strtools import remove_non_digits

def create_contacts_temp_table(db, columns, cursor, temp_table_name):
    db.create_table(temp_table_name, columns)

    for row_tuple in cursor:
        row = list(row_tuple)

        row[2] = remove_non_digits(row[2]) # remove non digits from cnpj
        row[4] = remove_non_digits(row[4]) # remove non digits from cep

        cnpj = row[2]
        exists = db.value_exists(temp_table_name, "cnpj", cnpj)

        if not exists:
            row.append(0)
            db.insert_data(temp_table_name, row)
