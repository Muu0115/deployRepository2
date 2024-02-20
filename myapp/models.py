from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, User
from django.contrib.auth import get_user_model
from datetime import datetime
from django.utils import timezone
from datetime import date
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta


User = get_user_model()

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, password, **extra_fields)

class UserCredentials(AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True)
    password_hash = models.CharField(max_length=128)

    # 他に必要なフィールドがあれば追加

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username

class SessionTokens(models.Model):
    token_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    expiry_date = models.DateTimeField()

def __str__(self):
        return f"Token: {self.token} - User: {self.user.username}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    target = models.CharField(max_length=255, default="未設定")  # ユーザーの目標を保存するフィールド
    height = models.FloatField(null=True, blank=True)  # 身長（メートル単位）
    weight = models.FloatField(null=True, blank=True)  # 体重（キログラム単位）
    exercise_goal = models.TextField(null=True, blank=True)  # 運動目標


    def calculate_bmi(self):
        if self.height and self.weight:
            return self.weight / (self.height ** 2)
        return None

class HealthRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    sleep_hours = models.CharField(max_length=5, blank=True, null=True)
    CONDITION_CHOICES = [(i, str(i)) for i in range(1, 6)]
    physical_condition = models.IntegerField(choices=CONDITION_CHOICES, null=True, blank=True)
    stress_level = models.IntegerField(choices=CONDITION_CHOICES, null=True, blank=True)
    hydration_amount = models.IntegerField(null=True, blank=True)
    breakfast_content = models.TextField(blank=True, null=True)  
    lunch_content = models.TextField(blank=True, null=True)      
    dinner_content = models.TextField(blank=True, null=True)     
    other_meal_content = models.TextField(blank=True, null=True) 
    training_content = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Health Record for {self.user.get_username()} on {self.date}"
    
class WebLink(models.Model):
    # 既存のフィールド
    title = models.CharField(max_length=255)
    url = models.URLField()
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    purpose = models.CharField(max_length=255, blank=True)  # 動画の目的や用途
    tags = models.CharField(max_length=255, blank=True)     # 動画に関連するタグ

    def __str__(self):
        return f"{self.title} - {self.purpose}"
    
    class Meta:
        permissions = [
            ('can_view_weblink', 'Can view web link'),
            # 他のカスタムパーミッションがあれば追加
        ]


class GuestBookEntry(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    description = models.TextField()

class Entry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)  # 追加

class Reply(models.Model):
    entry = models.ForeignKey(Entry, related_name='replies', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

class DailyWeight(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=date.today)
    weight = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        unique_together = ('user', 'date')

class UserRewards(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    last_login_date = models.DateField(auto_now_add=True)
    continuous_weeks = models.IntegerField(default=0)
    continuous_months = models.IntegerField(default=0)

    def update_login_streak(self):
        today = timezone.now().date()
        last_login = self.last_login_date

        if last_login:
            # 前回のログインが今日から1日前であるかをチェック
            if last_login == today - timedelta(days=1):
                # 週数と月数のカウントアップ
                # 以下は単純な例です
                self.continuous_days += 1
                self.continuous_weeks = self.continuous_days // 7
                self.continuous_months = self.continuous_days // 30
            else:
                # 連続ログインが途切れた場合、カウンタをリセット
                self.continuous_days = 0
                self.continuous_weeks = 0
                self.continuous_months = 0

        self.last_login_date = today
        self.save()


@receiver(post_save, sender=User)
def create_user_rewards(sender, instance, created, **kwargs):
    if created:
        UserRewards.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_rewards(sender, instance, **kwargs):
    instance.userrewards.save()