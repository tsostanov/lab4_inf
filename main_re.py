import re
import time


start_time = time.perf_counter()
for _ in range(100):
    flag = [None]
    with open('re_timetable.json', 'r', encoding='utf-8') as json_file:
        with open('timetable.yaml', 'w', encoding='utf-8') as yaml_file:
            for current_string in json_file.read().split('\n'):
                current_string_re = current_string
                if re.search(r']', current_string):
                    flag.pop()
                if len(re.findall(r'":', current_string)) >= 1:
                    current_string = re.sub(r'[{}"",\]\[]', '', current_string)
                    if flag[-1] == '' or str(flag[-1]) in current_string:
                        delta_string = ': '.join(re.findall(r'\w+', current_string))
                        delta_string += ':' * (len(re.findall(r':', delta_string)) == 0)
                        yaml_file.write(' ' * (len(current_string[2:].rstrip()) - len(delta_string) - 2 * len(flag))
                                        + '- ' + delta_string + '\n')
                        current_string = re.sub(r'[\s\d]', '', current_string)
                        flag[-1] = current_string[:current_string.index(':')]
                    else:
                        yaml_file.write(current_string[2 + 2 * (len(flag) - 1):].rstrip() + '\n')

                if re.search(r'\[', current_string_re):
                    flag.append('')

print(time.perf_counter() - start_time)
