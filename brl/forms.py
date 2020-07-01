from django import forms


class T2BForm(forms.Form):
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "id": "message",
                "placeholder": "Input TEXT here... ",
            }
        )
    )


class B2TForm(forms.Form):
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "id": "message",
                "placeholder": "Input BRAILLE here... ",
            }
        )
    )
