from django import forms


class OrderForm(forms.Form):
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={"class": "form-control"}))
    robot_serial = forms.CharField(
        label="Robot serial number", max_length=5, widget=forms.TextInput(attrs={"class": "form-control"})
    )
