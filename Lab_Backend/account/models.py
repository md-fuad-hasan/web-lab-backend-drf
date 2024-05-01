from django.db import models
from django.contrib.auth import password_validation
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, email,roll, password=None):
        if not email:
            raise ValueError('Email must be needed')
        
        email = self.normalize_email(email)
        user = self.model(email=email,roll=roll)
        
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self,email,roll,password=None):
        email= self.normalize_email(email)
        user = self.create_user(email=email,roll=roll,password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using = self._db) 

        return user


class CustomUser(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    roll = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['roll']

    def __str__(self):
        if self.roll:
            return self.roll
        return self.email
    
    def get_group_permissions(obj=None):
        return obj
    

def profile_pic_uploaded(instance,filename):
    return 'uploads\{user}\{filename}'.format(user=instance.user.roll,filename=filename)


class StudentDetail(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE,related_name='student')
    reg = models.CharField(max_length=50, blank=True)
    profile_pic = models.ImageField(upload_to=profile_pic_uploaded, default="default.jpg", blank=True, null=True)
    full_name = models.CharField(max_length=255, blank=True)
    fathers_name = models.CharField(max_length=255, blank=True)
    mothers_name = models.CharField(max_length=255, blank=True)
    mobile_no = models.CharField(max_length = 255, blank=True)
    session = models.CharField(max_length=10,blank=True)

    def __str__(self):
        if self.user.roll:
            return self.user.roll
        return self.user.email


# @receiver(post_save, sender=CustomUser)
# def create_account_detail(sender, instance, created, **kwargs):
#     if created:
#         StudentDetail.objects.create(user = instance)

# @receiver(post_save, sender=CustomUser)
# def save_account_detail(sender, instance, **kwargs):
#     instance.student.save()


ACADEMIC_YEAR = [
    ('2018-19','2018-19'),
    ('2019-20','2019-20'),
    ('2020-21','2020-21'),
    ('2021-22','2021-22'),
    ('2022-23','2022-23'),
]

class Course(models.Model):
    semester = models.CharField(max_length=5)
    course_code = models.CharField(max_length=10)
    course_credit = models.FloatField()
    course_title = models.CharField(max_length=255)
    session = models.CharField(max_length=10,choices=ACADEMIC_YEAR, default = '2018-19')

    def __str__(self):
        return self.session+" - "+ self.course_code+" "+ self.course_title
    

STATUS = [
    ('C','Collegiate'),
    ('N','Non-Collegiate'),
    ('I','Improvement'),
]

YEAR = [
    ('Part-1','Part-1'),
    ('Part-2','Part-2'),
    ('Part-3','Part-3'),
    ('Part-4','Part-4'),
]

SEMESTER = [
    ('Odd','Odd'),
    ('Even','Even'),
]

class FormFillUp(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user')
    course = models.ManyToManyField(Course, related_name='course')
    student_type = models.CharField(max_length=20,choices=[('Regular','Regular'),('Improvement','Improvement')])
    student_status = models.CharField(max_length=50, choices=STATUS)
    previous_exam = models.CharField(max_length=3, choices=[("Yes","Yes"),("No","No")])
    previous_exam_year = models.CharField(max_length=4)

    year = models.CharField(max_length=10, choices=YEAR)
    semester = models.CharField(max_length=5, choices=SEMESTER)
    academic_year = models.CharField(max_length=5)
    start = models.DateField()
    end_without_fine = models.DateField()
    end_with_fine = models.DateField()
    exam_date = models.DateField()
    complete = models.BooleanField(default=False)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return self.user.roll + ' '+self.year+" - "+self.semester + self.academic_year + self.student_type
