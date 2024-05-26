from django import forms
from .models import Excel


# class NewInputForm(forms.ModelForm):
#     class Meta:
#         model = Input
#         fields = ('date',
#                   'invoice_number',
#                   'value',
#                   'haircut',
#                   'daily_fee',
#                   'currency',
#                   'revenue_src',
#                   'customer',
#                   'expected_payment_duration')


class NewExcelImport(forms.ModelForm):
    """
    HTML form to upload excel files in frontend
    """
    class Meta:
        model = Excel
        fields = ('file',)
