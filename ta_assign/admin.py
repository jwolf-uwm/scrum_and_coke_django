from django.contrib import admin

# Register your models here.
from .models import (Person)
from .models import (Administrator)
from .models import (Supervisor)
from .models import (TA)
from .models import (Instructor)
from .models import (Course)
admin.site.register(Person)
admin.site.register(Administrator)
admin.site.register(Supervisor)
admin.site.register(TA)
admin.site.register(Instructor)
admin.site.register(Course)