import os
import sys

from Parser import Parser

if len(sys.argv) > 1:
    full_file_name = sys.argv[1]
else:
    print("Usage: python3 VMTranslator.py <some_program.vm>")
    sys.exit(1)

file_name, extension = os.path.splitext(full_file_name)

if not extension or extension != ".vm":
    print("File's extension must be of type '.vm'")
    sys.exit(1)

if not os.path.exists(full_file_name):
    print(f"There is no file named {full_file_name}")
    sys.exit(1)

parser = Parser(full_file_name)
while parser.has_more_commands():
    parser.advance()
    print(parser.command_type())
    print(parser.arg1())
    print(parser.arg2())
