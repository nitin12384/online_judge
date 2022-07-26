from django.db import models
from django.contrib.auth.models import User

# Create your models here.

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
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    source_file_path = models.CharField(max_length=200)
    verdict = models.CharField(max_length=50) # Time Limit Exceeded on Test Case 1000 (37 chars)
    verdict_type = models.IntegerField()
    runtime = models.IntegerField()
    language_id = models.IntegerField()
    submission_time = models.DateTimeField()


"""
user,
first_name, 
last_name,
num_problems_solved : integer 
score : integer,
"""
class UserInfo(models.Model) :
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    num_problems_solved = models.IntegerField()
    score = models.IntegerField()

    def get_full_name(self) -> str :
        return self.first_name + " " + self.last_name

    # return id 
    # return -1 if there was error
    def create_userinfo(user, first_name:str, last_name:str, num_problems_solved:int=0, score:int=0) -> int :

        try:
            userinfo_obj = UserInfo(
                user                = user                ,
                first_name          = first_name          ,
                last_name           = last_name           ,
                num_problems_solved = num_problems_solved ,
                score               = score               ,
            )
            userinfo_obj.save()
            return userinfo_obj.id
        except :
            raise "UserInfo Creation Exception"
            #return -1

"""
status : 1 -> attempted, 2 -> solved 
"""
class UserProblemRelation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    status = models.IntegerField()

    

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


    
