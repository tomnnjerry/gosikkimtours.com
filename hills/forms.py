from django import forms

from .content import MONTHS, catalogue
from .models import Enquiry


class EnquiryForm(forms.ModelForm):
    lands = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple)
    month = forms.ChoiceField(required=False)
    website = forms.CharField(required=False, widget=forms.HiddenInput)  # honeypot

    class Meta:
        model = Enquiry
        fields = ["name", "email", "phone", "contact_pref", "lands", "month", "nights", "travellers", "budget", "message", "source_page", "kind"]
        widgets = {
            "message": forms.Textarea(attrs={"rows": 5}),
            "source_page": forms.HiddenInput,
            "kind": forms.HiddenInput,
            "contact_pref": forms.RadioSelect,
            "budget": forms.Select(choices=[
                ("", "Choose a tier"), ("budget", "Budget: homestays, shared jeeps where possible"),
                ("value", "Value: good hotels, private car"), ("comfort", "Comfort: the best rooms on the route"),
                ("mixed", "Mix: cheap nights, one or two good hotels"), ("unsure", "Not sure yet")]),
        }
        labels = {"phone": "Phone or WhatsApp", "nights": "Nights (roughly)", "message": "Tell us about the trip", "lands": "Where would you like to go?"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        cat = catalogue()
        self.fields["lands"].choices = [(r["slug"], r["name"]) for r in cat.regions.values()]
        self.fields["month"].choices = [("", "Flexible")] + [(m, m) for m in MONTHS]
        self.fields["kind"].required = False
        self.fields["contact_pref"].choices = Enquiry._meta.get_field("contact_pref").choices
        self.fields["contact_pref"].required = False

    def clean_kind(self):
        return self.cleaned_data.get("kind") or "full"

    def clean_lands(self):
        return ", ".join(self.cleaned_data.get("lands") or [])

    def clean(self):
        data = super().clean()
        if data.get("website"):
            raise forms.ValidationError("Spam detected.")
        return data


class SubscribeForm(forms.Form):
    email = forms.EmailField()
    source_page = forms.CharField(required=False, max_length=300)
    website = forms.CharField(required=False)  # honeypot
