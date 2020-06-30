""" view for handling logging rerouting """
from django.views.generic import View
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class LoggedInView(View):
    """
    Class view to identify who is the logged in User and then redirect
     them to the relevant dashboard
    """
    template_name = "/dashboards/instructor_dashboard.html"

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        """ checks the type of logged in user and redirects accodingly to home pages """
        response = None
        response_url = '/'
        if request.user.groups.filter(name='Instructor').exists():
            response_url = "dashboards/instructor_dashboard.html"
        elif request.user.groups.filter(name='Lecturer').exists():
            response_url = "dashboards/lecturer_dashboard.html"
        elif request.user.groups.filter(name='Student').exists():
            response_url = "dashboards/student_dashboard.html"

        response = render(request, response_url, *args, **kwargs)
        response['Response-URL'] = response_url
        return response
