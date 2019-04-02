from django.contrib import admin

# Register your models here.
from .models import (ModelPerson)
from .models import (ModelAdministrator)
from .models import (ModelSupervisor)
from .models import (ModelTA)
from .models import (ModelInstructor)
from .models import (ModelCourse)
from .models import (ModelTACourse)
admin.site.register(ModelPerson)
admin.site.register(ModelAdministrator)
admin.site.register(ModelSupervisor)
admin.site.register(ModelTA)
admin.site.register(ModelInstructor)
admin.site.register(ModelCourse)
admin.site.register(ModelTACourse)
