from django.contrib import admin
from .models import *
# Register your models here.

admin.site.site_header='Medical management'
admin.site.register(Ponto)
admin.site.register(User)
admin.site.register(Paciente)
admin.site.register(BancoUrgencia)
admin.site.register(Atendete)
admin.site.register(Receita)
admin.site.register(ReceitaMedicamento)
admin.site.register(Medicamento)
admin.site.register(Medico)
admin.site.register(Consulta)
admin.site.register(Factura)
admin.site.register(Consultorio)
admin.site.register(Alocacao)
admin.site.register(ConsultaAgenda)
admin.site.register(MedicoEspecialista)
admin.site.register(Analise)
admin.site.register(ReceitaAnalise)