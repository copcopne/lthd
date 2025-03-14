from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from courses import serializers, paginations
from courses.models import Category, Course, Lesson, User


class CategoryViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Category.objects.filter(active=True)
    serializer_class = serializers.CategorySerializer


class CourseViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Course.objects.filter(active=True)
    serializer_class = serializers.CourseSerializer
    pagination_class = paginations.ItemPaginator

    def get_queryset(self):
        query = self.queryset

        q = self.request.query_params.get('q')
        if q:
            query = query.filter(subject__icontains=q)
        c_id = self.request.query_params.get('category_id')
        if c_id:
            query = query.filter(category_id=c_id)

        return query

    @action(methods=['GET'], detail=True, url_path='lesson')
    def get_lessons(self, request, pk):
        lessons = self.get_object().lesson_set.prefetch_related('tags').filter(active=True)
        return Response(serializers.LessonSerializer(lessons, many=True).data, status=status.HTTP_200_OK)


class LessonsViewSet(viewsets.ViewSet, generics.RetrieveAPIView):
    queryset = Lesson.objects.prefetch_related('tags').filter(active=True)
    serializer_class = serializers.LessonDetailsSerializer

    @action(methods=['get'], detail=True, url_path='comments')
    def get_comments(self,request, pk):
        comments = self.get_object().comment_set.filter(active=True)
        return Response(serializers.CommentSerializer(comments, many=True).data, status= status.HTTP_200_OK)


class UserViewSet(viewsets.ViewSet, generics.GenericAPIView, CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = serializers.NewUserSerializer