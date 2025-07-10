from distutils.util import strtobool

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, UpdateView, DeleteView

from task.forms import CreateTaskForm
from task.models import Task


class IndexView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'main.html'
    login_url = reverse_lazy('login')

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


class CreateTaskView(LoginRequiredMixin, View):
    http_method_names = ['post']
    form_class = CreateTaskForm
    login_url = reverse_lazy('login')

    def post(self, request, *args, **kwargs):
        form = CreateTaskForm(request.POST)
        if form.is_valid():
            form.instance.user = self.request.user
            form.save()

        return HttpResponseRedirect(reverse_lazy('task:index'))


class UpdateTaskView(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['content']
    success_url = reverse_lazy("task:index")
    template_name = "edit.html"
    context_object_name = 'task'
    login_url = reverse_lazy('login')


class DeleteTaskView(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy("task:index")
    login_url = reverse_lazy('login')


class ChangeStateTaskView(LoginRequiredMixin, View):
    http_method_names = ['post']
    login_url = reverse_lazy('login')

    def post(self, request, pk, *args, **kwargs):
        task = Task.objects.get(pk=pk)
        if request.POST.get('is_complete'):
            task.is_complete = not strtobool(request.POST.get('is_complete'))
            task.save()
        return HttpResponseRedirect(reverse_lazy('task:index'))
