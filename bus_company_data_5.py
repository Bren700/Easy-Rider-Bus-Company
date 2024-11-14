import re
import json
from datetime import datetime


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
b_lines_num_stops = {}
b_lines_s_f = {}
b_lines_names = {}
start_stops = set()
finish_stops = set()

previous_arrival_time = zero = datetime.strptime('00:00', '%H:%M')
current_bus_id = None
bus_id_skip = False

for bus_stop in bus_stops:
    stp_name = bus_stop.get('stop_name')
    sf_type = bus_stop.get('stop_type')
    time_val = bus_stop.get('a_time')
    current_arrival_time = datetime.strptime(time_val, '%H:%M')

    for key, val in bus_stop.items():
        if not isinstance(val, validation[key]['type']) \
        or not re.fullmatch(validation[key]['re_pattern'], str(val)):
            err_dict[key] += 1

        if key == 'bus_id' \
        and re.fullmatch(validation[key]['re_pattern'], str(val)):
            if str(val) not in b_lines_s_f:
                b_lines_s_f[str(val)] = [sf_type]
            else:
                b_lines_s_f[str(val)].append(sf_type)
            if str(val) not in b_lines_names:
                b_lines_names[str(val)] = [stp_name]
            else:
                b_lines_names[str(val)].append(stp_name)
            if str(val) not in b_lines_num_stops:
                b_lines_num_stops[str(val)] = 1
            else:
                b_lines_num_stops[str(val)] += 1

            if current_bus_id != val:
                current_bus_id = val
                previous_arrival_time = zero
                bus_id_skip = False

            if current_arrival_time <= previous_arrival_time and not bus_id_skip:
                err_dict['a_time'] += 1
                bus_id_skip = True

            previous_arrival_time = current_arrival_time

        if key == 'stop_type' \
                and re.fullmatch(validation[key]['re_pattern'], str(val)):
            if str(val) == 'S':
                start_stops.add(bus_stop.get('stop_name'))
            if str(val) == 'F':
                finish_stops.add(bus_stop.get('stop_name'))

print(f"Type and required field validation: {sum(err_dict.values())} errors")
for k, v in err_dict.items():
    print(f"{k}: {v}")

print("\nLine names and number of stops:")
for k, v in b_lines_num_stops.items():
    print(f"bus_id: {k} stops: {v}")

for k, v in b_lines_s_f.items():
    if 'S' and 'F' not in v:
        print(f'There is no start or end stop for the line: {k}')
        break
    else:
        stp_name_counts = {}
        for key, vals in b_lines_names.items():
            for val in vals:
                if val in stp_name_counts:
                    stp_name_counts[val] += 1
                else:
                    stp_name_counts[val] = 1

        trans_stops = [name for name, count in stp_name_counts.items() if count > 1]
        print(f'\nStart stops: {len(start_stops)}', sorted(list(start_stops)))
        print(f'Transfer stops: {len(trans_stops)}', sorted(trans_stops))
        print(f'Finish stops: {len(finish_stops)}', sorted(list(finish_stops)))
        break