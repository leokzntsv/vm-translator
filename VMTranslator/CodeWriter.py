class CodeWriter:
    def __init__(self):
        self.comparison_counter = 0
    
    def set_file_name(self, file_name: str):
        self.file_name = file_name

    def write_arithmetic(self, command: str):
        with open(f"{self.file_name}.asm", "a") as f:
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
        with open(f"{self.file_name}.asm", "a") as f:
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
        with open(f"{self.file_name}.asm", "a") as f:
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

    def close(self):
        pass

    def __translate_push_constant(self, value: int) -> str:
        return f"""
        @{value}
        D=A
        @SP
        A=M
        M=D
        @SP
        M=M+1
        """

    def __translate_push_local(self, index: int) -> str:
        return f"""
        @{index}
        D=A
        @LCL
        A=D+M
        D=M
        @SP
        A=M
        M=D
        @SP
        M=M+1
        """

    def __translate_pop_local(self, index: int):
        return f"""
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
        M=D // put value from stack to the final RAM address
        """

    def __translate_push_argument(self, index: int) -> str:
        return f"""
        @{index}
        D=A
        @ARG
        A=D+M
        D=M
        @SP
        A=M
        M=D
        @SP
        M=M+1
        """

    def __translate_pop_argument(self, index: int):
        return f"""
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
        M=D // put value from stack to the final RAM address
        """

    def __translate_push_this(self, index: int) -> str:
        return f"""
        @{index}
        D=A
        @THIS
        A=D+M
        D=M
        @SP
        A=M
        M=D
        @SP
        M=M+1
        """

    def __translate_pop_this(self, index: int):
        return f"""
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
        M=D // put value from stack to the final RAM address
        """

    def __translate_push_that(self, index: int) -> str:
        return f"""
        @{index}
        D=A
        @THAT
        A=D+M
        D=M
        @SP
        A=M
        M=D
        @SP
        M=M+1
        """

    def __translate_pop_that(self, index: int):
        return f"""
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
        M=D // put value from stack to the final RAM address
        """

    def __translate_push_temp(self, index: int) -> str:
        return f"""
        @{index}
        D=A
        @5
        A=D+A
        D=M
        @SP
        A=M
        M=D
        @SP
        M=M+1
        """

    def __translate_pop_temp(self, index: int) -> str:
        return f"""
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
        M=D // put value from stack to the final RAM address
        """

    def __translate_push_pointer(self, index: int) -> str:
        aligned_segment = "THIS" if index == 0 else "THAT"
        return f"""
        @{aligned_segment}
        D=M
        @SP
        A=M
        M=D
        @SP
        M=M+1
        """

    def __translate_pop_pointer(self, index: int) -> str:
        aligned_segment = "THIS" if index == 0 else "THAT"
        return f"""
        @SP
        AM=M-1
        D=M
        @{aligned_segment}
        M=D
        """

    def __translate_push_static(self, index: int) -> str:
        variable_name = f"{self.file_name}.{index}"
        return f"""
        @{variable_name}
        D=M
        @SP
        A=M
        M=D
        @SP
        M=M+1
        """
    
    def __translate_pop_static(self, index: int) -> str:
        variable_name = f"{self.file_name}.{index}"
        return f"""
        @SP
        AM=M-1
        D=M
        @{variable_name}
        M=D
        """

    def __translate_add(self) -> str:
        return """
        @SP
        AM=M-1
        D=M
        @SP
        M=M-1
        A=M
        M=D+M
        @SP
        M=M+1
        """

    def __translate_sub(self) -> str:
        return """
        @SP
        AM=M-1
        D=M
        @SP
        AM=M-1
        M=M-D
        @SP
        M=M+1
        """

    def __translate_neg(self) -> str:
        return """
        @SP
        AM=M-1
        M=-M
        @SP
        M=M+1
        """

    def __translate_eq(self) -> str:
        label_true = f"EQ_TRUE_{self.comparison_counter}"
        label_end = f"EQ_END_{self.comparison_counter}"
        self.comparison_counter += 1
        return f"""
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
        M=M+1
        """

    def __translate_gt(self) -> str:
        label_true = f"EQ_TRUE_{self.comparison_counter}"
        label_end = f"EQ_END_{self.comparison_counter}"
        self.comparison_counter += 1
        return f"""
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
        M=M+1
        """

    def __translate_lt(self) -> str:
        label_true = f"EQ_TRUE_{self.comparison_counter}"
        label_end = f"EQ_END_{self.comparison_counter}"
        self.comparison_counter += 1
        return f"""
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
        M=M+1
        """

    def __translate_and(self) -> str:
        return """
        @SP
        AM=M-1
        D=M
        @SP
        AM=M-1
        M=D&M
        @SP
        M=M+1
        """

    def __translate_or(self) -> str:
        return """
        @SP
        AM=M-1
        D=M
        @SP
        AM=M-1
        M=D|M
        @SP
        M=M+1
        """

    def __translate_not(self) -> str:
        return """
        @SP
        AM=M-1
        M=!M
        @SP
        M=M+1
        """
