import textwrap


class CodeWriter:
    def __init__(self, output_file_name: str):
        self.comparison_counter = 0
        self.output_file_name = output_file_name
        self.file_name = ""
        self.current_function_name = ""

    def set_file_name(self, file_name: str):
        self.current_file_name = file_name

    def write_init(self):
        with open(f"{self.output_file_name}", "a") as f:
            f.write(self.__initialization_code())
            f.write("\n")

    def write_arithmetic(self, command: str):
        with open(f"{self.output_file_name}", "a") as f:
            f.write(f"// {command}\n")
            if command == "add":
                f.write(self.__translate_add())
                f.write("\n")
            elif command == "sub":
                f.write(self.__translate_sub())
                f.write("\n")
            elif command == "neg":
                f.write(self.__translate_neg())
                f.write("\n")
            elif command == "eq":
                f.write(self.__translate_eq())
                f.write("\n")
            elif command == "gt":
                f.write(self.__translate_gt())
                f.write("\n")
            elif command == "lt":
                f.write(self.__translate_lt())
                f.write("\n")
            elif command == "and":
                f.write(self.__translate_and())
                f.write("\n")
            elif command == "or":
                f.write(self.__translate_or())
                f.write("\n")
            elif command == "not":
                f.write(self.__translate_not())
                f.write("\n")

    def write_push(self, command: str, segment: str, index: int):
        with open(f"{self.output_file_name}", "a") as f:
            f.write(f"// {command}\n")
            if segment == "constant":
                f.write(self.__translate_push_constant(index))
                f.write("\n")
            elif segment == "local":
                f.write(self.__translate_push_local(index))
                f.write("\n")
            elif segment == "argument":
                f.write(self.__translate_push_argument(index))
                f.write("\n")
            elif segment == "this":
                f.write(self.__translate_push_this(index))
                f.write("\n")
            elif segment == "that":
                f.write(self.__translate_push_that(index))
                f.write("\n")
            elif segment == "temp":
                f.write(self.__translate_push_temp(index))
                f.write("\n")
            elif segment == "pointer":
                f.write(self.__translate_push_pointer(index))
                f.write("\n")
            elif segment == "static":
                f.write(self.__translate_push_static(index))
                f.write("\n")

    def write_pop(self, command: str, segment: str, index: int):
        with open(f"{self.output_file_name}", "a") as f:
            f.write(f"// {command}\n")
            if segment == "local":
                f.write(self.__translate_pop_local(index))
                f.write("\n")
            elif segment == "argument":
                f.write(self.__translate_pop_argument(index))
                f.write("\n")
            elif segment == "this":
                f.write(self.__translate_pop_this(index))
                f.write("\n")
            elif segment == "that":
                f.write(self.__translate_pop_that(index))
                f.write("\n")
            elif segment == "temp":
                f.write(self.__translate_pop_temp(index))
                f.write("\n")
            elif segment == "pointer":
                f.write(self.__translate_pop_pointer(index))
                f.write("\n")
            elif segment == "static":
                f.write(self.__translate_pop_static(index))
                f.write("\n")

    def write_label(self, command: str, label: str):
        full_label = self.current_function_name + f"${label}"
        with open(f"{self.output_file_name}", "a") as f:
            f.write(f"// {command}\n")
            f.write(self.__translate_label(full_label))
            f.write("\n")

    def write_goto(self, command: str, label: str):
        full_label = self.current_function_name + f"${label}"
        with open(f"{self.output_file_name}", "a") as f:
            f.write(f"// {command}\n")
            f.write(self.__translate_goto(full_label))
            f.write("\n")

    def write_if(self, command: str, label: str):
        full_label = self.current_function_name + f"${label}"
        with open(f"{self.output_file_name}", "a") as f:
            f.write(f"// {command}\n")
            f.write(self.__translate_if(full_label))
            f.write("\n")

    def write_function(self, command: str, function_name: str, num_locals: int):
        self.current_function_name = function_name
        with open(f"{self.output_file_name}", "a") as f:
            f.write(f"// {command}\n")
            f.write(self.__translate_function(function_name, num_locals))
            f.write("\n")

    def write_return(self, command: str):
        with open(f"{self.output_file_name}", "a") as f:
            f.write(f"// {command}\n")
            f.write(self.__translate_return())
            f.write("\n")

    def close(self):
        pass

    def __initialization_code(self) -> str:
        return textwrap.dedent(
            f"""\
                @256
                D=A
                @SP
                M=D
                @Sys.init
                0;JMP\
            """
        )

    def __translate_push_constant(self, value: int) -> str:
        return textwrap.dedent(f"""\
            @{value}
            D=A
            @SP
            A=M
            M=D
            @SP
            M=M+1\
        """)

    def __translate_push_local(self, index: int) -> str:
        return textwrap.dedent(f"""\
            @{index}
            D=A
            @LCL
            A=D+M
            D=M
            @SP
            A=M
            M=D
            @SP
            M=M+1\
        """)

    def __translate_pop_local(self, index: int):
        return textwrap.dedent(f"""\
            @{index}
            D=A
            @LCL
            D=D+M // final RAM address
            @R13
            M=D // save final RAM address to R13
            @SP
            AM=M-1
            D=M // retrieve value to pop from stack
            @R13
            A=M
            M=D // put value from stack to the final RAM address\
        """)

    def __translate_push_argument(self, index: int) -> str:
        return textwrap.dedent(f"""\
            @{index}
            D=A
            @ARG
            A=D+M
            D=M
            @SP
            A=M
            M=D
            @SP
            M=M+1\
        """)

    def __translate_pop_argument(self, index: int):
        return textwrap.dedent(f"""\
            @{index}
            D=A
            @ARG
            D=D+M // final RAM address
            @R13
            M=D // save final RAM address to R13
            @SP
            AM=M-1
            D=M // retrieve value to pop from stack
            @R13
            A=M
            M=D // put value from stack to the final RAM address\
        """)

    def __translate_push_this(self, index: int) -> str:
        return textwrap.dedent(f"""\
            @{index}
            D=A
            @THIS
            A=D+M
            D=M
            @SP
            A=M
            M=D
            @SP
            M=M+1\
        """)

    def __translate_pop_this(self, index: int):
        return textwrap.dedent(f"""\
            @{index}
            D=A
            @THIS
            D=D+M // final RAM address
            @R13
            M=D // save final RAM address to R13
            @SP
            AM=M-1
            D=M // retrieve value to pop from stack
            @R13
            A=M
            M=D // put value from stack to the final RAM address\
        """)

    def __translate_push_that(self, index: int) -> str:
        return textwrap.dedent(f"""\
            @{index}
            D=A
            @THAT
            A=D+M
            D=M
            @SP
            A=M
            M=D
            @SP
            M=M+1\
        """)

    def __translate_pop_that(self, index: int):
        return textwrap.dedent(f"""\
            @{index}
            D=A
            @THAT
            D=D+M // final RAM address
            @R13
            M=D // save final RAM address to R13
            @SP
            AM=M-1
            D=M // retrieve value to pop from stack
            @R13
            A=M
            M=D // put value from stack to the final RAM address\
        """)

    def __translate_push_temp(self, index: int) -> str:
        return textwrap.dedent(f"""\
            @{index}
            D=A
            @5
            A=D+A
            D=M
            @SP
            A=M
            M=D
            @SP
            M=M+1\
        """)

    def __translate_pop_temp(self, index: int) -> str:
        return textwrap.dedent(f"""\
            @{index}
            D=A
            @5
            D=D+A // final RAM address
            @R13
            M=D // save final RAM address to R13
            @SP
            AM=M-1
            D=M // retrieve value to pop from stack
            @R13
            A=M
            M=D // put value from stack to the final RAM address\
        """)

    def __translate_push_pointer(self, index: int) -> str:
        aligned_segment = "THIS" if index == 0 else "THAT"
        return textwrap.dedent(f"""\
            @{aligned_segment}
            D=M
            @SP
            A=M
            M=D
            @SP
            M=M+1\
        """)

    def __translate_pop_pointer(self, index: int) -> str:
        aligned_segment = "THIS" if index == 0 else "THAT"
        return textwrap.dedent(f"""\
            @SP
            AM=M-1
            D=M
            @{aligned_segment}
            M=D\
        """)

    def __translate_push_static(self, index: int) -> str:
        variable_name = f"{self.current_file_name}.{index}"
        return textwrap.dedent(f"""\
            @{variable_name}
            D=M
            @SP
            A=M
            M=D
            @SP
            M=M+1\
        """)
    
    def __translate_pop_static(self, index: int) -> str:
        variable_name = f"{self.current_file_name}.{index}"
        return textwrap.dedent(f"""\
            @SP
            AM=M-1
            D=M
            @{variable_name}
            M=D\
        """)

    def __translate_add(self) -> str:
        return textwrap.dedent("""\
            @SP
            AM=M-1
            D=M
            @SP
            M=M-1
            A=M
            M=D+M
            @SP
            M=M+1\
        """)

    def __translate_sub(self) -> str:
        return textwrap.dedent("""\
            @SP
            AM=M-1
            D=M
            @SP
            AM=M-1
            M=M-D
            @SP
            M=M+1\
        """)

    def __translate_neg(self) -> str:
        return textwrap.dedent("""\
            @SP
            AM=M-1
            M=-M
            @SP
            M=M+1\
        """)

    def __translate_eq(self) -> str:
        label_true = f"EQ_TRUE_{self.comparison_counter}"
        label_end = f"EQ_END_{self.comparison_counter}"
        self.comparison_counter += 1
        return textwrap.dedent(f"""\
            @SP
            AM=M-1
            D=M
            @SP
            AM=M-1
            D=M-D
            @{label_true}
            D;JEQ
            D=0
            @{label_end}
            0;JMP
            ({label_true})
            D=-1
            ({label_end})
            @SP
            A=M
            M=D
            @SP
            M=M+1\
        """)

    def __translate_gt(self) -> str:
        label_true = f"EQ_TRUE_{self.comparison_counter}"
        label_end = f"EQ_END_{self.comparison_counter}"
        self.comparison_counter += 1
        return textwrap.dedent(f"""\
            @SP
            AM=M-1
            D=M
            @SP
            AM=M-1
            D=M-D
            @{label_true}
            D;JGT
            D=0
            @{label_end}
            0;JMP
            ({label_true})
            D=-1
            ({label_end})
            @SP
            A=M
            M=D
            @SP
            M=M+1\
        """)

    def __translate_lt(self) -> str:
        label_true = f"EQ_TRUE_{self.comparison_counter}"
        label_end = f"EQ_END_{self.comparison_counter}"
        self.comparison_counter += 1
        return textwrap.dedent(f"""\
            @SP
            AM=M-1
            D=M
            @SP
            AM=M-1
            D=M-D
            @{label_true}
            D;JLT
            D=0
            @{label_end}
            0;JMP
            ({label_true})
            D=-1
            ({label_end})
            @SP
            A=M
            M=D
            @SP
            M=M+1\
        """)

    def __translate_and(self) -> str:
        return textwrap.dedent("""\
            @SP
            AM=M-1
            D=M
            @SP
            AM=M-1
            M=D&M
            @SP
            M=M+1\
        """)

    def __translate_or(self) -> str:
        return textwrap.dedent("""\
            @SP
            AM=M-1
            D=M
            @SP
            AM=M-1
            M=D|M
            @SP
            M=M+1\
        """)

    def __translate_not(self) -> str:
        return textwrap.dedent("""\
            @SP
            AM=M-1
            M=!M
            @SP
            M=M+1\
        """)

    def __translate_label(self, label: str) -> str:
        return textwrap.dedent(
            f"""\
                ({label})\
            """
        )

    def __translate_goto(self, label: str) -> str:
        return textwrap.dedent(
            f"""\
                @{label}
                0;JMP\
            """
        )

    def __translate_if(self, label: str) -> str:
        return textwrap.dedent(
            f"""\
                @SP
                AM=M-1
                D=M
                @{label}
                D;JNE\
            """
        )

    def __translate_function(self, function_name: str, num_locals: int) -> str:
        loop_start_label = f"{function_name}$PUSH_LOCALS_LOOP_START"
        loop_end_label = f"{function_name}$PUSH_LOCALS_LOOP_END"
        return textwrap.dedent(
            f"""\
                ({function_name})
                @{num_locals}
                D=A
                @{loop_end_label}
                D;JEQ
                @R13 // Save `number of local variables`
                M=D
                ({loop_start_label}) // Push 0 to the stack `number of local variables` times
                @0
                D=A
                @SP
                A=M
                M=D
                @SP
                M=M+1
                @R13
                M=M-1
                D=M
                @{loop_start_label}
                D;JGT
                ({loop_end_label})\
            """
        )

    def __translate_return(self) -> str:
        return textwrap.dedent(
            f"""\
                @LCL // endFrame = LCL
                D=M
                @endFrame
                M=D
                @5 // retAddr = *(endFrame - 5)
                A=D-A
                D=M
                @retAddr
                M=D
                @SP // *ARG = pop()
                AM=M-1
                D=M
                @ARG
                A=M
                M=D
                @ARG // SP = ARG + 1
                D=M
                @SP
                M=D+1
                @endFrame // THAT = *(endFrame - 1)
                A=M-1
                D=M
                @THAT
                M=D
                @2 // THIS = *(endFrame - 2)
                D=A
                @endFrame
                A=M-D
                D=M
                @THIS
                M=D
                @3 // ARG = *(endFrame - 3)
                D=A
                @endFrame
                A=M-D
                D=M
                @ARG
                M=D
                @4 // LCL = *(endFrame - 4)
                D=A
                @endFrame
                A=M-D
                D=M
                @LCL
                M=D
                @retAddr
                0;JMP\
            """
        )
