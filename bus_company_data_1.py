import json


json_convert = json.loads(input())

bus_id = 0
stop_id = 0
stop_name = 0
next_stop = 0
stop_type = 0
a_time = 0

for line in json_convert:
    if not line['bus_id'] or not isinstance(line['bus_id'], int):
        bus_id += 1
    if not line['stop_id'] or not isinstance(line['stop_id'], int):
        stop_id += 1
    if not isinstance(line['next_stop'], int):
        next_stop += 1
    if not line['stop_name'] or not isinstance(line['stop_name'], str):
        stop_name += 1
    if (line['stop_name'] and not isinstance(line['stop_type'], str)
            or len(line['stop_type']) > 1):
        stop_type += 1
    if not line['a_time'] or not isinstance(line['a_time'], str):
        a_time += 1

total_errors = bus_id + stop_id + stop_name + next_stop + stop_type + a_time

print(f'Type and field validation: {total_errors} errors')
print('bus_id:', bus_id)
print('stop_id:', stop_id)
print('next_stop:', next_stop)
print('stop_name:', stop_name)
print('stop_type:', stop_type)
print('a_time:', a_time)