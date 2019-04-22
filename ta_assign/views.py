from django.shortcuts import render
from django.views import View
from classes.CmdHandler import CmdHandler
from classes.Administrator import Administrator

# Create your views here.


class Home(View):
    def get(self, request):
        return render(request, 'main/index.html')

    def post(self, request):
        get_workin = CmdHandler()
        command_input = request.POST["command"]
        if command_input:
            response = get_workin.parse_command(command_input)
        else:
            response = "Please type a command to do stuff."

        return render(request, 'main/index.html', {"message": response})


class CreateAccount(View):
    def get(self, request):
        return render(request, 'main/create_account.html')

    def post(self, request):
        email = request.POST["email"]
        password = request.POST["password"]
        type = request.POST["type"]
        return render(request, 'main/create_account.html', {"message": [email, password, type]})


class CreateCourse(View):
    def get(self, request):
        return render(request, 'main/create_course.html')

    def post(self, request):
        course_id = request.POST["course_id"]
        course_section = request.POST["course_section"]
        num_labs = request.POST["num_labs"]
        return render(request, 'main/create_course.html', {"message": [course_id, course_section, num_labs]})

class AssignInstructor(View):
    def get(self, request):
        return render(request, 'main/assign_instructor.html')

    def post(self, request):
        course_id = request.POST["course_id"]
        email = request.POST["Instructor email"]
        return render(request, 'main/assign_instructor.html', {"message": [course_id, email]})