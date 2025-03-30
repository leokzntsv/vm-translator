import os
import sys

from CodeWriter import CodeWriter
from Parser import Parser
from VMCommand import VMCommand

if len(sys.argv) > 1:
    input_path = sys.argv[1]
else:
    print("Usage: python3 VMTranslator.py <folder or some_program.vm>")
    sys.exit(1)

if not os.path.exists(input_path):
    print("Error: given file or directory does not exist")
    sys.exit(1)

def translate(parser: Parser, code_writer: CodeWriter):
    while parser.has_more_commands():
        parser.advance()
        command_type = parser.command_type()
        if command_type == VMCommand.C_PUSH:
            code_writer.write_push(parser.current_command, parser.arg1(), parser.arg2())
        elif command_type == VMCommand.C_POP:
            code_writer.write_pop(parser.current_command, parser.arg1(), parser.arg2())
        elif command_type == VMCommand.C_ARITHMETIC:
            code_writer.write_arithmetic(parser.current_command)
        elif command_type == VMCommand.C_LABEL:
            code_writer.write_label(parser.current_command, parser.arg1())
        elif command_type == VMCommand.C_GOTO:
            code_writer.write_goto(parser.current_command, parser.arg1())
        elif command_type == VMCommand.C_IF:
            code_writer.write_if(parser.current_command, parser.arg1())
        elif command_type == VMCommand.C_FUNCTION:
            code_writer.write_function(parser.current_command, parser.arg1(), parser.arg2())
        elif command_type == VMCommand.C_RETURN:
            code_writer.write_return(parser.current_command)
        elif command_type == VMCommand.C_CALL:
            code_writer.write_call(parser.current_command, parser.arg1(), parser.arg2())

if os.path.isdir(input_path):
    files = []
    for f in os.listdir(input_path):
        file_path = os.path.join(input_path, f)
        if os.path.isfile(file_path) and f.endswith(".vm"):
            files.append(file_path)

    if len(files) == 0:
        print("Error: no .vm files in the given folder")
        sys.exit(1)

    folder_name = os.path.basename(os.path.normpath(input_path))
    output_file_name = os.path.join(input_path, folder_name) + ".asm"
    code_writer = CodeWriter(output_file_name)

    for input_file_path in files:
        _, file = os.path.split(input_file_path)
        file_name, _ = os.path.splitext(file)
        code_writer.set_file_name(file_name)

        parser = Parser(input_file_path)
        translate(parser, code_writer)

    code_writer.close()

elif os.path.isfile(input_path):
    _, extension = os.path.splitext(input_path)
    if not extension or extension != ".vm":
        print("File's extension must be of type '.vm'")
        sys.exit(1)

    output_file_root, _ = os.path.splitext(input_path)
    output_file_name = output_file_root + ".asm"
    code_writer = CodeWriter(output_file_name)

    _, file = os.path.split(input_path)
    file_name, _ = os.path.splitext(file)
    code_writer.set_file_name(file_name)

    parser = Parser(input_path)
    translate(parser, code_writer)
    code_writer.close()
