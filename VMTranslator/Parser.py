from VMCommand import VMCommand


class Parser:
    def __init__(self, file_name):
        self.file_name = file_name
        self.__reset()

    def has_more_commands(self) -> bool:
        current_position = self.position
        has_more_lines = True

        while has_more_lines:
            line = self.__get_line(current_position)
            if not line:
                has_more_lines = False
                break

            current_position += len(line)
            processed_line = self.__process_line(line)

            if processed_line:
                return True

        return False

    def advance(self):
        line = self.__get_next_line()

        if not line:
            return

        self.position += len(line)
        processed_line = self.__process_line(line)

        if processed_line:
            self.current_command = processed_line
        else:
            self.advance()

    def command_type(self) -> VMCommand:
        if self.__is_arithmetic_command(self.current_command):
            return VMCommand.C_ARITHMETIC
        elif self.__is__push_command(self.current_command):
            return VMCommand.C_PUSH
        elif self.__is_pop_command(self.current_command):
            return VMCommand.C_POP
        elif self.__is_label_command(self.current_command):
            return VMCommand.C_LABEL
        elif self.__is_goto_command(self.current_command):
            return VMCommand.C_GOTO
        elif self.__is_if_goto_command(self.current_command):
            return VMCommand.C_IF
        elif self.__is_function_command(self.current_command):
            return VMCommand.C_FUNCTION
        elif self.__is_call_command(self.current_command):
            return VMCommand.C_CALL
        elif self.__is_return_command(self.current_command):
            return VMCommand.C_RETURN

    def arg1(self) -> str:
        if self.command_type() == VMCommand.C_ARITHMETIC:
            return self.current_command
        if self.command_type() == VMCommand.C_RETURN:
            return None
        return self.__get_command_arg1(self.current_command)

    def arg2(self) -> int:
        current_command_type = self.command_type()
        if (current_command_type != VMCommand.C_PUSH and
            current_command_type != VMCommand.C_POP and
            current_command_type != VMCommand.C_FUNCTION and
            current_command_type != VMCommand.C_CALL):
            return None
        return self.__get_command_arg2(self.current_command)

    def __reset(self):
        self.position = 0
        self.current_command = None

    def __get_next_line(self):
        return self.__get_line(self.position)

    def __get_line(self, position):
        with open(self.file_name, "r", encoding="utf-8") as f:
            f.seek(position)
            line = f.readline()
            return line

    def __process_line(self, line):
        line = self.__strip_comment(line)
        line = self.__strip_whitespace(line)
        return line

    def __strip_comment(self, line):
        return line.split("//")[0]

    def __strip_whitespace(self, line):
        return line.strip()

    def __get_command_arg1(self, command: str) -> str:
        return command.split()[1]

    def __get_command_arg2(self, command: str) -> int:
        return int(command.split()[2])

    def __is_arithmetic_command(self, command: str) -> bool:
        if (command == "add" or
            command == "sub" or
            command == "neg" or
            command == "eq" or
            command == "gt" or
            command == "lt" or
            command == "and" or
            command == "or" or
            command == "not"):
            return True
        else:
            return False

    def __is__push_command(self, command: str) -> bool:
        return command[:4] == "push"

    def __is_pop_command(self, command: str) -> bool:
        return command[:3] == "pop"

    def __is_label_command(self, command: str) -> bool:
        return command[:5] == "label"

    def __is_goto_command(self, command: str) -> bool:
        return command[:4] == "goto"

    def __is_if_goto_command(self, command: str) -> bool:
        return command[:7] == "if-goto"

    def __is_function_command(self, command: str) -> bool:
        return command[:8] == "function"

    def __is_call_command(self, command: str) -> bool:
        return command[:4] == "call"

    def __is_return_command(self, command: str) -> bool:
        return command[:6] == "return"
