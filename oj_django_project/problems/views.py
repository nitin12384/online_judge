import json
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate


from .backend import configs
from .models import Problem, UserInfo, Language
from .backend.utils import Logger
from .backend.core import SubmissionHandler
from .backend.configs import cur_config


def index(request):
    Logger.log('Index page requested')

    # merging the two dictionaries by using |
    context = {'problem_list': Problem.objects.all(), **get_cur_user_context(request) }
    
    return render(request, 'problems/index.html', context)


def detail_submit(request, problem_id):
    problem = get_object_or_404(Problem, pk=problem_id)

    # merging the two dictionaries by using |
    context = { **get_problem_detailed_context(problem) , **get_cur_user_context(request) } 

    return render(request, 'problems/detail_submit.html', context)


def submissions_detail(request, problem_id):
    # all submission with that problem id 
    problem = get_object_or_404(Problem, pk=problem_id)

    # merging the two dictionaries by using |
    context = {'problem': problem, **get_cur_user_context(request) }

    return render(request, 'problems/submissions_detail.html', context)



@csrf_exempt
def submit(request):
    if request.method != 'POST':
        return HttpResponse("This endpoint is only for code submission. Use POST request only.")
    
    user = get_cur_user_obj(request)
    if user is None:
        # Not logged in.
        return JsonResponse({
            'verdict': 'Please Login to Submit code.',
            'verdict_type' : -1
        })        

    # request body contain code, and language and problem id
    req_body = request.body

    #print(req_body)

    body = json.loads(req_body, strict=False)
    problem_id = int(body['problem_id'])
    language_id = int(body['language_id'])
    code = body['code']

    Logger.log("(views.py)Received submission for P-" + str(problem_id)
               + " language_id " + str(language_id))

    verdict, verdict_type, verdict_details = SubmissionHandler.submit(code, user, problem_id, language_id)

    verdict_dict = dict({
        'verdict': verdict,
        'verdict_type' : verdict_type,
        'verdict_details' : verdict_details
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
        is_requested_user_logged_in = is_user_logged_in(request, username)
        user_private_info = None 
        if is_requested_user_logged_in :
            user_private_info = get_user_private_info(user)

        context = {
            'user_public_info' : get_user_public_info(user),
            'is_requested_user_logged_in' : is_requested_user_logged_in,
            'user_private_info' : user_private_info,
            **get_cur_user_context(request),
            
        }
        return render(request, 'problems/profile.html', context)


# next_page_field_name = 'next'

# cant use reverse globally
# default_next_page = reverse('problems:index')

# Todo Test if works
default_next_page = '/'

## User Auth related views : 

def login_page(request, error_message : str = ''):
    next_page = get_next_page(request)
    context = get_login_page_context(next_page, error_message)
    return render(request, 'problems/login.html', context)

# for post request of login
def login_action(request):

    Logger.log("login action initialted")
    error_message = ''
    next_page = get_next_page(request)

    try:
        username = request.POST['username-input']
        password = request.POST['password-input']

        user_obj_qset = User.objects.filter(username=username)

        if not user_obj_qset.exists() : 
            error_message = "No user with username - " + username
        else :
            log = ""
            user_obj = user_obj_qset[0]

            if user_obj.is_authenticated :
                log += "Given user is Already authenticated .\n"

            user = authenticate(username=username, password=password)

            if user is None :
                log += "Given password is wrong\n"
                error_message = "Wrong Password"
                Logger.log(log)
            else :
                log += "Successfully authenticated\n"
                # just sets the cookie
                login(request, user)
                log += "Successfully logged in .\n"
                Logger.log(log)
                # we are done here. Now redirect

                return HttpResponseRedirect(next_page)

    except KeyError:
        print("KeyError")
        error_message = 'KeyError in form. Invalid form input field names'
        
    Logger.log("!!!!! Error Message : " + error_message)

    return login_page(request, error_message)

# for post request of signup
def signup_action(request):

    Logger.log("signup action initialted")
    
    error_message = ''
    next_page = get_next_page(request)

    try:
        username = request.POST['username-input']
        email = request.POST['email-input']
        password = request.POST['password-input']
        re_password = request.POST['re-enter-password-input']

        user_obj_qset = User.objects.filter(username=username)

        if user_obj_qset.exists() : 
            error_message = "There are existing user with username - " + username
        elif password != re_password:
            error_message = "Password dont match" 
        # no need to check for email validation
        else :
            log = ""
            # create user
            new_user = User.objects.create_user(username, email, password)
            new_user.save()

            # create userinfo
            UserInfo.create_userinfo(new_user)

            log += "Created User and UserInfo object\n"
            authenticate(username=username, password=password)
            login(request, new_user)
            log += "Loggin In the user\n" 
            log += "Signup of username - " + username + " Completed\n"
            Logger.log(log)
            return HttpResponseRedirect(next_page)

    except KeyError:
        print("KeyError")
        error_message = 'KeyError in form. Invalid form input field names'
        
    Logger.log("!!!!! Error Message : " + error_message)

    return signup_page(request, error_message)

def signup_page(request, error_message : str = ''):
    next_page = get_next_page(request)
    context = get_signup_page_context(next_page, error_message)
    return render(request, 'problems/signup.html', context)


def logout_action(request):
    next_page = get_next_page(request)
    logout(request)
    return HttpResponseRedirect(next_page)


## Utility Code : Later, move them to seperate file

def get_login_page_context(next_page : str, error_message : str=''):
    post_url = reverse('problems:login_action_path') + '?next=' + next_page
    return get_form_page_context(post_url, error_message)

def get_signup_page_context(next_page : str, error_message : str=''):
    post_url = reverse('problems:signup_action_path') + '?next=' + next_page
    return get_form_page_context(post_url, error_message)

def get_form_page_context(post_url:str, error_message : str=''):
    form_input_error = False

    if error_message != '' :
        form_input_error = True
    
    context = {
        'post_url':post_url,
        'form_input_error' : form_input_error,
        'error_message' : error_message
    }
    return context


def get_next_page(request):
    try:
        return request.GET['next']
    except KeyError:
        Logger.log("KeyError in get_next_page")
        return default_next_page

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

def get_cur_user_obj(request):
    if not is_cur_user_logged_in(request):
        return None 
    else:
        # Still may return none.
        return get_user_obj(request.user.username)

def get_user_obj(username : str):
    user_qset = User.objects.filter(username=username)

    if user_qset.exists() :
        return user_qset[0]
    else:
        return None

def get_user_public_info(user_obj) -> UserPublicInfo:
    username = user_obj.username
    full_name = user_obj.first_name + configs.SPACE + user_obj.last_name
    num_problems_solved = UserInfo.get_num_problems_solved(user_obj)
    return UserPublicInfo(username, full_name, num_problems_solved)

def get_user_private_info(user_obj) -> UserPrivateInfo:
    email = user_obj.email 
    return UserPrivateInfo(email)

def is_user_logged_in(request, username):
    # Todo : Find out what user.is_active means
    if not is_cur_user_logged_in(request) :
        return False
    else :
        return request.user.username == username 

def get_cur_user_context(request):
    is_logged_in = True
    username = ''

    if not is_cur_user_logged_in(request) :
        is_logged_in = False
    else :
        username = request.user.username
    return {
        'is_logged_in' : is_logged_in,
        'username' : username,
    }

def is_cur_user_logged_in(request):
    return request.user.is_authenticated

"""
absolute path = "C:\\....\data\problems_data"
data_dir_path = "\1"

/desc.txt : description of the file
/input.txt : input details
/output.txt : output details
/constraints.txt : constraints details
/examples.txt : constraints details

/testcases/ : directory of test_cases, in which we have input/output files
inp_1.txt, inp_2.txt, ....inp_k.txt, where k is 'num_testcases'
out_1.txt, out_2.txt, ...
"""
def get_problem_detailed_context(problem: Problem) -> dict:

    data_dir = configs.cur_config.problem_data_dir_path + problem.data_dir_path 
    
    description_file_path = data_dir + "/description.txt"
    input_file_path = data_dir + "/input.txt"
    output_file_path = data_dir + "/output.txt"
    constraints_file_path = data_dir + "/constraints.txt"
    examples_file_path = data_dir + "/examples.txt"

    file_paths = [description_file_path, input_file_path, output_file_path,
                  constraints_file_path, examples_file_path]
    
    # require backslash formatting in windows, otherwize "type" command wont work
    file_paths = [ cur_config.path_formatter(path) for path in file_paths ]

    files = [open(s, "r") for s in file_paths]
    file_data = [f.read() for f in files]

    # close files
    for f in files:
        f.close()

    plr_set = problem.problemlanguagerelation_set.all()

    languages = []
    languages_str = ""

    for plr in plr_set:
        language_id = plr.language_id
        cur_language = Language.objects.get(pk=language_id)
        languages.append(cur_language)
        languages_str += cur_language.name + ", "

    return {
        'problem': problem,

        'description': file_data[0],
        'input': file_data[1],
        'output': file_data[2],
        'constraints': file_data[3],
        'examples': file_data[4],
        'languages': languages,
        'languages_str': languages_str,

    }

