import re
import json


validation = {
    'bus_id': {'type': int, 're_pattern': r"\d+"},
    'stop_id': {'type': int, 're_pattern': r"\d+"},
    'stop_name': {'type': str, 're_pattern':
        r"([A-Z][a-z]+\s)+(Road|Avenue|Boulevard|Street)"},
    'next_stop': {'type': int, 're_pattern': r"\d+"},
    'stop_type': {'type': str, 're_pattern': r"[SOF]?"},
    'a_time': {'type': str, 're_pattern': r"[012]\d:[012345]\d"}
}

err_dict = dict.fromkeys(validation, 0)
routes = json.loads(input())

for route in routes:
    for key, val in route.items():
        if not isinstance(val, validation[key]['type']) \
        or re.fullmatch(validation[key]['re_pattern'], str(val)) is None:
            err_dict[key] += 1

print(f"Type and required field validation: {sum(err_dict.values())} errors")
for k, v in err_dict.items():
    print(f"{k}: {v}")