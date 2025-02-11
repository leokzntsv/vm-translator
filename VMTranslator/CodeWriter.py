class CodeWriter:
    def __init__(self):
        self.comparison_counter = 0
    
    def set_file_name(self, file_name: str):
        self.file_name = file_name

    def write_arithmetic(self, command: str):
        with open(f"{self.file_name}.asm", "a") as f:
            f.write(f"// {command}\n")
            if command == "add":
                # pop from stack
                f.write("@SP\n")
                f.write("AM=M-1\n")
                f.write("D=M\n")
                f.write("@SP\n")
                f.write("AM=M-1\n")
                # add
                f.write("M=D+M\n")
                # move pointer
                f.write("@SP\n")
                f.write("M=M+1\n")
            elif command == "sub":
                # pop from stack
                f.write("@SP\n")
                f.write("AM=M-1\n")
                f.write("D=M\n")
                f.write("@SP\n")
                f.write("AM=M-1\n")
                # sub
                f.write("M=M-D\n")
                # move pointer
                f.write("@SP\n")
                f.write("M=M+1\n")
            elif command == "neg":
                f.write("@SP\n")
                f.write("AM=M-1\n")
                # neg
                f.write("M=-M\n")
                # move pointer
                f.write("@SP\n")
                f.write("M=M+1\n")
            elif command == "eq":
                label_true = f"EQ_TRUE_{self.comparison_counter}"
                label_end = f"EQ_END_{self.comparison_counter}"
                self.comparison_counter += 1
                # pop from stack
                f.write("@SP\n")
                f.write("AM=M-1\n")
                f.write("D=M\n")
                f.write("@SP\n")
                f.write("AM=M-1\n")
                
                # eq
                f.write("D=M-D\n")
                # if == 0 then -1 to the stack else 0 to the stack
                f.write(f"@{label_true}\n")
                f.write("D;JEQ\n")
                f.write("D=0\n")
                f.write(f"@{label_end}\n")
                f.write("0;JMP\n")
                f.write(f"({label_true})\n")
                f.write("D=-1\n")
                f.write(f"({label_end})\n")
                f.write("@SP\n")
                f.write("A=M\n")
                f.write("M=D\n")

                # move pointer
                f.write("@SP\n")
                f.write("M=M+1\n")
            elif command == "gt":
                label_true = f"EQ_TRUE_{self.comparison_counter}"
                label_end = f"EQ_END_{self.comparison_counter}"
                self.comparison_counter += 1
                # pop from stack
                f.write("@SP\n")
                f.write("AM=M-1\n")
                f.write("D=M\n")
                f.write("@SP\n")
                f.write("AM=M-1\n")
                
                # gt
                f.write("D=M-D\n")
                # if > 0 then -1 to the stack else 0 to the stack
                f.write(f"@{label_true}\n")
                f.write("D;JGT\n")
                f.write("D=0\n")
                f.write(f"@{label_end}\n")
                f.write("0;JMP\n")
                f.write(f"({label_true})\n")
                f.write("D=-1\n")
                f.write(f"({label_end})\n")
                f.write("@SP\n")
                f.write("A=M\n")
                f.write("M=D\n")

                # move pointer
                f.write("@SP\n")
                f.write("M=M+1\n")
            elif command == "lt":
                label_true = f"EQ_TRUE_{self.comparison_counter}"
                label_end = f"EQ_END_{self.comparison_counter}"
                self.comparison_counter += 1
                # pop from stack
                f.write("@SP\n")
                f.write("AM=M-1\n")
                f.write("D=M\n")
                f.write("@SP\n")
                f.write("AM=M-1\n")
                
                # lt
                f.write("D=M-D\n")
                # if < 0 then -1 to the stack else 0 to the stack
                f.write(f"@{label_true}\n")
                f.write("D;JLT\n")
                f.write("D=0\n")
                f.write(f"@{label_end}\n")
                f.write("0;JMP\n")
                f.write(f"({label_true})\n")
                f.write("D=-1\n")
                f.write(f"({label_end})\n")
                f.write("@SP\n")
                f.write("A=M\n")
                f.write("M=D\n")

                # move pointer
                f.write("@SP\n")
                f.write("M=M+1\n")
            elif command == "and":
                # pop from stack
                f.write("@SP\n")
                f.write("AM=M-1\n")
                f.write("D=M\n")
                f.write("@SP\n")
                f.write("AM=M-1\n")
                # and
                f.write("M=D&M\n")
                # move pointer
                f.write("@SP\n")
                f.write("M=M+1\n")
            elif command == "or":
                # pop from stack
                f.write("@SP\n")
                f.write("AM=M-1\n")
                f.write("D=M\n")
                f.write("@SP\n")
                f.write("AM=M-1\n")
                # or
                f.write("M=D|M\n")
                # move pointer
                f.write("@SP\n")
                f.write("M=M+1\n")
            elif command == "not":
                # pop from stack
                f.write("@SP\n")
                f.write("AM=M-1\n")
                # not
                f.write("M=!M\n")
                # move pointer
                f.write("@SP\n")
                f.write("M=M+1\n")

    def write_push(self, command: str, segment: str, index: int):
        with open(f"{self.file_name}.asm", "a") as f:
            f.write(f"// {command}\n")
            f.write(f"@{index}\n")
            f.write("D=A\n")
            f.write("@SP\n")
            f.write("A=M\n")
            f.write("M=D\n")
            f.write("@SP\n")
            f.write("M=M+1\n")

    def write_pop(self, command: str, segment: str, index: int):
        pass
    
    def close(self):
        pass
