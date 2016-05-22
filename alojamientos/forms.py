from django import forms
from .models import Comentario

class ComentarioCreateForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ('title', 'body')
        labels = {
            'title':'Titulo',
            'body':'Texto'
            }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'})
        }
# Hacer: limpiar el formulario con cosas como que
# un alojamiento no tenga el mismo titulo de comentario
# etc

class BuscadorForm(forms.Form):
    CHOICES = []
    categoria = forms.ChoiceField(choices=CHOICES, required=True)
    texto = forms.CharField(min_length=5, widget=forms.TextInput(attrs={'class':'form-control'}))

    def __init__(self, custom_choices=None, *args, **kwargs):
        super(BuscadorForm, self).__init__(*args, **kwargs)
        if custom_choices:
            self.fields['categoria'].choices = custom_choices