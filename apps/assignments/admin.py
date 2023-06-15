from django.contrib import admin

from .models import Assignments


class AssignmentsAdmin(admin.ModelAdmin):
    pass


admin.site.register(Assignments, AssignmentsAdmin)
