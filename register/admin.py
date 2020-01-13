from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):

    def username(self, obj):
        return obj.user.username

    def name(self, obj):
        return obj.user.first_name + " " + obj.user.last_name

    list_display = ['username', 'name', 'image', 'phone_no']
    list_editable = ['image','phone_no']
    search_fields = ['user__username']

admin.site.register(Profile, ProfileAdmin)