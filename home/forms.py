from django import forms
from .models import *

class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ['medico_id', 'paciente_id','tipo']

class ReceitaForm(forms.ModelForm):
    class Meta:
        model = Receita
        fields = ['medico_id', 'consulta_id','paciente_id','descricao']
        widgets = {
            'medicamento_id': forms.CheckboxSelectMultiple,
        }

class MedicoForm(forms.ModelForm):
    class Meta:
        model = Medico
        fields = ['nome', 'idade','nacionalidade','genero','profissao','descricao','especialidade','is_especialista','especialidade_agendamento','formacao','foto']

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['nome', 'idade','nacionalidade','genero','nif','profissao','descricao','foto']

class FacturaForm(forms.ModelForm):
    class Meta:
        model=Factura
        fields=['consulta_id','total','paciente_id']
class MedicamentoForm(forms.ModelForm):
    class Meta:
        model=Medicamento
        fields=['nome','especificacoes','recomendacoes','horario','tipo']

class ReceitaMedicamentoForm(forms.ModelForm):
    class Meta:
        model = ReceitaMedicamento
        fields = ['medicamento', 'dosagem','receita']



class EmailChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este email já está em uso.')
        return email
    

