from django import forms
from .models import UserProfile, HealthRecord, WebLink, Entry, DailyWeight
from django.contrib.auth.forms import UserCreationForm
from .models import UserCredentials, UserProfile
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.contrib.auth.models import User 

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['height', 'target', 'exercise_goal']

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['exercise_goal'].widget.attrs['class'] = 'exercise-goal-input'
        #self.fields['height'].help_text = 'メートル入力でお願いします。例）160cmの方：1.60'
        


class HealthRecordForm(forms.ModelForm):
    class Meta:
        model = HealthRecord
        fields = ['sleep_hours', 'physical_condition', 'stress_level', 'hydration_amount', 'breakfast_content', 'lunch_content', 'dinner_content', 'other_meal_content','training_content']
        widgets = {
               'hydration_amount': forms.NumberInput(attrs={'min': 0}),
        }
        labels = {
            'date': '日付',
            'sleep_hours': '睡眠時間',
            'physical_condition': '体調',
            'stress_level': 'ストレスレベル',
            'hydration_amount': '水分摂取量',
            'meal_content': '食事内容',
            'training_content': 'トレーニング内容',
        }

class WebLinkForm(forms.ModelForm):
    class Meta:
        model = WebLink
        fields = ['url']

    def clean_url(self):
        url = self.cleaned_data['url']
        # ここでカスタムバリデーションを追加することができます
        return url
    

class EntryForm(forms.ModelForm):
    description = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '新規コメントはこちら', 'required': True}))

    class Meta:
        model = Entry
        fields = ['description']

class DailyWeightForm(forms.ModelForm):
    class Meta:
        model = DailyWeight
        fields = ['weight']
        labels = {
            'weight': '体重',
        }

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label='ユーザー名',
        validators=[
            RegexValidator(
                regex='^[a-zA-Z0-9]*$',
                message='ユーザー名は半角英数字で入力してください。記号は含めないでください。',
                code='invalid_username'
            ),
        ],
        help_text='半角英数字であること、記号は含まないこと。'
    )
    
    # パスワードのバリデーションルールを定義
    password1 = forms.CharField(
        label='パスワード',
        widget=forms.PasswordInput,
        validators=[
            RegexValidator(
                regex='^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$',
                message='パスワードは8文字以上で、大文字小文字数字を含む必要があります。',
                code='invalid_password'
            ),
        ],
        help_text='大文字小文字数字を含む８文字以上であること。'
    )

   
    height = forms.FloatField(
        label='身長',
        required=False, 
        help_text='半角数字でメートル単位で入力してください。例: 1.70'
        )
    weight = forms.FloatField(
        label='体重',
        required=False,
        help_text='半角数字でキログラム単位で入力してください。'
        )

    class Meta:
        model = User
        fields = ('username', 'height', 'weight')  # 必要なフィールドを追加
    
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # UserProfileが既に存在しない場合のみ作成
            UserProfile.objects.get_or_create(user=user)
        return user
    