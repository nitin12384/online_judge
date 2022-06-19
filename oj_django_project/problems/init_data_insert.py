
from models import Problem,Submission,Language,ProblemLanuageRelation
from logger import Logger

def insert_init_data() :
    # insert sample problem 
    # first problem
    # only if not existing

    if Problem.objects.get(pk=1) is None :
        # insert problem
        new_problem =   Problem(name='Max Matrix Row', data_dir_path='/1', difficulty=600, 
                    num_testcases=2, time_limit=1.0)
        new_problem.save()
        assert new_problem.id == 1 
        Logger.log('New Problem added, id : ' + new_problem.id + ', name : ' + new_problem.name )



insert_init_data()

    
