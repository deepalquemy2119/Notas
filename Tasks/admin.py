from django.contrib import admin

# Register your models here.

# modelo Tasks

# para heredar del modelo y poder ver las fechas
class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ('created', )  # es una tupla



from .models import Task
admin.site.register(Task, TaskAdmin)