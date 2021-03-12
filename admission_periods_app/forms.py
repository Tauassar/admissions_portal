from django.forms import ModelForm
from admission_periods_app.models import AdmissionRoundModel


class AdmissionRoundForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['threshold'].required = True

    class Meta:
        model = AdmissionRoundModel
        fields = ['threshold']
