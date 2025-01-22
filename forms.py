from django import forms

class CompanySearchForm(forms.Form):
    company_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Search for a company...'}),
        error_messages={
            'required': 'Please enter a company name.',
            'max_length': 'Company name cannot exceed 100 characters.'
        }
    )

    def clean_company_name(self):
        company_name = self.cleaned_data.get('company_name')
        if not company_name.isalpha():
            raise forms.ValidationError("Company name should only contain alphabetic characters.")
        return company_name
