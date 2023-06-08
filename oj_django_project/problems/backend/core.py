# contains SubmissionManger

import math
from datetime import datetime
from .db_handler import get_num_submissions, get_language_file_extension, save_new_submission, update_submission, update_user_problem_relation
from . import configs
from .configs import cur_config
from .code_processor import process

from django.contrib.auth.models import User

class SubmissionHandler:

    @staticmethod
    def submit(code: str, user: User, problem_id: int, language_id: int) -> tuple:
        # save code to file 

        num_sub = get_num_submissions()
        file_name_without_extension = "code_" + str(num_sub+1)
        file_relative_path = SubmissionHandler.get_new_file_relative_path(language_id, num_sub,
                                                                          file_name_without_extension)
        file_full_path = SubmissionHandler.get_new_file_full_path(file_relative_path)
        SubmissionHandler.save_to_file(code, file_full_path)

        # now to insert into Submission Database
        submission_id = save_new_submission(
            user, problem_id, file_relative_path,
            language_id,  datetime.now()
        )

        # -- LanguageProcessor
        # preprocess
        # validate
        # compile and run with input
        # match output
        # get verdict
        verdict, verdict_type, verdict_details, runtime = process(file_full_path, language_id, submission_id,
                                   problem_id, file_name_without_extension)

        runtime_msec = int(runtime * 1000) # convert to msec
        # save to submission database
        update_submission(submission_id, verdict=verdict, verdict_type=verdict_type, 
                          runtime=runtime_msec)
        
        # User problem relation databse
        update_user_problem_relation(user, problem_id, verdict_type)

        return verdict, verdict_type, verdict_details

    # completed

    # completed
    @staticmethod
    def save_to_file(code: str, file_full_path: str):
        out_file = open(file_full_path, "w")
        out_file.write(code)

    # completed
    @staticmethod
    def get_new_file_full_path(file_relative_path: str) -> str:
        return configs.cur_config.submission_data_dir_path + file_relative_path

    # completed
    @staticmethod
    def get_new_file_relative_path(language_id: int, num_sub: int,
                                   file_name_without_extension: str) -> str:
        # what should be the path of new file
        # relative path 
        file_extension = get_language_file_extension(language_id)
        data_dir = SubmissionHandler.get_next_sub_data_dir(num_sub)

        file_name = file_name_without_extension + "." + file_extension
        file_path = cur_config.slash + data_dir + cur_config.slash + file_name
        return file_path

    def get_next_sub_data_dir(num_sub: int) -> str:
        # 100000 submission in one dir

        old_dir_num = math.ceil(num_sub / configs.NUM_SUBMISSION_IN_DIR)
        num_sub_in_dir = num_sub % configs.NUM_SUBMISSION_IN_DIR
        
        # Todo : Properly implement this
        # return 'data1' for now

        return "data1"
