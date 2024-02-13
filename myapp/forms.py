from django import forms
from .models import UserProfile, HealthRecord, WebLink, Entry, DailyWeight


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