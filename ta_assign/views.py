from django.shortcuts import render, redirect
from django.views import View
from classes.CmdHandler import CmdHandler
from django.contrib.messages import error
from ta_assign import models

# Create your views here.


class Index(View):
    def get(self, request):
        return render(request, 'main/index.html')


class Command(View):
    def get(self, request):
        return render(request, 'main/command.html')

    def post(self, request):
        get_workin = CmdHandler()
        command_input = request.POST["command"]
        if command_input:
            response = get_workin.parse_command(command_input)
        else:
            response = "Please type a command to do stuff."

        return render(request, 'main/command.html', {"message": response})


class Login(View):
    def get(self, request):
        if request.session.get("email"):
            return redirect("index1")

        return render(request, "main/login.html")

    def post(self, request):
        username = request.POST["email"]
        password = request.POST["password"]
        user = models.ModelPerson.objects.all().filter(email=username)

        if user.count() == 0 or user[0].password != password:
            return render(request, "main/login.html", {"error_messages": "username/password incorrect"})

        models.ModelPerson.objects.filter(email=username).update(isLoggedOn=True)
        request.session["email"] = username
        request.session["type"] = user[0].type
        return redirect("index1")


class Logout(View):
    def get(self, request):
        if not request.session.get("email"):
            return redirect("index1")
        username = request.session.get("email")
        models.ModelPerson.objects.filter(email=username).update(isLoggedOn=False)
        request.session.pop("email", None)
        return redirect("Login1")


class CreateAccount(View):

    def get(self, request):

        if not request.session.get("email"):
            error(request, 'Please login first.')
            return redirect("Login1")

        account_type = request.session.get("type")

        if not account_type == "administrator" and not account_type == "supervisor":
            error(request, 'You do not have access to this page.')
            return redirect("index1")

        return render(request, 'main/create_account.html')

    def post(self, request):
        account_email = request.POST["email"]
        account_password = request.POST["password"]
        account_type = request.POST["type"]
        command_input = "create_account " + account_email + " " + account_password + " " + account_type
        get_workin = CmdHandler()
        response = get_workin.parse_command(command_input)
        return render(request, 'main/create_account.html', {"message": response})


class CreateCourse(View):
    def get(self, request):
        return render(request, 'main/create_course.html')

    def post(self, request):
        course_id = request.POST["course_id"]
        course_section = request.POST["course_section"]
        num_labs = request.POST["num_labs"]
        return render(request, 'main/create_course.html', {"message": [course_id, course_section, num_labs]})
