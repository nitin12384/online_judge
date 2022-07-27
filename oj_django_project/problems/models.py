from django.db import models
from django.contrib.auth.models import User

from .backend.utils import Logger

# Create your models here.

# Todo : Add Proper contraints

"""
Fields 
id (default) ,
name,
data_dir_path,
difficulty,
num_testcases,
time_limit
"""
class Problem(models.Model) :
    name = models.CharField(max_length=200)
    data_dir_path = models.CharField(max_length=200)
    difficulty = models.IntegerField()
    num_testcases = models.IntegerField()
    time_limit = models.FloatField(default=1)

"""
id : int, primary key
problem_id : int foreign key
source_file_path : string
verdict : string,
verdict_type : 0 -> AC, 1 -> WA, 2 -> RE, 3 -> TLE, 4 -> MLE, 5 -> CE
verdict_type : -1 -> Not Logged In  (this is just for submit buttton, never saved in database)
runtime : int, (in msec)
language_id : int 
submission_time : timestamp

"""
class Submission(models.Model) :
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    source_file_path = models.CharField(max_length=200)
    verdict = models.CharField(max_length=50) # Time Limit Exceeded on Test Case 1000 (37 chars)
    verdict_type = models.IntegerField()
    runtime = models.IntegerField()
    language_id = models.IntegerField()
    submission_time = models.DateTimeField()


"""
user,

first name and last name are redundant here
might going to be removed

first_name, 
last_name,
num_problems_solved : integer 
score : integer,
"""
class UserInfo(models.Model) :
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    num_problems_solved = models.IntegerField()
    score = models.IntegerField()

    def get_full_name(self) -> str :
        return self.first_name + " " + self.last_name
    
    # Make sure it works
    def function1(self):
        pass

    def add_num_problems_solved(self):
        self.num_problems_solved += 1
        self.save()


    # return id 
    # return -1 if there was error
    @staticmethod
    def create_userinfo(user, first_name:str='', last_name:str='', num_problems_solved:int=0, score:int=0) :
        userinfo_obj = UserInfo(
            user                = user                ,
            first_name          = first_name          ,
            last_name           = last_name           ,
            num_problems_solved = num_problems_solved ,
            score               = score               ,
        )
        userinfo_obj.save()
    
    def get_num_problems_solved(user)->int:
        return UserInfo.objects.get(user=user).num_problems_solved 
    
    # Todo : make user public, private info fucntions here
    def get_user_public_info(user):
        pass

"""
status : 1 -> attempted, 2 -> solved 
"""
class UserProblemRelation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    status = models.IntegerField()

    @staticmethod
    def add_attempted(user, problem):
        # check if already attempted, or solved
        Logger.log("add_attempted() for user = " + str(user) + "problem = " + str(problem))
        qset = UserProblemRelation.objects.filter(user=user).filter(problem=problem)

        if qset.exists() : 
            Logger.log("Already Attempted")
            # Todo May remvoe this.
            assert qset[0].status == 1 or qset[0].status == 2
            # do nothing
            pass
        else :
            Logger.log("Adding as Attempted")
            upr_obj = UserProblemRelation(user=user, problem=problem, status=1)
            upr_obj.save()

    @staticmethod
    def add_solved(user, problem):
        Logger.log("add_solved() for user = " + str(user) + "problem = " + str(problem))
        
        try:
            upr_obj = UserProblemRelation.objects.get(user=user, problem=problem)
            # query set's save doesnt works
            # qset[0].save()

            if upr_obj.status == 1:
                Logger.log("Already Attempted. Adding as Solved")
                upr_obj.status = 2
                upr_obj.save()
                # add num_solved in userinfo
                UserInfo.objects.get(user=user).add_num_problems_solved()
            else:
                Logger.log("Already Solved")

        except UserProblemRelation.DoesNotExist :
            Logger.log("Adding as Solved")
            upr_obj = UserProblemRelation(user=user, problem=problem, status=2)
            upr_obj.save()
            # add num_solved in userinfo
            UserInfo.objects.get(user=user).add_num_problems_solved()
            #upr_obj.user.num_problems_solved += 1
            #upr_obj.user.save()


"""
id,
name
"""
class Language(models.Model) :
    name = models.CharField(max_length=30)

"""
problem_id,
language_id
"""

class ProblemLanguageRelation(models.Model) :
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    language_id = models.IntegerField()


    
