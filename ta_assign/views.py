from django.shortcuts import render
from django.views import View
from classes.CmdHandler import CmdHandler

# Create your views here.


class Home(View):

    def get(self, request):
        return render(request, 'main/index.html')

    def post(self, request):
        # your_instance = SomeCommandClass()
        command_input = request.POST["command"]
        if command_input:
            response = CmdHandler().deal_with_command(command_input)
        else:
            response = ""

        return render(request, 'main/index.html', {"message": response})
