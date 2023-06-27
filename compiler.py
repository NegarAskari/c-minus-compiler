from parserr import Parser
from anytree import RenderTree

input_file = open('input.txt')
parser = Parser(input_file)
input_file.close()

parser.generate_tree()
root = parser.root

with open('output.txt', 'w') as output_file:
    for i, cmd in enumerate(parser.code_gen.pb):
        if len(cmd) > 0:
            output_file.write(str(i) + "\t" + cmd + '\n')
