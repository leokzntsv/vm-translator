import os
import sys

from CodeWriter import CodeWriter
from Parser import Parser
from VMCommand import VMCommand

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
code_writer = CodeWriter()
code_writer.set_file_name(file_name)

while parser.has_more_commands():
    parser.advance()
    command_type = parser.command_type()
    if command_type == VMCommand.C_PUSH:
        code_writer.write_push(parser.current_command, parser.arg1(), parser.arg2())
    elif command_type == VMCommand.C_POP:
        code_writer.write_pop(parser.current_command, parser.arg1(), parser.arg2())
    elif command_type == VMCommand.C_ARITHMETIC:
        code_writer.write_arithmetic(parser.current_command)
