import re

def is_valid_cnpj(cnpj):
    cnpj = ''.join(filter(str.isdigit, cnpj))
    return len(cnpj) == 14

def remove_non_digits(input_string):
    if input_string:
        return re.sub(r'\D', '', input_string)
    return input_string

def strip_str_in_list(tup):
    processed_items = []
    for item in tup:
        if isinstance(item, str):
            processed_items.append(item.strip())
        else:
            processed_items.append(item)
    return processed_items


