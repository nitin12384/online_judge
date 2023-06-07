
# run these commands in $ python manage.py shell

from problems.models import Problem,Submission,Language,ProblemLanguageRelation
from django.utils import timezone



new_problem =   Problem(name='Max Matrix Row', data_dir_path='/1', difficulty=600, num_testcases=2, time_limit=1.0)
new_problem.save()
assert new_problem.id == 1 

new_problem =   Problem(name='Amazon - Robot With Strings', data_dir_path='/2', difficulty=1300, num_testcases=2, time_limit=1.0)
new_problem.save()
assert new_problem.id == 2 

new_problem =   Problem(name='Naruto\'s Bracket Sequence', data_dir_path='/3', difficulty=1200, num_testcases=1, time_limit=1.0)
new_problem.save()
assert new_problem.id == 3

new_problem =   Problem(name='Childrens Holiday', data_dir_path='/4', difficulty=1500, num_testcases=1, time_limit=1.0)
new_problem.save()
assert new_problem.id == 4




new_language = Language(name='C++ 14')
new_language.save()
assert new_language.id == 1

new_language = Language(name='Python 3.10')
new_language.save()
assert new_language.id == 2




new_plr = ProblemLanguageRelation(problem=Problem.objects.get(pk=1), language_id=1)
new_plr.save()
assert new_plr.id == 1

new_plr = ProblemLanguageRelation(problem=Problem.objects.get(pk=1), language_id=2)
new_plr.save()
assert new_plr.id == 2

new_plr = ProblemLanguageRelation(problem=Problem.objects.get(pk=2), language_id=1)
new_plr.save()
assert new_plr.id == 3

new_plr = ProblemLanguageRelation(problem=Problem.objects.get(pk=2), language_id=2)
new_plr.save()
assert new_plr.id == 4

new_plr = ProblemLanguageRelation(problem=Problem.objects.get(pk=3), language_id=1)
new_plr.save()
assert new_plr.id == 5

new_plr = ProblemLanguageRelation(problem=Problem.objects.get(pk=3), language_id=2)
new_plr.save()
assert new_plr.id == 6

new_plr = ProblemLanguageRelation(problem=Problem.objects.get(pk=4), language_id=1)
new_plr.save()
assert new_plr.id == 7

new_plr = ProblemLanguageRelation(problem=Problem.objects.get(pk=4), language_id=2)
new_plr.save()
assert new_plr.id == 8



new_submission = Submission(problem = Problem.objects.get(pk=1), source_file_path = 'data1/1.cpp', verdict = 'WA on Test Case 1', runtime = 1, language_id = 1, submission_time =  timezone.now())
new_submission.save()
assert new_submission.id == 1

new_submission = Submission(problem = Problem.objects.get(pk=1), source_file_path = 'data1/2.cpp', verdict = 'Accepted', runtime = 1, language_id = 1, submission_time =  timezone.now())
new_submission.save()
assert new_submission.id == 2


# Add the user 
from django.contrib.auth.models import User 
# username, email, password
user1 = User.objects.create_user('dummy', 'dummy@dummy.com', 'dummy')
user1.first_name = 'Dummy'
user1.last_name = 'User'
user1.save()

assert user1.id == 1




## All user who doesnt have a userinfo object, needs one now

from django.contrib.auth.models import User 
from problems.models import UserInfo

for user in User.objects.all():
    if not UserInfo.objects.filter(user=user).exists():
        # no userinfo
        UserInfo.create_userinfo(user)

# All submissions, add in userproblem relation, accepted or tried
from django.contrib.auth.models import User 
from problems.models import UserInfo, UserProblemRelation, Submission

for submission in Submission.objects.all():
    # for AC , type = 0
    if submission.verdict_type == 0:
        UserProblemRelation.add_solved(submission.user, submission.problem)
    else:
        UserProblemRelation.add_attempted(submission.user, submission.problem)




