from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import Problem, Submission
from .utility import get_problem_detailed_context
 

# Create your views here.

def index(request) :
    context = {
        'problem_list' : Problem.objects.all()
    }

    return render(request, 'problems/index.html', context)

def detail(request, problem_id) :    
    problem = get_object_or_404(Problem, pk=problem_id)
    context = get_problem_detailed_context(problem)

    return render(request, 'problems/detail.html', context)

def submissions_detail(request, problem_id) :
    # all submission with that problem id 
    problem = get_object_or_404(Problem, pk=problem_id)
    context = {'problem' : problem}

    return render(request, 'problems/submissions_detail.html', context)

def submit_page(request, problem_id) :
    
    problem = get_object_or_404(Problem, pk=problem_id)
    
    #TODO : later replace it with only required things
    context = get_problem_detailed_context(problem)
    return render(request, 'problems/submit.html', context)

def get_verdict(request, submission_id) :
    submission:Submission = get_object_or_404(Submission, pk=submission_id)
    verdict_dict = dict({
        'verdict' : submission.verdict
    })

    return JsonResponse(verdict_dict)    

def submit(request) :
    # request body contain code, and language and problem id
    if request.method == 'POST' :
        pass
    else :
        return HttpResponse("This endpoint is only for code submission");
