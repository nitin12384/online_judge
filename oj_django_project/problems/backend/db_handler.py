from re import sub
from ..models import Problem, Language, ProblemLanguageRelation, Submission, UserProblemRelation
from django.contrib.auth.models import User

from datetime import datetime
from . import configs



def get_problem(problem_id: int) -> Problem:
    return Problem.objects.get(pk=problem_id)

def get_submission(submission_id: int) -> Submission:
    return Submission.objects.get(pk=submission_id)

def get_num_submissions() -> int:
    # to name the file
    return Submission.objects.count()


def get_language_file_extension(langauge_id: int) -> str:
    if langauge_id == 1:
        return "cpp"
    elif langauge_id == 2:
        return "py"
    else:
        return "unknown"


def save_new_submission(user: User, problem_id: int, source_file_path: str,
                        language_id: int, submission_time: datetime) -> int:
    problem = Problem.objects.get(pk=problem_id)

    # it should exist .
    assert problem is not None
    assert user is not None

    verdict = configs.INITIAL_VERDICT_TEXT
    verdict_type = configs.INITIAL_VERDICT_TYPE
    runtime = 0

    submission = Submission(user=user, problem=problem, source_file_path=source_file_path,
                            verdict=verdict, verdict_type=verdict_type, 
                            runtime=runtime, language_id=language_id,
                            submission_time=submission_time)
    submission.save()
    return submission.id


def update_submission(submission_id: int, verdict: int, verdict_type: int, runtime: int):
    submission = Submission.objects.get(pk=submission_id)
    submission.verdict = verdict
    submission.verdict_type = verdict_type
    submission.runtime = runtime
    submission.save()

def update_user_problem_relation(user: User, problem_id: int, verdict_type: int):
    if verdict_type == 0:
        UserProblemRelation.add_solved(user, Problem.objects.get(pk=problem_id))
    else :
        UserProblemRelation.add_attempted(user, Problem.objects.get(pk=problem_id))
    pass