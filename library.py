import yaml
import json
import time

start_time = time.perf_counter()
for _ in range(100):
    with open('timetable.json', 'r', encoding='utf-8') as input_file:
        with open('timetable.yaml', 'w', encoding='utf-8') as output_file:
            parsed = str(yaml.dump(json.load(input_file), sort_keys=False)).replace('"', '')
            parsed = parsed.replace('          ', '')
            output_file.write(parsed.encode().decode('unicode-escape'))

print(time.perf_counter() - start_time)
