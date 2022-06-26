from ..models import Problem,Language,ProblemLanguageRelation, Submission 

def get_num_submissions() -> int :
    # to name the file
    return Submission.objects.count()


def get_lanuage_file_extension(langauge_id : int) -> str :
    if langauge_id == 1 :
        return "cpp"
