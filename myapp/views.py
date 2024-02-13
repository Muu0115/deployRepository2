from datetime import datetime
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import UserProfile, HealthRecord, Entry, Reply, DailyWeight, WebLink
from .forms import UserProfileForm, HealthRecordForm, WebLinkForm, EntryForm, DailyWeightForm
from datetime import datetime, date
from decimal import Decimal
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required




# signup ビューは signup.html テンプレートを表示します
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect('home')  # ホームページへリダイレクト
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

# SignUpViewクラスはユーザー登録用のビューを定義します
class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')  # ログインページへリダイレクト
    template_name = 'signup.html'

    # form_validメソッドはフォームが有効な場合に呼び出されます
    def form_valid(self, form):
        response = super(SignUpView, self).form_valid(form)  # 親クラスのform_validメソッドを呼び出し
        UserProfile.objects.create(user=self.object)  # type: ignore # ユーザープロファイルを作成
        return response

@login_required
def manage_health_record(request, year, month, day):
    # URLから日付を取得
    record_date = datetime(year=year, month=month, day=day)

    try:
        # 既存の記録を取得、なければ新規作成
        health_record = HealthRecord.objects.get(user=request.user, date=record_date)
    except HealthRecord.DoesNotExist:
        health_record = None

    if request.method == 'POST':
        form = HealthRecordForm(request.POST, instance=health_record)
        if form.is_valid():
            new_record = form.save(commit=False)
            new_record.user = request.user
            new_record.date = record_date
            new_record.save()
            return redirect('home')
    else:
        form = HealthRecordForm(instance=health_record)

    return render(request, 'health_record/health_record.html', {
        'form': form,
        'record_date': record_date.strftime('%Y-%m-%d')
    })

def health_record(request, year, month, day):
    record_date = datetime(year=year, month=month, day=day)
    try:
        health_record = HealthRecord.objects.get(user=request.user, date=record_date)
    except HealthRecord.DoesNotExist:
        health_record = None

    if request.method == 'POST':
        form = HealthRecordForm(request.POST, instance=health_record)
        if form.is_valid():
            new_record = form.save(commit=False)
            new_record.user = request.user
            new_record.date = record_date
            new_record.save()
            return redirect('home')
    else:
        form = HealthRecordForm(instance=health_record)

    return render(request, 'health_record/health_record.html', {
        'form': form,
        'record_date': record_date.strftime('%Y-%m-%d')
    })

@staff_member_required
def add_weblink(request):
    # 管理者かどうかをチェックする
    if not request.user.is_staff:
        return HttpResponse('Unauthorized', status=401)

    if request.method == 'POST':
        form = WebLinkForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_weblink')
    else:
        form = WebLinkForm()
    return render(request, 'weblink/weblink.html', {'form': form})

def weblink_detail(request, pk):
    weblink = get_object_or_404(WebLink, pk=pk)
    return render(request, 'weblink/detail.html', {'weblink': weblink})

def weblink_list(request):
    links = WebLink.objects.all()  
    return render(request, 'weblink/weblink.html', {'links': links}) 


def guestbook(request):
    if request.method == 'POST':
        # 返信の処理
        if 'reply_text' in request.POST:
            reply_text = request.POST['reply_text']
            entry_id = request.POST['entry_id']
            entry = Entry.objects.get(id=entry_id)
            reply = Reply(user=request.user, entry=entry, description=reply_text)
            reply.save()
            return redirect('guestbook')

        # エントリーの投稿処理
        else:
            form = EntryForm(request.POST)
            if form.is_valid():
                entry = form.save(commit=False)
                entry.user = request.user
                entry.save()
                return redirect('guestbook')
    else:
        form = EntryForm()

    entries = Entry.objects.all()
    return render(request, 'guestbook/guestbook.html', {'form': form, 'entries': entries})

def home(request):
    if not request.user.is_authenticated:
        return redirect('login')  # ログインしていないユーザーをログインページにリダイレクト

    form = DailyWeightForm()
    bmi = None
    target = None  # ユーザーの目標を初期化

    if request.method == 'POST':
        form = DailyWeightForm(request.POST)
        if form.is_valid():
            # ユーザーと今日の日付でフィルタリングします
            daily_weight, created = DailyWeight.objects.get_or_create(
                user_id=request.user.id,
                date=timezone.now().date(),
                defaults={'weight': form.cleaned_data['weight']}
            )
            if not created:
                # 既存のレコードを更新します
                daily_weight.weight = form.cleaned_data['weight']
                daily_weight.save()

    try:
        profile = request.user.userprofile
        target = profile.target  # 'target'フィールドをUserProfileモデルに追加してください
        if profile.height:
            height_m = Decimal(profile.height) / 100  # cmからmへ変換
            today_weight = DailyWeight.objects.filter(user=request.user, date=date.today()).first()
            if today_weight:
                bmi = today_weight.weight / (height_m ** 2)
                bmi = round(bmi, 2)
    except UserProfile.DoesNotExist:
        profile = None  # プロファイルが存在しない場合

    # 新しく追加する部分：身長をJavaScriptで使えるようにする
    height_for_js = None
    if profile:
        height_for_js = profile.height

    context = {
        'form': form,
        'bmi': bmi,
        'profile': profile,
        'height_for_js': height_for_js,  # JavaScriptで使えるように身長を渡す
        'target': target,  # 新しく追加
    }

    return render(request, 'home/home.html', context)

def mypage(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            # 保存後、ホーム画面にリダイレクト
            return redirect('home')

    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'mypage/mypage.html', {'form': form})