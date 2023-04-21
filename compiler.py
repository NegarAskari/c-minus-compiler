from parser import *
from anytree import Node, RenderTree

input_file = open('input.txt')
parser = Parser(input_file)
input_file.close()

parser.generate_tree()
root = parser.root

for pre, fill, node in RenderTree(root):
    print("%s%s" % (pre, node.name))