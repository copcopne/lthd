from django.contrib import admin
from django.db.models import Count
from django.template.response import TemplateResponse
from django.urls import path

from courses.models import Course, Category, Lesson, Tag, Comment
from django.utils.html import mark_safe
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class CourseAppAdminSite(admin.AdminSite):
    site_header = "Hệ thống khóa học trực tuyến"

    def get_urls(self):
        return [
            path('cate-stats/', self.cate_stats)
        ] + super().get_urls()

    # def stats_view(self, request):
    #     count = Course.objects.filter(active=True).count()
    #     stats = Course.objects \
    #         .annotate(lesson_count=Count('lesson')) \
    #         .values('id', 'subject', 'lesson_count')
    #     return TemplateResponse(request,
    #                             'admin/course-stats.html', {
    #                                     'course_count': count,
    #                                     'course_stats': stats
    #                                 }
    #                             )
    
    def cate_stats(self, request):
        stats = Category.objects.annotate(course_count=Count('course__id')) \
            .values('id', 'name', 'course_count')
        return TemplateResponse(request, 'admin/cate-stats.html', {
            'stats': stats
        })


admin_site = CourseAppAdminSite(name="myadmin")


class LessonForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget)
    class Meta:
        model = Lesson
        fields = '__all__'


class LessonInlineAdmin(admin.StackedInline):
    model = Lesson
    fk_name = 'course' # tên khoá ngoại (tuỳ chọn)


class LessonTagInlineAdmin(admin.TabularInline):
    model = Lesson.tags.through


class TagAdmin(admin.ModelAdmin):
    inlines = [LessonTagInlineAdmin, ]


class MyCourseView(admin.ModelAdmin):
    list_display = ['id', 'subject', 'active', 'category', 'created_date']
    search_fields = ['subject', 'category']
    list_filter = ['id', 'subject']
    list_editable = ['subject']
    readonly_fields = ['image_view']
    inlines = [LessonInlineAdmin, ]

    def image_view(self, course):
        return mark_safe(f"<img src='/static/{course.image.name}' width='200' />")


class MyEditorForm(admin.ModelAdmin):
    form = LessonForm
    inlines = [LessonTagInlineAdmin, ]
    
    class Media:
        css = {
            'all': ('/static/css/style.css',)
        }
        js = ('/static/js/script.js',)


admin_site.register(Category)
admin_site.register(Course, MyCourseView)
admin_site.register(Lesson, MyEditorForm)
admin_site.register(Tag, TagAdmin)
admin_site.register(Comment)