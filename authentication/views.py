from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from .forms import RegisterForm
from django.contrib.auth.models import Group

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data.get("email")  # lưu email
            user.save()

            # gán Reader mặc định
            from django.contrib.auth.models import Group
            reader_group = Group.objects.get(name="Reader")
            user.groups.add(reader_group)

            login(request, user)
            messages.success(request, "Đăng ký thành công! Bạn đã được gán quyền Reader.")
            return redirect("home")
    else:
        form = RegisterForm()
    return render(request, "authentication/register.html", {"form": form})



def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser or user.is_staff:
                return redirect("admin_dashboard") 
            return redirect("home") 
        else:
            messages.error(request, "Sai tài khoản hoặc mật khẩu")
    return render(request, "authentication/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")
