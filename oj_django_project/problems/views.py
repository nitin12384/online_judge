from cmath import log
import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404

from .backend import configs
from .models import Problem, Submission
from .backend.utils import get_problem_detailed_context
from django.views.decorators.csrf import csrf_exempt
from .backend.utils import Logger
from .backend.core import SubmissionHandler

from django.contrib.auth.models import User
# Create your views here.

from .backend import db_handler


def index(request):
    Logger.log('Index page requested')
    is_logged_in = True
    username = ''
    
    if request.user.is_anonymous :
        is_logged_in = False
    else :
        username = request.user.username

    context = {
        'problem_list': Problem.objects.all(),
        'is_logged_in' : is_logged_in,
        'username' : username,
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

# Todo : Move code to functions, modularize it
# View for profile
def user_profile(request, username):
    user = get_user_obj(username)
    if user is None:
        # 404 page
        return render(request, 'problems/404.html')
    else:
        is_logged_in = is_user_logged_in(request, username)
        user_private_info = None 
        if is_logged_in :
            user_private_info = get_user_private_info(user)

        context = {
            'user_public_info' : get_user_public_info(user),
            'is_logged_in' : is_logged_in,
            'user_private_info' : user_private_info
        }
        return render(request, 'problems/profile.html', context)


## Utility Code : Later, move them to seperate file

class UserPublicInfo:
    
    def __init__(self):
        self.is_valid = False

    def __init__(self,
        username            ,
        full_name           ,
        num_problems_solved ,
    ):
        self.is_valid             = True            
        self.username             = username            
        self.full_name            = full_name           
        self.num_problems_solved  = num_problems_solved 
    

class UserPrivateInfo:
    def __init__(self,
        email
    ):
        self.email = email

def get_user_obj(username : str):
    user_qset = User.objects.filter(username=username)

    if user_qset.exists() :
        return user_qset[0]
    else:
        return None

def get_user_public_info(user_obj) -> UserPublicInfo:
    username = user_obj.username
    user_id = user_obj.id 
    full_name = user_obj.first_name + configs.SPACE + user_obj.last_name
    num_problems_solved = 0
    return UserPublicInfo(username, full_name, num_problems_solved)

def get_user_private_info(user_obj) -> UserPrivateInfo:
    email = user_obj.email 
    return UserPrivateInfo(email)


def is_user_logged_in(request, username):
    # Todo : Find out what user.is_active means
    if request.user.is_anonymous :
        return False
    else :
        return request.user.username == username 
