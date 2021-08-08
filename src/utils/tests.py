from datetime import datetime


def process_dict(dict_: dict) -> dict:
    output_dict = {}
    for key, value in dict_.items():
        if isinstance(value, datetime):
            value = str(value)
        output_dict[key] = value

    return output_dict
