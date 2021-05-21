from django.contrib import admin
from .models import *
admin.site.register(model_system)
admin.site.register(model_lfile)
admin.site.register(site_identify)
admin.site.register(site_hardware)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Statistic)
# Register your models here.
