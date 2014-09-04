from django.shortcuts import render_to_response, HttpResponseRedirect
from Testing import commands

# Create your views here.



def controller(request):
    helper = commands.RequestHelper()
    command = helper.get_command(request)
    page, context = command.execute(request)
    if (context.get('redirect', False)):
        return HttpResponseRedirect(page)
    else:
        return render_to_response(page, context)


