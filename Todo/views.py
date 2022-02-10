from django.shortcuts import render, redirect
from .forms import TodoForm
from .models import Todo


from .serializers import TodoSerializer
from rest_framework import viewsets


# Create your views here.
class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all().order_by('created_on')
    serializer_class = TodoSerializer


def create_form(request):
    form = TodoForm()
    context = {
        'task_form': form
    }
    return render(request, 'todo/todo_form.html', context)


def overview_to_dos(request):
    to_dos = Todo.objects.all()
    context = {
        'to_dos': to_dos
    }
    return render(request, 'todo/todo_index.html', context)


def update_todo(request, pk):
    to_do = Todo.objects.get(id=pk)

    if request.method == 'POST':
        form = TodoForm(request.Post, instance=to_do)
        if form.is_valid():
            form.save()
            return redirect('all-todos')

        context = {
            'forms': form,
            'to_do': to_do
        }
    return render(request, 'todo/todo_update_form.html', context)
