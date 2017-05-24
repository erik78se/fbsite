from django import forms

# Form for registering FaceBook events
class FaceBookEventForm(forms.Form):
    facebook_event_id = forms.CharField(label='Facebook Event ID (123123)', max_length=24)
