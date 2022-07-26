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

from .backend import db_handler


def index(request):
    Logger.log('Index page requested')

    context = {
        'problem_list': Problem.objects.all()
    }

    return render(request, 'problems/index.html', context)


def detail_submit(request, problem_id):
    problem = get_object_or_404(Problem, pk=problem_id)
    context = get_problem_detailed_context(problem)

    return render(request, 'problems/detail_submit.html', context)


def submissions_detail(request, problem_id):
    # all submission with that problem id 
    problem = get_object_or_404(Problem, pk=problem_id)
    context = {'problem': problem}

    return render(request, 'problems/submissions_detail.html', context)



@csrf_exempt
def submit(request):
    if request.method != 'POST':
        return HttpResponse("This endpoint is only for code submission. Use POST request only.")

    # request body contain code, and language and problem id
    req_body = request.body

    print(req_body)

    body = json.loads(req_body, strict=False)
    problem_id = int(body['problem_id'])
    language_id = int(body['language_id'])
    code = body['code']

    Logger.log("(views.py)Received submission for P-" + str(problem_id)
               + " language_id " + str(language_id))

    verdict, verdict_type = SubmissionHandler.submit(code, problem_id, language_id)

    verdict_dict = dict({
        'verdict': verdict,
        'verdict_type' : verdict_type
    })

    return JsonResponse(verdict_dict)

# View for profile
def user_profile(request, username):
    context = {}
    return render(request, 'problems/profile.html', context)
