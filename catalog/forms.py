from django.forms import ModelForm
from .models import BookInstance
import datetime

class RenewBookForm(ModelForm):
    class Meta:
        model = BookInstance
        fields = ['due_back']
        labels = {'due_back': 'Renewal date'}
        help_texts = {'due_back': 'Enter a date between now and 4 weeks.'}