
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

new_submission = Submission(problem = Problem.objects.get(pk=1), source_file_path = 'data1/1.cpp', verdict = 'WA on Test Case 1', runtime = 1, language_id = 1, submission_time =  timezone.now())
new_submission.save()
assert new_submission.id == 1

new_submission = Submission(problem = Problem.objects.get(pk=1), source_file_path = 'data1/2.cpp', verdict = 'Accepted', runtime = 1, language_id = 1, submission_time =  timezone.now())
new_submission.save()
assert new_submission.id == 2





    
