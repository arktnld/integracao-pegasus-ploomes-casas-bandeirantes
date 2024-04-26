from utils.strtools import strip_str_in_list

def extract_contact_info(data):
    """
    Extract contact information from data list.
    """
    data = strip_str_in_list(data)
    nomefantasia, razaosocial, cnpj, cnae, cep, endereco, bairro, estado, cidade, telefone, email, vendedor, promotor, categoria = data
    return {
        "Name": nomefantasia,
        "LegalName": razaosocial,
        "Register": cnpj,
        "StreetAddress": endereco,
        "Neighborhood": bairro,
        "CNAECode": cnae,
        "ZipCode": cep,
        "City": cidade,
        "State": estado,
        "Phone": telefone,
        "Email": email,
        "Vendedor": vendedor,
        "Promotor": promotor,
        "Categoria": categoria
    }

def construct_contact_json(data, city_id):
    """
    Construct JSON data for contact information.
    """
    contact_info = extract_contact_info(data)

    data = {
        **contact_info,
        "CityId": city_id,
        "OtherProperties": [
            {"FieldKey": "contact_138C8A1E-4C1D-455C-9450-915715E47167", "StringValue": contact_info["Name"]},
            {"FieldKey": "contact_01B0A091-4D90-4EDD-9512-8BC134547281", "StringValue": contact_info["Categoria"]},
            {"FieldKey": "contact_AF9E8061-9394-4F39-AF1C-F7EE1FA426FA", "StringValue": contact_info["Vendedor"]},
            {"FieldKey": "contact_E95C1C0D-5612-4823-B4BD-109135462495", "StringValue": contact_info["Promotor"]}
        ],
        "Phones": [
            {
                "PhoneNumber": contact_info["Phone"],
                "TypeId": 1,
                "CountryId": 76
            }
        ]
    }

    return data

