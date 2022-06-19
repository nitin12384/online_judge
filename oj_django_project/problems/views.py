from django.shortcuts import render, get_object_or_404
from .models import Problem

# Create your views here.

def index(request) :
    context = {
        'problem_list' : Problem.objects.all()
    }

    return render(request, 'problems/index.html', context)

def detail(request, problem_id) :
    
    problem = get_object_or_404(Problem, pk=problem_id)
    
    context = {
        'problem' : problem
    }
    return render(request, 'problems/detail.html', context)

