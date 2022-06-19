from django.shortcuts import render, get_object_or_404
from .models import Problem
from .utility import to_window_slash,get_problem_detailed_context


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

def submit(request, problem_id) :
    
    problem = get_object_or_404(Problem, pk=problem_id)
    context = {'problem' : problem}
    return render(request, 'problems/submit.html', context)
