import re
import json
from datetime import datetime
from collections import defaultdict

# Validation patterns and types
validation = {
    'bus_id': {'type': int, 're_pattern': r"\d+"},
    'stop_id': {'type': int, 're_pattern': r"\d+"},
    'stop_name': {'type': str, 're_pattern': r"([A-Z][a-z]+\s)+(Road|Avenue|Boulevard|Street)"},
    'next_stop': {'type': int, 're_pattern': r"\d+"},
    'stop_type': {'type': str, 're_pattern': r"[SOF]?"},
    'a_time': {'type': str, 're_pattern': r"[012]\d:[012345]\d"}
}

# Initialize error dictionary, sets and variables
err_dict = dict.fromkeys(validation, 0)
bus_stops = json.loads(input())
bus_lines_s_f = defaultdict(list)
bus_lines_and_names = defaultdict(list)
bus_lines_num_stops = defaultdict(int)
start_stops = set()
finish_stops = set()
on_demand_stops = set()

previous_arrival_time = datetime.strptime('00:00', '%H:%M')
actual_bus_id = None
bus_id_skip = False

# Process each bus stop
for bus_stop in bus_stops:
    stp_name_val = bus_stop.get('stop_name')
    stp_type_val = bus_stop.get('stop_type')
    a_time_val = bus_stop.get('a_time')
    actual_arrival_time = datetime.strptime(a_time_val, '%H:%M')

    # Validation, update and fill dictionaries and sets
    for key, val in bus_stop.items():
        if not isinstance(val, validation[key]['type']) \
        or not re.fullmatch(validation[key]['re_pattern'], str(val)):
            err_dict[key] += 1

        if key == 'bus_id' and re.fullmatch(validation[key]['re_pattern'], str(val)):
            bus_lines_s_f[str(val)].append(stp_type_val)
            bus_lines_and_names[str(val)].append(stp_name_val)
            bus_lines_num_stops[str(val)] += 1

            if actual_bus_id != val:
                actual_bus_id = val
                previous_arrival_time = datetime.strptime('00:00', '%H:%M')
                bus_id_skip = False

            if actual_arrival_time <= previous_arrival_time and not bus_id_skip:
                err_dict['a_time'] += 1
                bus_id_skip = True

            previous_arrival_time = actual_arrival_time

        if key == 'stop_type' and re.fullmatch(validation[key]['re_pattern'], str(val)):
            if str(val) == 'S':
                start_stops.add(stp_name_val)
            if str(val) == 'F':
                finish_stops.add(stp_name_val)
            if str(val) == 'O':
                on_demand_stops.add(stp_name_val)

# Output error summary
print(f"Type and required field validation: {sum(err_dict.values())} errors")
for k, v in err_dict.items():
    print(f"{k}: {v}")

# Output line names and number of stops
print("\nLine names and number of stops:")
for k, v in bus_lines_num_stops.items():
    print(f"bus_id: {k} stops: {v}")

# Check for start and finish stops
for k, v in bus_lines_s_f.items():
    if 'S' not in v or 'F' not in v:
        print(f'There is no start or end stop for the line: {k}')
        break
else:
    stp_name_counts = defaultdict(int)
    for key, vals in bus_lines_and_names.items():
        for val in vals:
            stp_name_counts[val] += 1

    trans_stops = [name for name, count in stp_name_counts.items() if count > 1]
    for stop in on_demand_stops.copy():
        if stop in start_stops or stop in trans_stops or stop in finish_stops:
            on_demand_stops.discard(stop)

    print(f'\nStart stops: {len(start_stops)}', sorted(list(start_stops)))
    print(f'Transfer stops: {len(trans_stops)}', sorted(trans_stops))
    print(f'Finish stops: {len(finish_stops)}', sorted(list(finish_stops)))
    print(f'On demand stops: {len(on_demand_stops)}', sorted(list(on_demand_stops)))
