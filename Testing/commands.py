from django.http import Http404
from Testing import forms
from django.contrib import auth
from Testing import models

class RequestHelper:

    def __init__(self):
        self.commands = dict(login=LoginCommand(),
                             logout=LogoutCommand(),
                             choose_test=ChooseTestCommand(),
                             end_test=EndTestCommand())

    def get_command(self, request):
        command = request.GET.get('command', '') if request.method == 'GET' else request.POST.get('command', '')
        return self.commands.get(command, NoCommand())


class NoCommand:
    def execute(self, request):
        params = request.GET if request.method == 'GET' else request.POST
        if request.user.is_authenticated():
            if request.user.is_staff:
                return ('/admin/', dict(redirect=True))
            else:
                subjects = models.Subject.objects.all();
                lst = []
                for subject in subjects:
                    lst.append([subject.name, models.Test.objects.filter(subject=subject)])
                return ('test.html', dict(redirect=False, lst=lst))
        else:
            return ('login.html', dict(redirect=False, form=forms.LoginForm()))


class LoginCommand:
    def execute(self, request):
        if request.method != 'POST':
            raise Http404('Only POST-request are allowed')
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = auth.authenticate(username=cd['username'],
                                     password=cd['password'])
            if user is not None and user.is_active:
                auth.login(request, user)
        return '', dict(redirect=True)

class LogoutCommand:
    def execute(self, request):
        if request.method != 'POST':
            raise Http404('Only POST-request are allowed')
        auth.logout(request)
        return '', dict(redirect=True)


class ChooseTestCommand:
    def execute(self, request):
        if request.method != 'POST':
            raise Http404('Only POST-request are allowed')
        if not request.POST.get('test', ''):
            request.POST = {}
            return '', dict(redirect=True)
        questions = models.Question.objects.filter(test_id=request.POST['test'])
        lst = []
        for question in questions:
            lst.append([question.text, models.Variant.objects.filter(question=question)])
        return ('questions.html', dict(redirect=False, questions=lst))


class EndTestCommand:
    def execute(self, request):
        if request.method != 'POST':
            raise Http404('Only POST-request are allowed')
        return ('final.html', dict(redirect=False))