import re


def parse_bitrix_payload(data: dict) -> dict:
    result = {}

    for key, value in data.items():
        value = value[0]

        match = re.match(r"(\w+)\[(.+)\]", key)

        if not match:
            result[key] = value
            continue

        root, child = match.groups()

        if root not in result:
            result[root] = {}

        result[root][child] = value

    return result