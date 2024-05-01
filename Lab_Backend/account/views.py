from .serializers import StudentSerializer,LoginSerializer,StudentDetailSerializer,CourseSerializer, FormFillUpSerializer,CustomUserSerializer
from .models import StudentDetail, Course,CustomUser,FormFillUp
# from drf_nested_field_multipart import NestedMultipartParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, parsers
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.http import Http404
from django.contrib.auth.models import update_last_login 
from rest_framework_simplejwt.tokens import RefreshToken

# from .parsers import MultiPartJSONParser

# from .utils import MultiPartJSONParser
from .parsers import MultipartJsonParser

# Create your views here.



class Register( APIView):
    parser_classes = [MultipartJsonParser, parsers.JSONParser]
    def get(self, request,fromat=None):
        student = StudentDetail.objects.all()
        serializer = StudentSerializer(student, many=True)

        return Response(serializer.data)

    def post(self, request, fromat=None):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            # serializer.create(validated_data=request.data)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


class LoginView(APIView):
    serializer_class = LoginSerializer
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            if user is None:
                return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)
            

            update_last_login(None, user)
            refresh = RefreshToken.for_user(user)
            return Response({
                'roll': user.roll,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },status=status.HTTP_200_OK)
        

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class DetailView(APIView):
    # permission_classes = [IsAuthenticated]
    def get_object(self, id):
        try:
            return StudentDetail.objects.get(user=id)
        except StudentDetail.DoesNotExist:
            raise Http404 
    
    def get(self, request, id, format=None):
        student = self.get_object(id)
        # if student.user == request.user:
        serializer = StudentDetailSerializer(student)
        return Response(serializer.data)
        # return Response({"errors":"That's an error occurs!"},status=status.HTTP_400_BAD_REQUEST)
    
    # def put(self, request, id, format=None):
    #     student = self.get_object(id)
    #     if student.user == request.user:
    #         serializer = StudentDetailSerializer(student, data=request.data)
    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response(serializer.data)
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     return Response({"errors":"That's an error occurs!"},status=status.HTTP_400_BAD_REQUEST)

 
class FormFillUpView(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self, id):
        try:
            return FormFillUp.objects.filter(user=id,complete=True)
        except FormFillUp.DoesNotExist:
            raise Http404 
    
    def get(self, request, id, format=None):
        formfillup = self.get_object(id)

        # if id == request.user:
        # print(request.user)
        # print(formfillup[0].user)
        if formfillup:
            if formfillup[0].user ==request.user:
                serializer = FormFillUpSerializer(formfillup, many=True)
                return Response(serializer.data)
        
        # return Response({'message':'Form Fillup not start yet'}, status=status.HTTP_404_NOT_FOUND)
        return Response({"message":"That's an error."}, status=status.HTTP_400_BAD_REQUEST)

 
class FormFillUpAllView(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self, id):
        try:
            return FormFillUp.objects.filter(user=id)
        except FormFillUp.DoesNotExist:
            raise Http404 
    
    def get(self, request, id, format=None):
        formfillup = self.get_object(id)
        # if id ==request.user:
        if formfillup:
            serializer = FormFillUpSerializer(formfillup, many=True)
            return Response(serializer.data)
        
        return Response({'message':'Form Fillup not start yet'}, status=status.HTTP_404_NOT_FOUND)
    # return Response({"message":"That's an error."}, status=status.HTTP_400_BAD_REQUEST)


class CourseView(APIView):

    def get(self, request, format=None):

        session = self.request.query_params.get('session')
        semester= self.request.query_params.get('semester')

        queryset = Course.objects.filter(session=session,semester=semester).order_by('course_code')
        serializer = CourseSerializer(queryset,many=True)
        return Response(serializer.data)


class FormFillUpCompleteView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, id):
        try:
            return FormFillUp.objects.get(id=id)
        except FormFillUp.DoesNotExist:
            raise Http404
    
    def get(self, request, id, format=None):
        form = self.get_object(id)
        if form.user == request.user:
            if form.complete==False:
                form.complete=True
                form.save()
                return Response({"message":"Form Fillup done"}, status=status.HTTP_200_OK)
        return Response({"message":"It's not possible"},status=status.HTTP_400_BAD_REQUEST)
