def get_information(pattern_information, information):
    pattern_keys = [i for i in pattern_information.keys()]
    while '"' in information:
        delta = information[:information.index('"')]
        information = information[(information.index('"') + 1):]
        if delta in pattern_keys:
            information = information[(information.index('"') + 1):]
            pattern_information[delta] = information[:information.index('"')]

    return pattern_information


def all_information(information):
    pattern_information = {'lang': None,
                           'group': None,
                           'name': None,
                           'time': None,
                           'room': None,
                           'place': None,
                           'lesson': None,
                           'type': None,
                           'teacher': None
                           }
    return get_information(pattern_information, information)


def writer(values):
    delta_string = ''
    for key, value in values:
        if value is None or value == '':
            delta_string += ','
        else:
            delta_string += value + ','
    return delta_string


def start(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as json_file:
        with open(output_file, 'w', encoding='utf-8') as csv_file:
            csv_file.write(';'.join(all_information('').keys()) + '\n')
            delta_information = all_information('')
            for current_string in json_file.read().replace('{', '~{').replace('}', '}~').split('~'):
                if current_string.count(':') > 1:
                    for key, value in all_information(current_string + '""').items():
                        if (delta_information[key] is None or str(delta_information[key]) == '')\
                                and (str(value) != '' and value is not None and
                                     str(value) not in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']):
                            delta_information[key] = value
                        elif ((delta_information[key] is not None and str(delta_information[key]) != '')\
                                and (str(value) != '' and value is not None))\
                                or str(value) in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']:
                            answer_string = ''
                            for keys, values in delta_information.items():
                                answer_string += str(values) * (str(values) != 'None' and str(values) != '') + ';'
                            delta_information = all_information('')
                            delta_information[key] = value
                            csv_file.write(answer_string[:-1] + '\n')
            answer_string = ''
            for keys, values in delta_information.items():
                answer_string += str(values) * (str(values) != 'None' and str(values) != '') + ';'
            delta_information = all_information('')
            delta_information[key] = value
            csv_file.write(answer_string[:-1] + '\n')


start('timetable.json', 'to_csv.csv')
