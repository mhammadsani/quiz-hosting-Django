from django.http import HttpResponseRedirect

def is_authenticated(view_function):
    def check_if_authenticated(request):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/profile/')
        return view_function(request)
    return check_if_authenticated
