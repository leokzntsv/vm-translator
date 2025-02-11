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

    def write_pop(self, command: str, segment: str, index: int):
        pass
    
    def close(self):
        pass

    def __translate_push_constant(self, index: int) -> str:
        return f"""
        @{index}
        D=A
        @SP
        A=M
        M=D
        @SP
        M=M+1
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
