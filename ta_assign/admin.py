from django.contrib import admin

# Register your models here.
from .models import (ModelPerson)
from .models import (ModelCourse)
from .models import (ModelTACourse)
admin.site.register(ModelPerson)
admin.site.register(ModelCourse)
admin.site.register(ModelTACourse)
