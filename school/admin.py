from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from .models import UserBase

class UserBaseAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'user_type', 'email', 'phone', 'is_active']
    change_list_template = "admin/school/userbase/change_list.html"  # custom template

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('add-new-member/', self.admin_site.admin_view(self.add_new_member), name='add_new_member'),  # 👈 Ye line hi url name set karta hai
        ]
        return custom_urls + urls

    def add_new_member(self, request):
        return redirect('/create-user/')  # 👈 This can point to your form

admin.site.register(UserBase, UserBaseAdmin)