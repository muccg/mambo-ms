from django import forms


class PasswordChangeForm(forms.Form):
    token = forms.CharField(widget=forms.HiddenInput, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    confirm = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        password = self.cleaned_data.get("password", None)

        if not password:
            raise forms.ValidationError("A password must be provided.")
        elif password != self.cleaned_data.get("confirm", None):
            raise forms.ValidationError("The passwords do not match.")

        return self.cleaned_data

class PasswordResetForm(forms.Form):
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True, label="E-mail address")
