from rest_framework import serializers
# from drf_writable_nested.serializers import WritableNestedModelSerializer
from .models import CustomUser, StudentDetail, Course,FormFillUp
from django.contrib.auth.hashers import check_password
from django.conf import settings


class CustomUserSerializer(serializers.ModelSerializer):
    password2 = {'style':{'input_type':'password'},'write_only':True}
    class Meta:
        model = CustomUser
        fields = ['id','email','roll','password']
        extra_kwargs = {'password':{'style':{'input_type':'password'},'write_only':True}}
    
    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email = validated_data.pop('email'),
            roll = validated_data.pop('roll'),
            password = validated_data.pop('password')
        )
        return user
    

class StudentSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    
    class Meta:
        model = StudentDetail
        fields = ['user','id','reg','profile_pic','session','full_name','fathers_name','mothers_name','mobile_no']
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = CustomUserSerializer.create(CustomUserSerializer(), validated_data=user_data)

        student, created = StudentDetail.objects.update_or_create(
            user=user,
            reg = validated_data.pop('reg'),
            profile_pic = validated_data.pop('profile_pic'),
            session = validated_data.pop('session'),
            full_name = validated_data.pop('full_name'),
            fathers_name = validated_data.pop('fathers_name'),
            mothers_name = validated_data.pop('mothers_name'),
            mobile_no = validated_data.pop('mobile_no')

        )


        return student
    

    # def create(self, validated_data):
    #     user_data = validated_data.pop('user')
    #     user_info = CustomUserSerializer.create(CustomUserSerializer(), validated_data=user_data)
    #     # print(user.id)

    #     reg = validated_data.pop('reg'),
    #     profile_pic= validated_data.pop('profile_pic')
    #     full_name = validated_data.pop('full_name')
    #     fathers_name = validated_data.pop('fathers_name')
    #     mothers_name = validated_data.pop('mothers_name')
    #     mobile_no = validated_data.pop('mobile_no')
    #     session = validated_data.pop('session')

    #     student , created = StudentDetail.objects.update_or_create(
    #         user=user_info,
    #         reg = reg,
    #         profile_pic= profile_pic,
    #         full_name = full_name,
    #         fathers_name = fathers_name,
    #         mothers_name = mothers_name,
    #         mobile_no = mobile_no,
    #         session = session

    #     )
    #     return student
        

class StudentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentDetail
        fields = '__all__'


class LoginSerializer(serializers.Serializer):
    roll = serializers.CharField()
    password = serializers.CharField(write_only=True,style={'input_type': 'password'},)

    def validate(self, attrs):
        roll = attrs.get('roll')
        password = attrs.get('password')

        if roll and password:
            user = CustomUser.objects.filter(roll=roll).first()
            if user is None:
                user = CustomUser.objects.filter(email=roll).first()
                if user is None:
                    msg = 'Email or Roll not found'
                    raise serializers.ValidationError(msg, code='authorization')

            if check_password(password,user.password):
                attrs['user'] = user
                return attrs
            else:
                msg = 'Password is incorrect'
                raise serializers.ValidationError(msg, code='authorization')

        else:
            msg = 'Must include Email or Roll and Password'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
    

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        # fields = ['course_code','course_credit','course_title']
        fields = '__all__'

class FormFillUpSerializer(serializers.ModelSerializer):
    course = CourseSerializer(many=True,read_only = True)
    class Meta:
        model = FormFillUp
        fields = "__all__"