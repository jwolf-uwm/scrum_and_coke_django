from django.shortcuts import render, redirect
from django.views import View
from classes.CmdHandler import CmdHandler
from django.contrib import messages
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
            messages.error(request, 'Please login first.')
            return redirect("Login1")

        account_type = request.session.get("type")

        if not account_type == "administrator" and not account_type == "supervisor":
            messages.error(request, 'You do not have access to this page.')
            return redirect("index1")

        return render(request, 'main/create_account.html')

    def post(self, request):

        account_email = request.POST["email"]
        account_password = request.POST["password"]
        account_type = request.POST["type"]
        command_input = "create_account " + account_email + " " + account_password + " " + account_type
        get_workin = CmdHandler()
        response = get_workin.parse_command(command_input)

        if response == "Account Created!":
            messages.success(request, response)
        else:
            messages.error(request, response)

        return render(request, 'main/create_account.html')


class AccessInfo(View):

    def get(self, request):

        if not request.session.get("email"):
            messages.error(request, 'Please login first.')
            return redirect("Login1")

        account_type = request.session.get("type")

        if not account_type == "administrator" and not account_type == "supervisor":
            messages.error(request, 'You do not have access to this page.')
            return redirect("index1")

        get_workin = CmdHandler()
        command_input = "access_info"
        response = get_workin.parse_command(command_input)
        messages.success(request, response)
        return render(request, 'main/access_info.html')


class CreateCourse(View):
    def get(self, request):
        if not request.session.get("email"):
            messages.error(request, 'Please login first.')
            return redirect("Login1")

        account_type = request.session.get("type")

        if not account_type == "administrator" and not account_type == "supervisor":
            messages.error(request, 'You do not have access to this page.')
            return redirect("index1")

        return render(request, 'main/create_course.html')

    def post(self, request):
        course_id = request.POST["course_id"]
        course_section = request.POST["course_section"]
        num_labs = request.POST["num_labs"]

        command_input = "create_course CS" + course_id + "-" + course_section + " " + num_labs
        get_workin = CmdHandler()
        response = get_workin.parse_command(command_input)

        if response == "Course has been created successfully.":
            messages.success(request, response)
        else:
            messages.error(request, response)

        return render(request, 'main/create_course.html', {"message": [course_id, course_section, num_labs]})


class EditAccount(View):
    def get(self, request):
        if not request.session.get("email"):
            messages.error(request, 'Please login first.')
            return redirect("Login1")

        account_type = request.session.get("type")

        if not account_type == "administrator" and not account_type == "supervisor":
            messages.error(request, 'You do not have access to this page.')
            return redirect("index1")

        return render(request, 'main/edit_account.html')

    def post(self, request):
        email = request.POST["email"]
        field = request.POST["field"]
        data = request.POST["data"]
        command_input = "edit_account " + email + " " + field + " " + data
        get_workin = CmdHandler()
        response = get_workin.parse_command(command_input)

        if response == "Command successful.":
            messages.success(request, response)
        else:
            messages.error(request, response)

        return render(request, 'main/edit_account.html')


class EditInfo(View):

    def get(self, request):
        if not request.session.get("email"):
            messages.error(request, 'Please login first.')
            return redirect("Login1")

        return render(request, 'main/edit_info.html')

    def post(self, request):
        email = request.POST["email"]
        password = request.POST["password"]
        name = request.POST["name"]
        phone = request.POST["phone"]
        get_workin = CmdHandler()
        pick_anything = False

        if email != "":
            pick_anything = True
            response = get_workin.parse_command("change_email " + email)

            if response == "Email address changed.":
                messages.success(request, response)
            else:
                messages.error(request, response)

        if password != "":
            pick_anything = True
            response = get_workin.parse_command("change_password " + password)

            if response == "Password changed.":
                messages.success(request, response)
            else:
                messages.error(request, response)

        if name != "":
            pick_anything = True
            response = get_workin.parse_command("change_name " + name)

            if response == "Name changed.":
                messages.success(request, response)
            else:
                messages.error(request, response)

        if phone != "":
            pick_anything = True
            response = get_workin.parse_command("change_phone " + phone)

            if response == "Phone number changed.":
                messages.success(request, response)
            else:
                messages.error(request, response)

        if not pick_anything:
            messages.error(request, "You should pick something to change.")

class AssignInstructorToCourse(View):
    def get(self, request):
        if not request.session.get("email"):
            messages.error(request, 'Please login first.')
            return redirect("Login1")
        account_type = request.session.get("type")
        if not account_type == "supervisor":
            messages.error(request, 'You do not have access to this page.')
            return redirect("index1")
        return render(request, 'main/assign_instructor.html')

    def post(self, request):
        email1 = request.POST["email"]
        course_id = request.POST["course_id"]
        course_section = request.POST["course_section"]
        command_input = "assign_instructor " + email1 + " CS" + course_id + "-" + course_section
        get_workin = CmdHandler()
        response = get_workin.parse_command(command_input)
        if response == "command successful":
            messages.success(request, response)
            return redirect("index1")
        else:
            messages.error(request, response)
        return redirect("index1")


class AssignTAToCourse(View):
    def get(self, request):
        if not request.session.get("email"):
            messages.error(request, 'Please login first.')
            return redirect("Login1")
        account_type = request.session.get("type")
        if not account_type == "supervisor":
            messages.error(request, 'You do not have access to this page.')
            return redirect("index1")
        return render(request, 'main/assign_ta.html')

    def post(self, request):
        email = request.POST["email"]
        course_id = request.POST["course_id"]
        course_section = request.POST["course_section"]
        command_input = "assign_ta " + email + " CS" + course_id + "-" + course_section
        get_workin = CmdHandler()
        response = get_workin.parse_command(command_input)
        if response == "command successful":
            messages.success(request, response)
        else:
            messages.error(request, response)
        return redirect("index1")