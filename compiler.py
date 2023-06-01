from parserr import Parser

input_file = open('input.txt')
parser = Parser(input_file)
input_file.close()

parser.generate_tree()
root = parser.root

errors = parser.semantic_check.errors

with open('output.txt', 'w') as output_file:
    if len(errors) == 0:
        for i, cmd in enumerate(parser.code_gen.pb):
            if len(cmd) > 0:
                output_file.write(str(i) + "\t" + cmd + '\n')
    else:
        output_file.write("The output code has not been generated.")


with open("semantic_errors.txt", 'w') as error_file:
    if len(errors) == 0:
        error_file.write("The input program is semantically correct.")
    else:
        for error in errors:
            error_file.write(error + "\n")

