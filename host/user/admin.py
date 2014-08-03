# -*- coding: utf-8 -*- 
from user.models import RegularUser, LicencePlates

class RegularUserAdmin(admin.ModelAdmin):
    search_fields = ['user']
    list_display = ['id','user']
    
class LicencePlatesAdmin(admin.ModelAdmin):
    search_fields = ['licence_plate']
    list_display = ['user_id', 'licence_plate']

admin.site.register(LicencePlates, LicencePlatesAdmin)