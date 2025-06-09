from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30, required=True, label='Имя')
    last_name = forms.CharField(max_length=30, required=True, label='Фамилия')
    phone = forms.CharField(max_length=20, required=True, label='Телефон')
    role = forms.ChoiceField(
        choices=[('client', 'Клиент'), ('master', 'Мастер')],
        label='Роль',
        initial='client',
        widget=forms.RadioSelect
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone', 'role', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = self.cleaned_data['role']
        if commit:
            user.save()
            # Если пользователь регистрируется как мастер, создаем для него профиль мастера
            if user.role == 'master':
                from services.models import Master
                Master.objects.create(
                    user=user,
                    name=f"{user.first_name} {user.last_name}",
                    description="",
                    experience=0
                )
        return user

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone']
