from django.shortcuts import render
from .models import Todo

from .serializers import TodoSerializer
from rest_framework import viewsets


# Create your views here.
class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all().order_by('created_on')
    serializer_class = TodoSerializer


def overview_to_dos(request):
    to_dos = Todo.objects.all()
    context = {
        'to_dos': to_dos
    }
    return render(request, 'todo_index.html', context)


def todo_detail(request, pk):
    to_do = Todo.objects.get(pk=pk)
    context = {
        'to_do': to_do
    }
    return render(request, 'todo_detail.html', context)
