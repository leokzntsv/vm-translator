import os
import sys

from CodeWriter import CodeWriter
from Parser import Parser
from VMCommand import VMCommand

if len(sys.argv) > 1:
    path = sys.argv[1]
else:
    print("Usage: python3 VMTranslator.py <folder or some_program.vm>")
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

if os.path.isdir(path):
    files = []
    for f in os.listdir(path):
        file_path = os.path.join(path, f)
        if f.endswith(".vm") and os.path.isfile(file_path):
            files.append(file_path)

    folder_name = os.path.basename(path)
    output_file_name = os.path.join(path, folder_name) + ".asm"
    code_writer = CodeWriter(output_file_name)

    for file_path in files:
        _, file = os.path.split(file_path)
        file_name, _ = os.path.splitext(file)
        code_writer.set_file_name(file_name)

        parser = Parser(file_path)
        translate(parser, code_writer)

    code_writer.close()

elif os.path.isfile(path):
    _, extension = os.path.splitext(path)
    if not extension or extension != ".vm":
        print("File's extension must be of type '.vm'")
        sys.exit(1)
    if not os.path.exists(path):
        print(f"There is no file named {path}")
        sys.exit(1)

    output_file_root, _ = os.path.splitext(path)
    output_file_name = output_file_root + ".asm"
    code_writer = CodeWriter(output_file_name)

    _, file = os.path.split(path)
    file_name, _ = os.path.splitext(file)
    code_writer.set_file_name(file_name)

    parser = Parser(path)
    translate(parser, code_writer)
    code_writer.close()
