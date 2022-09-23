from django import forms
from django.forms import ModelForm
from .models import Project, Image, ReviewRating

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        exclude = ('created_by', 'is_featured', 'project_review_ratio')
    
    def clean_project_end_date(self):
        start_date = self.cleaned_data.get('project_start_date')
        end_date = self.cleaned_data.get('project_end_date')
        if (not (end_date is None or start_date is None)) and  end_date < start_date:
            raise forms.ValidationError('Ending date has to be after starting date.')
        return end_date

class ImageForm(forms.ModelForm):
    image = forms.ImageField(
        label="Image",
        widget=forms.ClearableFileInput(attrs={"multiple": True}),
    )

    class Meta:
        model = Image
        fields = ("image",)

class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ['rating']