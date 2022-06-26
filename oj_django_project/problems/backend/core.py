
# contains SubmissionManger

from ast import Sub
import math
from .DatabaseHandler import get_num_submissions, get_lanuage_file_extension
from . import configs

class SubmissionHandler:
    def submit(code : str, problem_id : int, language_id : int) -> str :
        # save code to file 
        SubmissionHandler.save_to_file(code, language_id)

        verdict = "Implementing"
        return verdict

    def save_to_file(code : str, language_id : int) -> str :
        file_path = SubmissionHandler.get_new_file_path(language_id)
        # return file name
        return ""


    def get_new_file_path(language_id : int) -> str :
        # what should be the path of new file
        # relative path 
        num_sub = get_num_submissions()
        file_extension = get_lanuage_file_extension(language_id)
        return ""



    def confirm_data_dir(num_sub : int) -> str :
        # 100000 submission in one dir

        old_dir_num = math.ceil( num_sub / configs.NUM_SUBMISSION_IN_DIR )
        num_sub_in_dir = num_sub % configs.NUM_SUBMISSION_IN_DIR

        return ""



