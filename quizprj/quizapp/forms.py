from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import gettext as _
from .models import Question, Choice

User = get_user_model()

class UserLoginForm(forms.Form):
    
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("This user does not exists")
            if not user.check_password(password):
                raise forms.ValidationError("Incorrect password")
            if not user.is_active:
                raise forms.ValidationError("This user is not active")
        return super(UserLoginForm, self).clean(*args, **kwargs)


class RegistrationForm(UserCreationForm):
    
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}), required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    is_staff = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
            'is_staff'
        ]

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.email = self.cleaned_data['is_staff']
    
        if commit:
            user.save()

        return user
    
    
    
    
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['qus_txt', 'is_published']
        widgets = {
            'qus_txt': forms.Textarea(attrs={'rows': 3, 'cols': 80}),
        }
        
        
class EditQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['qus_txt', 'is_published']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'cols': 20}),
        }


class ChoiceAddForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text', 'is_correct']
        widgets = {
            'choice_text': forms.Textarea(attrs={'rows': 2, 'cols': 80}),
            }
        
class ChoiceInlineFormset(forms.BaseInlineFormSet):
    def clean(self):
        super(ChoiceInlineFormset, self).clean()

        correct_choices_count = 0
        for form in self.forms:
            if not form.is_valid():
                return

            if form.cleaned_data and form.cleaned_data.get('is_correct') is True:
                correct_choices_count += 1

        try:
            assert correct_choices_count == Question.ALLOWED_NUMBER_OF_CORRECT_CHOICES
        except AssertionError:
            raise forms.ValidationError(_('Exactly one correct choice is allowed.'))