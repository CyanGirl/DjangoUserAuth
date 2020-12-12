from django.contrib.auth.forms import UserCreationForm

#extending usercreationform
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        #adding the email field
        fields = UserCreationForm.Meta.fields + ("email",)