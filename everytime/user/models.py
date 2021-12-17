from django.db import models

# Create your models here.
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin, UserManager
from django.utils import timezone

from university.models import University
from department.models import Department

class CustomUserManager(BaseUserManager):
    # CustomUserManager 가 위에 임포트해두고 쓰지 않는 UserManager 와 어떻게 다른지 파악하면서 보시면 좋을 것 같습니다.
    # 이메일 기반으로 인증 방식을 변경하기 위한 구현입니다.

    use_in_migrations = True

    def _create_user(self, ID, password, **extra_fields):
        if not ID:
            raise ValueError('아이디를 설정해주세요.')

        extra_fields['email'] = self.normalize_email(extra_fields['email'])
        user = self.model(ID=ID, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, ID, password=None, **extra_fields):

        # setdefault -> 딕셔너리에 key가 없을 경우 default로 값 설정
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(ID, password, **extra_fields)

    def create_superuser(self, ID, password, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True or extra_fields.get('is_superuser') is not True:
            raise ValueError('권한 설정이 잘못되었습니다.')

        return self._create_user(ID, password, **extra_fields)




class User(AbstractBaseUser, PermissionsMixin):
    objects = CustomUserManager()

    university = models.ForeignKey(University, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    ID = models.CharField(max_length=30, blank=False, db_index=True)
    email = models.EmailField(max_length=100, unique=True)
    admission_year = models.IntegerField()
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(default=timezone.now)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    # 해당 필드에 대한 설명은 부모 AbstractBaseUser 클래스 참고
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'ID'

    def __str__(self):
        return self.ID

    def get_short_name(self):
        return self.ID
