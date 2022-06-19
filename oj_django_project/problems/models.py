from django.db import models

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
verdict : string 
runtime : int, (in msec)
language_id : int 
submission_time : timestamp

"""
class Submission(models.Model) :
    problem_id = models.ForeignKey(Problem, on_delete=models.CASCADE)
    source_file_path = models.CharField(max_length=200)
    verdict = models.CharField(max_length=20)
    runtime = models.IntegerField()
    language_id = models.IntegerField()
    submission_time = models.DateTimeField()

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

class ProblemLanuageRelation(models.Model) :
    problem_id = models.ForeignKey(Problem, on_delete=models.CASCADE)
    language_id = models.IntegerField()


    
