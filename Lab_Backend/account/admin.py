from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, StudentDetail,Course,FormFillUp

# Register your models here.


class CustomUserAdmin(UserAdmin):

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ["email", "roll", "is_superuser", "is_staff", "is_active"]
    list_filter = ["is_superuser"]
    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["roll"]}),
        ("Permissions", {"fields": ["is_superuser","is_staff","is_active"]}),
        ('Group Permissions', {
            
            'fields': ('groups','user_permissions', )
        })
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "roll", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["email","roll"]
    ordering = ["id","email"]
    filter_horizontal = []


class FormFillUpAdmin(admin.ModelAdmin):
    list_display = ('user','year','semester','academic_year','student_type','student_status','complete')
    search_fields=["user"]
    ordering = ["id","user","start"]

class CourseAdmin(admin.ModelAdmin):
    list_display = ('session','semester', 'course_code', 'course_credit','course_title')
    search_fields=["course_code"]
    ordering = ["id", "course_code"]

admin.site.register(CustomUser,CustomUserAdmin)
admin.site.register(StudentDetail)
admin.site.register(Course,CourseAdmin)
admin.site.register(FormFillUp,FormFillUpAdmin)