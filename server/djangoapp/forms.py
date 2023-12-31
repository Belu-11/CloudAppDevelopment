from django import forms
from .models import CarModel


class ReviewForm(forms.Form):
    review = forms.CharField(label="Review", max_length=10000, widget=forms.Textarea(attrs={
                             "rows": 2, "class": "form-control", "id": "content", "name": "content", "placeholder": "Your review..."}), required=True)
    dealership = forms.IntegerField(widget=forms.HiddenInput())
    name = forms.CharField(widget=forms.HiddenInput())
    purchase = forms.BooleanField(
        label="Purchase", required=False, initial=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input", "id": "purchase", "name": "purchase"}))
    purchase_date = forms.DateField(label="Purchase Date", required=False, widget=forms.DateInput(format='%d/%m/%Y', attrs={
                                    "class": "date-own form-control", "id": "purchasedate", "name": "purchasedate", "type": "date"}))
    car = forms.ChoiceField(label="Car", required=True, widget=forms.Select(
        attrs={"class": "form-select", "id": "car", "name": "car"}))

    def __init__(self, *args, **kwargs):
        dealership = kwargs.pop("dealership")
        name = kwargs.pop("name")
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.fields["car"].choices = [("", "No car")] + [(car.pk, f"{car.name}-{car.make.name}-{car.year.year}")
                        for car in CarModel.objects.filter(dealer_id=dealership)]