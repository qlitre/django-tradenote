from django import forms
from .models import History, Transaction


class TransactionSearchForm(forms.Form):
    """取引検索フォーム。"""
    key_word = forms.CharField(
        label='検索キーワード',
        required=False,
        widget=forms.TextInput(attrs={'autocomplete': 'off',
                                      'class': 'form-control',
                                      })
    )


class HistoryCreateForm(forms.ModelForm):
    """売買履歴追加フォーム"""

    class Meta:
        model = History
        exclude = ('amount', 'target',)

        widgets = {
            'date_trade': forms.TextInput(attrs={'autocomplete': 'off',
                                                 'placeholder': 'date',
                                                 'class': 'form-control'}),
            'trading_category': forms.Select(attrs={'class': 'form-select'}),
            'price': forms.TextInput(attrs={'autocomplete': 'off',
                                            'placeholder': 'price',
                                            'class': 'form-control'}),
            'quantity': forms.TextInput(attrs={'autocomplete': 'off',
                                               'placeholder': 'quantity',
                                               'class': 'form-control'}),
            'commission': forms.TextInput(attrs={'autocomplete': 'off',
                                                 'placeholder': 'commission',
                                                 'class': 'form-control'}),
        }


class TransactionCreateForm(forms.ModelForm):
    """取引追加フォーム"""

    class Meta:
        model = Transaction
        fields = '__all__'
        widgets = {
            'reason': forms.Textarea(attrs={'rows': '3'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
            field.widget.attrs["autocomplete"] = "off"
