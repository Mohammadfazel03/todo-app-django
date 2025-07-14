from distutils.util import strtobool

from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.core.exceptions import PermissionDenied
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


class UpdateTaskView(AccessMixin, UpdateView):
    model = Task
    fields = ['content']
    success_url = reverse_lazy("task:index")
    template_name = "edit.html"
    context_object_name = 'task'
    login_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if request.user == self.get_object().user:
            return super().dispatch(request, *args, **kwargs)

        raise PermissionDenied()


class DeleteTaskView(AccessMixin, DeleteView):
    model = Task
    success_url = reverse_lazy("task:index")
    login_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if request.user == self.get_object().user:
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied()


class ChangeStateTaskView(AccessMixin, View):
    http_method_names = ['post']
    login_url = reverse_lazy('login')

    def dispatch(self, request, pk, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if request.user == Task.objects.get(pk=pk).user:
            return super().dispatch(request, pk, *args, **kwargs)

        raise PermissionDenied()

    def post(self, request, pk, *args, **kwargs):
        task = Task.objects.get(pk=pk)
        if request.POST.get('is_complete'):
            task.is_complete = not strtobool(request.POST.get('is_complete'))
            task.save()
        return HttpResponseRedirect(reverse_lazy('task:index'))
