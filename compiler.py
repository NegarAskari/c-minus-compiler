from parserr import Parser
from anytree import RenderTree

input_file = open('input.txt')
parser = Parser(input_file)
input_file.close()

parser.generate_tree()
root = parser.root

with open('parse_tree.txt', 'w',  encoding="utf-8") as output_file:
    for pre, fill, node in RenderTree(root):
        output_file.write("%s%s\n" % (pre, node.name))


with open('syntax_errors.txt', 'w') as errors_file:
    if len(parser.errors) == 0:
        errors_file.write("There is no syntax error.")
    else:
        for error in parser.errors:
            errors_file.write(error + "\n")