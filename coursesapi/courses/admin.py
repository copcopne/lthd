from django.contrib import admin
from courses.models import Course, Category, Lesson
from django.utils.html import mark_safe
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class CourseAppAdminSite(admin.AdminSite):
    site_header = "Hệ thống khóa học trực tuyến"


admin_site = CourseAppAdminSite(name="myadmin")


class LessonForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget)
    class Meta:
        model = Lesson
        fields = '__all__'


class MyCourseView(admin.ModelAdmin):
    list_display = ['id', 'subject', 'active', 'category', 'created_date']
    search_fields = ['subject', 'category']
    list_filter = ['id', 'subject']
    list_editable = ['subject']
    readonly_fields = ['image_view']

    def image_view(self, course):
        return mark_safe(f"<img src='/static/{course.image.name}' width='200' />")


class myEditorForm(admin.ModelAdmin):
    form = LessonForm


admin_site.register(Course, MyCourseView)
admin_site.register(Category)
admin_site.register(Lesson, myEditorForm)
