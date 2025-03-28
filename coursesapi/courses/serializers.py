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
    def to_representation(self, instance):
        data = super().to_representation(instance)

        data['avatar'] = instance.avatar.url if instance.avatar else ''

        return data

    def create(self, validated_data):
        data = validated_data.copy()
        u = User(**data)
        u.set_password(u.password)
        u.save()

        return u

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 'avatar']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

class CommentSerializer(ModelSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance=instance)
        data['user'] = UserSerializer(instance=instance.user).data
        return data

    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_date','updated_date', 'user', 'lesson']
        extra_kwargs = {
            'lesson': {
                'write_only': True
            }
        }
