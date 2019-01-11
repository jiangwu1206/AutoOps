from django.contrib import admin
from .models import HostInfo, StatusInfo

# Register your models here.
admin.site.register(HostInfo)
admin.site.register(StatusInfo)
