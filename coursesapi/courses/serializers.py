from rest_framework.serializers import ModelSerializer

from courses.models import Category, Course, Lesson, Comment, Tag, User


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class ModelSerializerContainsImage(ModelSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['image'] = instance.image.url if instance.image else ''
        return data


class CourseSerializer(ModelSerializerContainsImage):
    class Meta:
        model = Course
        fields = ['id', 'subject', 'image', 'created_date', 'category_id']


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class LessonSerializer(ModelSerializerContainsImage):
    tags = TagSerializer(many=True)
    class Meta:
        model = Lesson
        fields = ['id', 'subject', 'image', 'course_id', 'created_date', 'updated_date', 'tags']


class LessonDetailsSerializer(ModelSerializerContainsImage):
    class Meta:
        model = LessonSerializer.Meta.model
        fields = LessonSerializer.Meta.fields + ['content']



class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username']


class NewUserSerializer(ModelSerializer):
    class Meta:
        model = UserSerializer.Meta.model
        fields = UserSerializer.Meta.fields + ['password', 'avatar']

    def to_representation(self, instance):
        data = super().to_representation(self)

        return data


class CommentSerializer(ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_date', 'updated_date', 'user']
