from django import forms

# Form for registering FaceBook events
class FaceBookEventForm(forms.Form):
    facebook_event_id = forms.CharField(label="Event ID: ", max_length=24 )
