import os


def get_name(line):
    return line[line.find('"') + 1:line.rfind('"')]


def get_includes(file_name, standard_includes, file_order):
    with open(file_name, 'r') as file:
        for line in file:
            if line.startswith('#include'):
                if '<' in line:
                    standard_includes.add(line)
                else:
                    my_include = get_name(line)
                    if my_include not in file_order:
                        get_includes(my_include, standard_includes, file_order)

    file_order.append(file_name)

    if file_name.endswith('.h'):
        cpp_file = '{}.cpp'.format(file_name[:-2])
        if os.path.isfile(cpp_file):
            get_includes(cpp_file, standard_includes, file_order)


def copy_without_includes(file_name, target_file):
    target_file.write('// {}\n\n'.format(file_name))

    with open(file_name, 'r') as source:
        for line in source:
            if not line.startswith(('#include', '#pragma once')):
                target_file.write(line)

        target_file.write('\n\n')


def joiner():
    standard_includes = set()
    file_order = list()

    get_includes('main.cpp', standard_includes, file_order)

    with open('autoJoinedMain.cpp', 'w') as joined_file:
        for line in standard_includes:
            joined_file.write(line)
        joined_file.write('\n')

        for file_name in file_order:
            copy_without_includes(file_name, joined_file)


if __name__ == '__main__':
    joiner()
