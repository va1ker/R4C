from django import forms


class RobotCreateForm(forms.Form):
    model = forms.CharField(max_length=2, required=True)
    version = forms.CharField(max_length=2, required=True)
    created = forms.DateTimeField(input_formats=["%Y-%m-%d %H:%M:%S"], required=True)
