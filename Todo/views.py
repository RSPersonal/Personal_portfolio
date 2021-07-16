from django.shortcuts import render
from .models import Todo

# Create your views here.
def todo_index(request):
    
    all_todos = Todo.objects.all()
    context = {
        'Todo': all_todos
    }

    return render(request, 'todo_index.html', context)