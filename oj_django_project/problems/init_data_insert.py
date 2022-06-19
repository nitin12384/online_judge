
from .models import Problem,Submission,Language,ProblemLanuageRelation

def insert_init_data() :
    # insert sample problem 
    # first problem
    new_problem =   Problem(name='Max Matrix Row', data_dir_path='/1', difficulty=600, 
                    num_testcases=2, time_limit=1.0)
