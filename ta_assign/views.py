from django.shortcuts import render
from django.views import View
from ta_assign.models import ModelPerson

# Create your views here.


class Home(View):

    def get(self, request):
        return render(request, 'main/index.html')

    def post(self, request):
        your_instance = ModelPerson()
        command_input = request.POST["command"]
        if command_input:
            response = your_instance.command(command_input)
        else:
            response = ""
        return render(request, 'main/index.html', {"message": response})
