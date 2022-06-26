from cmath import log
import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import Problem, Submission
from .backend.utils import get_problem_detailed_context
from django.views.decorators.csrf import csrf_exempt
from .backend.utils import Logger

from .backend.core import SubmissionHandler
# Create your views here.

from .backend import DatabaseHandler

def index(request) :

    Logger.log('Index page requested')

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

@csrf_exempt
def submit(request) :
    if request.method != 'POST' :
        return HttpResponse("This endpoint is only for code submission. Use POST request only.")
    
    # request body contain code, and language and problem id
    req_body = request.body

    print(req_body)

    body=json.loads(req_body)
    problem_id = body['problem_id']
    language_id = body['language_id']
    code = body['code']

    Logger.log("Recieved submission for P-" + problem_id + " language_id " + language_id)

    verdict = SubmissionHandler.submit(code, problem_id, language_id)

    verdict_dict = dict({
        'verdict' : verdict
    })

    return JsonResponse(verdict_dict)


    


