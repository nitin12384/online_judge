import os
##########################################
# Environment Independent configurations #
##########################################

NUM_SUBMISSION_IN_DIR = 100000

SUBMISSION_DATA_DIR_NAME    = "submissions"
PROBLEM_DATA_DIR_NAME       = "problems"
TEMP_OUTPUT_DATA_DIR_NAME   = "temp_out_data"
TEMP_EXECUTABLE_DIR_NAME    = "temp_executables"
TESTCASES_DIR_NAME          = "testcases"

_BACKSLASH = "\\"
_SLASH = "/"
SPACE = " "


COMPILED_SUCCESSFULLY_MESSAGE = "Compiled Successfully"
EXECUTED_SUCCESSFULLY_MESSAGE = "Executed Successfully"

LINE_LENGTH_LIMIT = 100_000_000_000_000_000

DEFAULT_MEMORY_LIMIT = 500  # MB

COMMAND_LENGTH_LIMIT = 8191

INITIAL_VERDICT_TEXT = "Processing"
INITIAL_VERDICT_TYPE = -1
SECURITY_CHECK_FAILED_VERDICT = "Security check failed for your code"

##########################################
# Environment Dependent configurations   #
##########################################


#DATA_HOME_WINDOWS_1 = r"../data"
DATA_HOME_WINDOWS_1 = r"C:\Users\nitin\Programming\projects\online_judge\data"
DATA_HOME_UBUNTU_1 = r"/home/nitin/Programming/projects/online_judge/data"

CONSOLE_FILE_PRINTER_WIN_1 = "type"
CONSOLE_FILE_PRINTER_UBUNTU_1 = "cat"

CONSOLE_FILE_COPIER_1 = "cp"

CPP_COMPILER_PATH_WIN_1 = r"C:\Users\nitin\MorePrograms\mingw64\bin\g++.exe"
CPP_COMPILER_PATH_UBUNTU_1 = r"/usr/bin/g++"

PYTHON_COMPILER_PATH_WIN_1 = r"C:\Users\nitin\AppData\Local\Programs\Python\Python37\python.exe"
PYTHON_COMPILER_PATH_UBUNTU_1 = r"/usr/bin/python3"

def ubuntu_path_formatter_1(path:str)->str:
    # Todo : make it convert 
    return path

def win_path_formatter_1(path:str)->str:
    assert path != None
    # Todo : Use inbuilt string function for find and replace

    res = ""
    for i in range(0, len(path)):
        if path[i] == '/':
            res += '\\'
        else:
            res += path[i]
    return res


class Config:
    def __init__(self, 
        env_name            ,      
        data_home           ,
        slash               ,
        cpp_compiler_path   ,
        python_compiler_path,
        console_file_printer,
        path_formatter
    ):
        self.env_name               = env_name            
        self.data_home              = data_home           
        self.slash                  = slash
        self.cpp_compiler_path      = cpp_compiler_path   
        self.python_compiler_path   = python_compiler_path
        self.console_file_printer   = console_file_printer
        self.path_formatter         = path_formatter

        self.submission_data_dir_path = self.data_home + self.slash + SUBMISSION_DATA_DIR_NAME
        self.problem_data_dir_path = self.data_home + self.slash + PROBLEM_DATA_DIR_NAME
        self.temp_out_data_dir_path = self.submission_data_dir_path + self.slash + TEMP_OUTPUT_DATA_DIR_NAME
        self.temp_executable_dir_path = self.submission_data_dir_path + self.slash + TEMP_EXECUTABLE_DIR_NAME
        self.testcase_dir_relative_path = self.slash + TESTCASES_DIR_NAME
##########################################
#   Choose Environment                   #
##########################################


ubuntu_1_config = Config("ENV_UBUNTU1", DATA_HOME_UBUNTU_1, _SLASH, 
                         CPP_COMPILER_PATH_UBUNTU_1, PYTHON_COMPILER_PATH_UBUNTU_1, 
                         CONSOLE_FILE_PRINTER_UBUNTU_1, ubuntu_path_formatter_1)
window_1_config = Config("ENV_WINDOWS1", DATA_HOME_WINDOWS_1, _BACKSLASH, 
                         CPP_COMPILER_PATH_WIN_1, PYTHON_COMPILER_PATH_WIN_1, 
                         CONSOLE_FILE_PRINTER_WIN_1, win_path_formatter_1)

# for image with python, django, and gcc installed
dockerised_1_config = Config("DOCKERIZED_1",
"/root/data", # Data Home
_SLASH, # path seperator
"g++", # CPP compiler Path
"python", # Python compiler Path
CONSOLE_FILE_PRINTER_UBUNTU_1,
ubuntu_path_formatter_1
)


# for deployment
render_data_home = os.getcwd() + '/data'
print("os.getcwd() ", os.getcwd())

test_path = render_data_home + "/problems/1/description.txt" 

print("test_path = ", test_path, " exist : ", os.path.exists(test_path))

render_deploy_config = Config("RENDER_DEPLOY",
render_data_home,
_SLASH,
"g++",
"python",
CONSOLE_FILE_PRINTER_UBUNTU_1,
ubuntu_path_formatter_1                              
)

cur_config = ubuntu_1_config

# current config acc to evironment variable

ENVIRONMENT = os.getenv('OS_TYPE')

print("Environemt : ", ENVIRONMENT)

if ENVIRONMENT == 'WINDOWS':
    cur_config = window_1_config
elif ENVIRONMENT == 'UBUNTU_DOCKERIZED':
    cur_config = dockerised_1_config
elif ENVIRONMENT == 'RENDER_DEPLOYED':
    cur_config = render_deploy_config