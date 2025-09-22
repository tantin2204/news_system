from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                "class": "form-input"
            })
        self.fields["username"].widget.attrs["placeholder"] = "Tên đăng nhập"
        self.fields["email"].widget.attrs["placeholder"] = "Địa chỉ email"
        self.fields["password1"].widget.attrs["placeholder"] = "Mật khẩu"
        self.fields["password2"].widget.attrs["placeholder"] = "Xác nhận mật khẩu"

