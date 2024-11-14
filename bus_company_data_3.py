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
bus_stops = json.loads(input())
lines_and_stops = {}
for bus_stop in bus_stops:
    for key, val in bus_stop.items():
        if not isinstance(val, validation[key]['type']) \
        or not re.fullmatch(validation[key]['re_pattern'], str(val)):
            err_dict[key] += 1
        if key == 'bus_id' \
        and re.fullmatch(validation[key]['re_pattern'], str(val)):
                if str(val) not in lines_and_stops:
                    lines_and_stops[str(val)] = 1
                else:
                    lines_and_stops[str(val)] += 1


print(f"Type and required field validation: {sum(err_dict.values())} errors")
for k, v in err_dict.items():
    print(f"{k}: {v}")
print("\nLine names and number of stops:")
for k, v in lines_and_stops.items():
    print(f"bus_id: {k} stops: {v}")