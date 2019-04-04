from django.shortcuts import render
from django.views import View
from classes.CmdHandler import CmdHandler

# Create your views here.


class Home(View):
    get_workin = CmdHandler()

    def get(self, request):
        return render(request, 'main/index.html')

    def post(self, request):
        command_input = request.POST["command"]
        if command_input:
            response = self.get_workin.parse_command(command_input)
        else:
            response = "Please type a command to do stuff."

        return render(request, 'main/index.html', {"message": response})
