from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.views.generic import DeleteView, ListView, DetailView
from django.contrib.auth import logout
from django.contrib import messages


from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import UpdateView, CreateView
from django.views import View

from .forms import UserRegisterForm, ChangeUserInfoForm, CreatePollForm
from .models import AdvUser, Poll, Choice


def other_page(request, page):
    try:
        template = get_template('main/' + page + '.html')
    except TemplateDoesNotExist:
        raise Http404
    return HttpResponse(template.render(request=request))


def index(request):
    return render(request, 'main/index.html')

class PollHome(ListView):
    model = Poll
    template_name = 'main/home.html'



class BBLoginView(LoginView):
    template_name = 'main/login.html'


@login_required
def profile(request):
    return render(request, 'main/profile.html')


class BBLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'main/logout.html'


class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin,
                         UpdateView):
    model = AdvUser
    template_name = 'main/change_user_info.html'
    form_class = ChangeUserInfoForm
    success_url = reverse_lazy('main:profile')
    success_message = 'Личные данные пользователя изменены'

    def dispatch(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class BBPasswordChangeView(SuccessMessageMixin, LoginRequiredMixin,
                           PasswordChangeView):
    template_name = 'main/password_change.html'
    success_url = reverse_lazy('main:profile')
    success_message = 'Пароль пользователя изменен'

class RegistrateUser(CreateView):

    def get(self, request, *args, **kwargs):
        form = {'form': RegistrateUser()}
        return render(request, 'main/register_user.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = UserRegisterForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return render(request, 'main/register_done.html', {'form': form})
            if 'avatar' in request.FILES:
                profile.avatar = profile["avatar"]
        return render(request, 'main/register_user.html', {'form': form})


class DeleteUserView(LoginRequiredMixin, DeleteView):
   model = AdvUser
   template_name = 'main/delete_user.html'
   success_url = reverse_lazy('main:index')

   def dispatch(self, request, *args, **kwargs):
       self.user_id = request.user.pk
       return super().dispatch(request, *args, **kwargs)

   def post(self, request, *args, **kwargs):
       logout(request)
       messages.add_message(request, messages.SUCCESS, 'Пользователь удален')
       return super().post(request, *args, **kwargs)

   def get_object(self, queryset=None):
       if not queryset:
           queryset = self.get_queryset()
       return get_object_or_404(queryset, pk=self.user_id)


class CreatePoll(CreateView):
    model = Poll
    template_name = 'main/create.html'
    success_url = reverse_lazy('main:index')
    form_class = CreatePollForm

class ViewPolls(ListView):
    model = Poll
    template_name = 'main/index.html'
    context_object_name = 'polls'

class DetailView(DetailView):
    model = Poll
    template_name = 'main/detail.html'


class ResultsView(DetailView):
    model = Poll
    template_name = 'main/results.html'


def vote(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    try:
        selected_choice = poll.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'main/detail.html', {
            'Poll': Poll,
            'error_message': 'вы не сделали выбор'
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('main:results', args=(poll.id,)))





