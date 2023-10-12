from django import forms

from .models import ConversationMessage

class ConversationMessageForm(forms.ModelForm):
    class Meta:
        model = ConversationMessage
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'w-full py-2 px-3 rounded-xl border',
                'style': 'height: 80px;'  # Adjust the height as needed
            })
        }