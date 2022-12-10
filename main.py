from time import perf_counter


def get_information(pattern_information, information):
    pattern_keys = [i for i in pattern_information.keys()]
    while '"' in information:
        delta = information[:information.index('"')]
        information = information[(information.index('"') + 1):]
        if delta in pattern_keys:
            information = information[(information.index('"') + 1):]
            pattern_information[delta] = information[:information.index('"')]
    return pattern_information


def about_timetable(information):
    pattern_information = {'lang': None,
                           'group': None,
                           'days': None,
                           }
    return get_information(pattern_information, information)


def about_lesson(information):
    pattern_information = {'time': None,
                           'room': None,
                           'place': None,
                           'lesson': None,
                           'type': None,
                           'teacher': None
                           }
    return get_information(pattern_information, information)


def about_days(information):
    pattern_information = {'name': None,
                           'lessons': None
                           }
    return get_information(pattern_information, information)


def get_last_name(current_string):
    delta_last = current_string.split(',')[-1]
    return delta_last[1:(delta_last.index(':') - 1)]


def writer(nesting_level, key, value, flag):
    return ' ' * nesting_level + '- ' * flag + ' ' * (not flag) * nesting_level + key + ": " + value


def start(input_file, output_file):
    nesting_level = -1
    in_array = [[False, 'None'] for size in range(100)]
    with open(input_file, 'r', encoding='utf-8') as json_file:
        with open(output_file, 'w', encoding='utf-8') as yaml_file:
            for current_string in json_file.read().replace('{', '~{').replace('}', '}~').split('~'):
                nesting_level += current_string.count('{')
                if '[' in current_string:
                    in_array[nesting_level] = [True, get_last_name(current_string)]
                if current_string.count(':') == 1:
                    in_array[nesting_level][1] = get_last_name(current_string[1:])
                    current_string = '  ' * (nesting_level - 1) + '- ' * in_array[nesting_level - 1][0] + '  ' * \
                                     (not in_array[nesting_level - 1][0]) * (nesting_level > 0) \
                                     + in_array[nesting_level][1] + ':'
                    yaml_file.write(current_string + '\n')
                if current_string.count(':') > 1:
                    flag = in_array[nesting_level - 1][0]
                    if 'timetable' in in_array[nesting_level - 1][1]:
                        for key, value in about_timetable(current_string + '""').items():
                            yaml_file.write(writer(nesting_level, key, value, flag) + '\n')
                            flag = False
                    elif 'lesson' in in_array[nesting_level - 1][1]:
                        for key, value in about_lesson(current_string).items():
                            yaml_file.write(writer(nesting_level, key, value, flag) + '\n')
                            flag = False
                    elif 'days' in in_array[nesting_level - 1][1]:
                        for key, value in about_days(current_string + '""').items():
                            yaml_file.write(writer(nesting_level, key, value, flag) + '\n')
                            flag = False

                if ']' in current_string:
                    in_array[nesting_level][0] = False

                if '}' in current_string:
                    nesting_level -= 1
                    in_array[nesting_level + 1] = [False, 'None']


all_time = 0
for _ in range(100):
    start_time = perf_counter()
    start('timetable.json', 'timetable.yaml')
    all_time += perf_counter() - start_time
print(all_time)
