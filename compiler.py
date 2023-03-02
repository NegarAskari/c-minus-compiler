from scanner import *

input_file = open('input.txt')
scanner = Scanner(input_file)
input_file.close()

current_token = scanner.get_next_token()
line = 1
tokens_string = ''
with open('tokens.txt', 'w') as tokens_file:
    while(current_token != 0):
        if scanner.lineno != line:
            if tokens_string != '':
                tokens_file.write(f"{line}.\t{tokens_string}\n")
            tokens_string = ''
            line = scanner.lineno
        tokens_string += f"({current_token[0]}, {current_token[1]}) "
        current_token = scanner.get_next_token()
    if tokens_string != '':
        tokens_file.write(f"{line}.\t{tokens_string}\n")

errors = scanner.lexical_errors.errors_list
errors_string = ''
with open('lexical_errors.txt', 'w') as errors_file:
    if len(errors) == 0:
        errors_file.write('There is no lexical error.')
    else:
        line = errors[0][0]
        for error in errors:
            if error[0] != line:
                errors_file.write(f"{line}.\t{errors_string}\n")
                errors_string = ''
                line = error[0]
            errors_string += f"({error[1]}, {error[2]}) "
        errors_file.write(f"{line}.\t{errors_string}\n")


symbol_table = scanner.symbol_table.dict
index = 0
with open("symbol_table.txt", "w") as symbols_file:
    for key in symbol_table:
        index += 1
        symbols_file.write(f"{index}.\t{key}\n")