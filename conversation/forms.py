from django import forms

from .models import ConversationMessage

class ConversationMessageForm(forms.ModelForm):
    class Meta:
        model = ConversationMessage
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={
<<<<<<< HEAD
                'class': 'w-full py- n4 px-6 rounded-xl border'
=======
                'class': 'w-full py-2 px-3 rounded-xl border'
>>>>>>> 90a58ff66c0c27164252a7d66d271a57b35d8555
            })
        }