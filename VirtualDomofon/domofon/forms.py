# forms.py
from django import forms
from .models import DomofonCall

class DomofonCallForm(forms.ModelForm):
    class Meta:
        model = DomofonCall
        fields = ['mac_address', 'apartment_number', 'is_active']
        widgets = {
            'mac_address': forms.TextInput(attrs={
                'placeholder': 'Нажмите кнопку генерации',
                'id': 'id_mac_address'
            }),
            'apartment_number': forms.NumberInput(attrs={'min': 1}),
        }
        labels = {
            'apartment_number': 'Номер квартиры',
            'is_active': 'Домофон включен',
        }