# Todo : Needs lot of cleanup, etc to make it easy to use

NUM_SUBMISSION_IN_DIR = 100000


#DATA_HOME_WINDOWS_1 = r"../data"
DATA_HOME_WINDOWS_1 = r"C:/Users/nitin/Programming/projects/online_judge/data"
DATA_HOME_UBUNTU_1 = r"/home/nitin/Programming/projects/online_judge/data"

SUBMISSION_DATA_RELATIVE_PATH = r"/submissions"
PROBLEM_DATA_RELATIVE_PATH = r"/problems"
TEMP_OUTPUT_DATA_RELATIVE_PATH = r"/temp_out_data"
TEMP_EXECUTABLE_DIR_RELATIVE_PATH = r"/temp_executables"
TESTCASES_DIR_RELATIVE_PATH = r"/testcases"

BACKSLASH = "\\"
SLASH = "/"
SPACE = " "

ENVIRONMENT = "WINDOWS_1"
ENV_WINDOWS1 = "WINDOWS_1"
ENV_UBUNTU1 = "UBUNTU_1"
COMPILED_SUCCESSFULLY_MESSAGE = "Compiled Successfully"
EXECUTED_SUCCESSFULLY_MESSAGE = "Executed Successfully"

LINE_LENGTH_LIMIT = 100_000_000_000_000_000

DEFAULT_MEMORY_LIMIT = 500  # MB

COMMAND_LENGTH_LIMIT = 8191

INITIAL_VERDICT_TEXT = "Processing"
INITIAL_VERDICT_TYPE = -1
SECURITY_CHECK_FAILED_VERDICT = "Security check failed for your code"

CONSOLE_FILE_PRINTER_WIN_1 = "type"
CONSOLE_FILE_PRINTER_UBUNTU_1 = "cat"

CONSOLE_FILE_COPIER_1 = "cp"

CPP_COMPILER_PATH_1 = r"C:\Users\nitin\MorePrograms\mingw64\bin\g++.exe"
CPP_COMPILER_PATH_2 = r"/usr/bin/g++"

PYTHON_COMPILER_PATH_1 = r"C:\Users\nitin\AppData\Local\Programs\Python\Python37\python.exe"
PYTHON_COMPILER_PATH_2 = r"/usr/bin/python3"

class Config:
    def __init__(self, 
        env_name            ,      
        data_home           ,
        cpp_compiler_path   ,
        python_compiler_path,
        console_file_printer
    ):
        self.env_name             = env_name            
        self.data_home            = data_home           
        self.cpp_compiler_path    = cpp_compiler_path   
        self.python_compiler_path = python_compiler_path
        self.console_file_printer = console_file_printer

        self.submission_data_dir_path = self.data_home + SUBMISSION_DATA_RELATIVE_PATH
        self.problem_data_dir_path = self.data_home + PROBLEM_DATA_RELATIVE_PATH
        self.temp_out_data_dir_path = self.submission_data_dir_path + TEMP_OUTPUT_DATA_RELATIVE_PATH
        self.temp_executable_dir_path = self.submission_data_dir_path + TEMP_EXECUTABLE_DIR_RELATIVE_PATH


ubuntu_1_config = Config(ENV_UBUNTU1, DATA_HOME_UBUNTU_1, CPP_COMPILER_PATH_2, PYTHON_COMPILER_PATH_2, CONSOLE_FILE_PRINTER_UBUNTU_1)
window_1_config = Config(ENV_WINDOWS1, DATA_HOME_WINDOWS_1, CPP_COMPILER_PATH_1, PYTHON_COMPILER_PATH_1, CONSOLE_FILE_PRINTER_WIN_1)

cur_config = None 

if ENVIRONMENT == ENV_UBUNTU1 :
    cur_config = ubuntu_1_config
elif ENVIRONMENT == ENV_WINDOWS1 :
    cur_config = window_1_config
