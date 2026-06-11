from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from students.models import Student

User = get_user_model()

class StudentRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Электронная почта')
    first_name = forms.CharField(max_length=30, required=True, label='Имя')
    last_name = forms.CharField(max_length=30, required=True, label='Фамилия')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким email уже зарегистрирован.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'student'
        user.email = self.cleaned_data['email']  # уже проверен
        if commit:
            user.save()
            # Автоматически создаём профиль Student
            Student.objects.create(user=user, student_id=f"STU{user.id}", group="Не указана")
        return user