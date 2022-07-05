

# Todo : test
def file_comparer_exact(file1_path: str, file2_path: str) -> bool:
    # return true or false
    # compare line by line and return
    file1 = open(file1_path, "r")
    file2 = open(file2_path, "r")

    cur_line_num = 1

    # Todo : make sure to have no possibility of trouble because of infinite loop
    while True :
        # Todo : LowPriority : Pass a limit, to make sure we dont read files which are too big.
        # or which have too long lines
        line1 = file1.readline()
        line2 = file2.readline()

        if line1 == "" and line2 == "":
            return True
        elif line1 != line2:
            # difference at line cur_line_num
            return False

        cur_line_num += 1


# Todo
def script_comparer(file1_path: str, file2_path: str, script_path: str) -> bool:
    pass


# Todo
def script_validator(file_path: str, script_path: str) -> bool:
    pass
