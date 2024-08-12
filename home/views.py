from django.shortcuts import render,redirect, get_object_or_404
from .models import *
from .forms import *
from django.views.generic import CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
import io
from django.http import HttpResponse
from django.template.loader import get_template
from django.core.paginator import Paginator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Q
from django.utils import timezone
from apscheduler.schedulers.background import BackgroundScheduler
from .forms import EmailChangeForm
from datetime import datetime,date
import uuid
import qrcode

# Create your views here.
from django.http import JsonResponse
from .forms import *
def home(request):
    return render(request,'home/home.html')


def form_modal(request):
    if request.method == 'POST':
        form = ReceitaForm(request.POST)
        if form.is_valid():
            
            return JsonResponse({'success': True, 'message': 'Form submitted successfully!'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    else:
        form = ReceitaForm()
    if request.htmx:
        return render(request, 'home/form_modal.html', {'form': form})
    else:
        return render(request, 'home/home.html', {'form': form})
@login_required
def pacientelist(request):
    if request.user.is_authenticated:
        if request.user.is_admin or request.user.is_atendente:
            paciente=Paciente.objects.all()
            paciente_paginator=Paginator(paciente,4)
            page_num=request.GET.get('page')
            page=paciente_paginator.get_page(page_num)
            pedidos=ConsultaAgenda.objects.filter(status='pendente').all()

            total=pedidos.count()
            
            atendente=Atendete.objects.filter(nome__iexact=request.user.username).first()
            consultas=Consulta.objects.all()
            n1=len(consultas)
            lista=list()
            for n in range(0,4):
                lista.append(consultas[n1-1])
            context={
                'pacientes':paciente,
                'consultas':lista,
                'atendentes':atendente,
                'page':page,
                'user':request.user,
                'total':total,
            }   

            return render(request,'home/paciente_list.html',context)
        return render(request, 'alert.html', {'message': 'Você precisa ser um atendente ou medico para acessar esta página.', 'redirect_url': '/login/'})
    return render(request, 'alert.html', {'message': 'Você precisa estar logado para acessar esta página.', 'redirect_url': '/register/'})



def registro(request):
    if request.method == 'GET':
        return render(request, 'cadastro.html')
    else:
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        is_paciente = request.POST.get('is_paciente') == 'on'
        is_medico = request.POST.get('is_medico') == 'on'

        is_atendente=request.POST.get('is_atendente') == 'on'

        user = User.objects.filter(username=username).first()

        if user:
            return render(request, 'alert.html', {'message': 'Já existe um usuário com esse username.', 'redirect_url': '/register/'})
        if is_paciente and is_medico or is_atendente and is_paciente or is_atendente and is_medico:
            return render(request, 'alert.html', {'message': 'Selecione apenas um campo.', 'redirect_url': '/register/'})

        if is_paciente:
            paciente = Paciente.objects.filter(nome=username).first()
            if not paciente:
                return render(request, 'alert.html', {'message': 'Não existe um paciente com esse username.', 'redirect_url': '/register/'})

        if is_medico:
            medico = Medico.objects.filter(nome=username).first()
            if not medico:
                return render(request, 'alert.html', {'message': 'Não existe um medico com esse username.', 'redirect_url': '/register/'})
        if is_atendente:
            atendente = Atendete.objects.filter(nome=username).first()
            if not atendente:
                return render(request, 'alert.html', {'message': 'Não existe um atendente com esse username.', 'redirect_url': '/register/'})

        user = User.objects.create_user(username=username, email=email, password=senha)
        user.is_paciente = is_paciente
        user.is_medico = is_medico
        user.is_atendente=is_atendente
        user.save()

        

        return redirect('login')
    
@login_required
def logout_view(request):
    logout(request)
    return redirect('home')
def login_view(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            if request.user.is_admin:
                return redirect('paciente-list')
            elif request.user.is_paciente:
                return redirect('dashboard-paciente') 
            elif request.user.is_medico:
                return redirect('dashboard-medico') 
        return render(request, 'login.html')
    
    username = request.POST.get('username')
    senha = request.POST.get('senha')

    user = authenticate(request, username=username, password=senha)

    if user is not None:
        login_(request, user)
        return redirect('plataforma')
    else:
        return render(request, 'alert.html', {'message': 'Email ou senha incorretos.', 'redirect_url': '/login/'})
    
import hashlib

def gerar_codigo_unico(objeto):
    """Gera um código único baseado no hash SHA-256 da representação em string do objeto."""
    string_objeto = str(objeto)  # Assumindo que o objeto tem um método _str_
    hash_object = hashlib.sha256(string_objeto.encode('utf-8'))
    hex_dig = hash_object.hexdigest()
    return hex_dig[:12]  # Limitar para 12 caracteres

import re

def gerar_codigo_unico_numerico(codigo_unico):
    
    codigo_unico_numerico = re.sub(r'\D', '', codigo_unico)

    codigo_unico_numerico = str(int(codigo_unico_numerico)).zfill(12)

    return codigo_unico_numerico
class PacienteCreate(CreateView,LoginRequiredMixin):
    model=Paciente
    fields = ['nome', 'idade','nacionalidade','genero','nif','profissao','descricao','foto']
    success_url = reverse_lazy('home')
    def form_valid(self, form):
        paciente = form.cleaned_data['nome']
        paciente1 = form.save(commit=False)
        if Paciente.objects.filter(nome__iexact=paciente).exists():
            form.add_error(None, 'Esta paciente já existe.')
            return self.form_invalid(form)
        if self.request.user.is_admin:
            paciente1.save()
            return redirect('paciente-list')
        elif self.request.user.is_atendente:
            paciente1.save()
            return redirect('dashboard-atendente')
        
        return super().form_valid(form)
class PacienteUpdate(UpdateView,LoginRequiredMixin):
    model=Paciente
    fields = ['nome', 'idade','nacionalidade','genero','nif','profissao','descricao','foto']
    success_url = reverse_lazy('home')
    def form_valid(self, form):
        
        paciente1 = form.save(commit=False)
        
        if self.request.user.is_admin:
            paciente1.save()
            return redirect('paciente-list')
        elif self.request.user.is_atendente:
            paciente1.save()
            return redirect('dashboard-atendente')
        
        return super().form_valid(form)
class PacienteDelete(DeleteView,LoginRequiredMixin):
    model=Paciente
    success_url = reverse_lazy('paciente-list')
def medicolist(request):
    medicamento_paginator=Paginator(Medico.objects.all(),4)
    page_num=request.GET.get('page')
    page=medicamento_paginator.get_page(page_num)
    context={
        'medicos':Medico.objects.all(),
        'page':page,

    }
    return render(request,'home/medico_list.html',context)
class MedicoCreate(CreateView,LoginRequiredMixin):
    model=Medico
    fields = ['nome', 'idade','nacionalidade','genero','profissao','descricao','especialidade','is_especialista','especialidade_agendamento','formacao','foto']
    success_url = reverse_lazy('paciente-list')

    def form_valid(self, form):
        medico = form.cleaned_data['nome']
        if Medico.objects.filter(nome__iexact=medico).exists():
            form.add_error(None, 'Esta Medico já existe.')
            return self.form_invalid(form)
        return super().form_valid(form)
    
class MedicoUpdate(UpdateView,LoginRequiredMixin):
    model=Medico
    fields = ['nome', 'idade','nacionalidade','genero','profissao','descricao','especialidade','is_especialista','especialidade_agendamento','formacao','foto']
    success_url = reverse_lazy('home')

class MedicoDelete(DeleteView,LoginRequiredMixin):
    model=Medico
    success_url = reverse_lazy('home')
    
class ConsultaCreate(CreateView,LoginRequiredMixin):
    model=Consulta
    fields = ['medico_id', 'paciente_id','tipo','estado']
    success_url = reverse_lazy('receita-create')
    def form_valid(self, form):
        consulta = form.cleaned_data['estado']
        consulta1 = form.save(commit=False)
        if self.request.user.is_medico:
            return render(self.request, 'alert.html', {'message': 'Você não está autorizada a fazer esta operação.', 'redirect_url': '/consulta-create/'})

            

        if consulta == 'Pagamento' and self.request.user.is_atendente:
            return render(self.request, 'alert.html', {'message': 'Você não está autorizada a fazer esta operação.', 'redirect_url': '/consulta-create/'})

        elif consulta =='Realizada' and self.request.user.is_atendente:
            return render(self.request, 'alert.html', {'message': 'Você não está autorizada a fazer esta operação.', 'redirect_url': '/consulta-create/'})
        elif consulta == 'Pendente' and self.request.user.is_atendente:
            consulta1.save()
            return redirect('dashboard-atendente')
        elif consulta == 'Marcada' and self.request.user.is_atendente:
            consulta1.save()
            return redirect('dashboard-atendente')

        else:
            return render(self.request, 'alert.html', {'message': 'Você não está autorizada a fazer esta operação.', 'redirect_url': '/consulta-create/'})

     
        


class ConsultaUpdate(UpdateView,LoginRequiredMixin):
    model=Consulta
    fields = ['medico_id', 'paciente_id','tipo','estado']
    success_url = reverse_lazy('receita-create')

    def form_valid(self, form):
        consulta = form.cleaned_data['estado']
        paciente=form.cleaned_data['paciente_id']
        consulta1 = form.save(commit=False)
        
        if consulta == 'Pagamento' and self.request.user.is_medico:
            consulta1.save()
            paciente1=BancoUrgencia.objects.filter(paciente=paciente)
            
            paciente1.update(status='concluida')

            return redirect ('receita-create')
        elif consulta =='Realizada' and self.request.user.is_atendente:
            consulta1.save()
            return redirect('factura-create')
        elif consulta == 'Pendente' and self.request.user.is_medico:
            return render(self.request, 'alert.html', {'message': 'Você não está autorizada a fazer esta operação.', 'redirect_url': f'/consulta-update/{paciente.id}'})
        elif consulta == 'Marcada' and self.request.user.is_medico:
            return render(self.request, 'alert.html', {'message': 'Você não está autorizada a fazer esta operação.', 'redirect_url': f'/consulta-update/{paciente.id}'})

        else:
            return render(self.request, 'alert.html', {'message': 'Você não está autorizada a fazer esta operação.', 'redirect_url': f'/consulta-update/{paciente.id}'})

class ConsultaDelete(DeleteView,LoginRequiredMixin):
    model=Consulta
    success_url = reverse_lazy('home')


@login_required
def buscar_medicamentos(request):
    if 'q' in request.GET:
        query = request.GET.get('q')
        medicamentos = Medicamento.objects.filter(nome__icontains=query)
        results = [{'id': medicamento.id, 'nome': medicamento.nome} for medicamento in medicamentos]
        return JsonResponse(results, safe=False)
    return JsonResponse([], safe=False)
@login_required
def ReceitaCreate(request):
    if request.user.is_authenticated:
        if request.user.is_medico:
            if request.method == 'POST':
                receita_form = ReceitaForm(request.POST)
                if receita_form.is_valid():
                    receita = receita_form.save()
                    medicamentos_ids = request.POST.getlist('medicamentos')
                    dosagens = request.POST.getlist('dosagens')

                    
                    medicamentos_com_dosagem = set(zip(medicamentos_ids, dosagens))

                   
                    for medicamento_id, dosagem in medicamentos_com_dosagem:
                        try:
                            medicamento_id = int(medicamento_id)  
                            medicamento = Medicamento.objects.get(id=medicamento_id)
                            ReceitaMedicamento.objects.create(
                                receita=receita,
                                medicamento=medicamento,
                                dosagem=dosagem
                            )
                        except ValueError:
                            
                            print(f"O ID do medicamento '{medicamento_id}' não é um número válido.")
                        except Medicamento.DoesNotExist:
                           
                            print(f"O medicamento com ID {medicamento_id} não existe.")

                    return redirect('detalhe_receita', receita_id=receita.id)
            else:
                receita_form = ReceitaForm()

            return render(request, 'home/receita_form.html', {'receita_form': receita_form})
        
@login_required
def detalhe_receita(request, receita_id):
    if request.user.is_authenticated:
        if request.user.is_medico:
            receita = get_object_or_404(Receita, pk=receita_id)
            
            
            return render(request, 'home/receita_doc.html', {'receita': receita,'Medicamento':ReceitaMedicamento.objects.all(),'Medico':Medico.objects.filter(nome__iexact=request.user.username).first()})

@login_required
def gerar_receita_texto(request, receita_id):
    
    if request.user.is_authenticated:
        if request.user.is_medico:
            receita = get_object_or_404(Receita, id=receita_id)
            template = get_template('home/receita_texto.txt')
            context = {'receita': receita,'Medicamento':ReceitaMedicamento.objects.all()}
            content = template.render(context)

            response = HttpResponse(content, content_type='text/plain')
            response['Content-Disposition'] = 'attachment; filename="receita_{}.txt"'.format(receita.id)
            return response

class ReceitaUpdate(UpdateView,LoginRequiredMixin):
    model=Receita
    fields = ['medico_id', 'consulta_id','paciente_id','descricao']
    success_url = reverse_lazy('home')

class ReceitaDelete(DeleteView,LoginRequiredMixin):
    model=Receita
    
    success_url = reverse_lazy('home')

def facturalist(request):
    medicamento_paginator=Paginator(Factura.objects.all(),4)
    page_num=request.GET.get('page')
    page=medicamento_paginator.get_page(page_num)
    context={
        'facturas':Factura.objects.all(),
        'page':page
        
    }

    return render(request,'home/facturas_list.html',context)
class FacturaCreate(CreateView,LoginRequiredMixin):
    model=Factura
    fields=['consulta_id','total','paciente_id']
    success_url = reverse_lazy('dashboard-atendente')
    def form_valid(self, form):
        consulta = form.cleaned_data['consulta_id']
        consulta1=Consulta.objects.filter(pk=consulta.id).first()

        consulta1.estado='Realizada'
        consulta1.save()
        forme=form.save(commit=False)
        forme.save()
        return redirect('dashboard-atendente')


class FacturaUpdate(UpdateView,LoginRequiredMixin):
    model=Factura
    fields=['consulta_id','total','paciente_id']
    success_url = reverse_lazy('dashboard-atendente')

class FacturaDelete(DeleteView,LoginRequiredMixin):
    model=Factura
    success_url = reverse_lazy('dashboard-atendente')


def medicamentolist(request):
    
    medicamento_paginator=Paginator(Medicamento.objects.all(),4)
    page_num=request.GET.get('page')
    page=medicamento_paginator.get_page(page_num)
    context={
        'page':page,
        'medicamentos':Medicamento.objects.all(),

    }

    return render(request,'home/medicamentos_list.html',context)
class MedicamentoCreate(CreateView,LoginRequiredMixin):
    model=Medicamento
    fields=['nome','especificacoes','recomendacoes','horario','tipo']
    success_url = reverse_lazy('admin-dashboard')

    def form_valid(self, form):
        Medicamento = form.cleaned_data['nome']
        if Medicamento.objects.filter(nome__iexact=Medicamento).exists():
            form.add_error(None, 'Esta Medicamento já existe.')
            return self.form_invalid(form)
        return super().form_valid(form)
    
class MedicamentoUpdate(UpdateView,LoginRequiredMixin):
    model=Medicamento
    fields=['nome','especificacoes','recomendacoes','horario','tipo']
    success_url = reverse_lazy('medicamento-list')

class MedicamentoDelete(DeleteView,LoginRequiredMixin):
    model=Medicamento
    success_url = reverse_lazy('medicamento-list')

def plataforma(request):
    if request.user.is_authenticated:
        if request.user.is_medico:
            medico=Medico.objects.filter(nome__iexact=request.user.username).first()
            #if aluno:
            return redirect('dashboard-medico')
            #else:
                #return render(request, 'alert.html', {'message': 'Não existe nenhum aluno com este username .', 'redirect_url': ''})


        
           
            
        elif request.user.is_paciente:
            paciente=Paciente.objects.filter(nome__iexact=request.user.username).first()
            #if professor:
            return redirect('dashboard-paciente')
            #else:
                #return render(request, 'alert.html', {'message': 'Não existe nenhum professor com este username .', 'redirect_url': ''})
                #professor=Professor.objects.create(nome=request.user.username)
                #professor.save()
                #return redirect('home-professor')
        elif request.user.is_atendente:
            atendente=Atendete.objects.filter(nome__iexact=request.user.username).first()
            #if professor:
            return redirect('dashboard-atendente')

        elif request.user.is_admin:
            return redirect('paciente-list')
    return HttpResponse('erro')
@login_required
def especialistadash(request):
    if request.user.is_authenticated and request.user.is_medico:
        medico = Medico.objects.get(nome__iexact=request.user.username)
        
        if medico.is_especialista!=True:

            return render(request, 'alert.html', {'message': 'Você não está autorizada a fazer esta operação.', 'redirect_url': f'/login/'})
        data1=date.today()
        context={
            'medicos':medico,
            'consultas':ConsultaAgenda.objects.filter(Q(especielidade__iexact=medico.especialidade_agendamento) & Q(status__iexact='aceite') & Q(medico_id=medico) ).all()

        }
        return render(request,'dashboards/medico_especialista.html',context)

@login_required
def medicodash(request):
    if request.user.is_authenticated and request.user.is_medico:
        
        medico = Medico.objects.get(nome__iexact=request.user.username)
        
        if medico.is_especialista==True:

            return redirect('dashboard-especialista')

        try:
            paciente = BancoUrgencia.objects.filter(prioridade='alta',status='pendente').order_by('prioridade').first().paciente
            id=BancoUrgencia.objects.filter(prioridade='alta',status='pendente').order_by('prioridade').first()
        except:
            
                paciente=None
                id=None
        if paciente==None:
            try:
                paciente = BancoUrgencia.objects.filter(prioridade='media',status='pendente').order_by('prioridade').first().paciente
                id=BancoUrgencia.objects.filter(prioridade='media',status='pendente').order_by('prioridade').first()
                
            except:
                
                    paciente=None
                    id=None
        if paciente==None:
            try:
                paciente = BancoUrgencia.objects.filter(prioridade='baixa',status='pendente').order_by('prioridade').first().paciente
                id=BancoUrgencia.objects.filter(prioridade='baixa',status='pendente').order_by('prioridade').first()

            except:
                
                    paciente=None
                    id=None
        
        hora_agora = timezone.now()
        hora_limite = hora_agora + timezone.timedelta(minutes=30)
        consultorios_livres = Consultorio.objects.filter(
            Q(alocacao__isnull=True) | Q(alocacao__horario_fim__lte=hora_agora)
        )

        if consultorios_livres:
            consultorio = consultorios_livres.first()

            alocacao=Alocacao.objects.filter(medico=medico).first()

            

            
            
            try:
                paciente.status = 'em atendimento'
                paciente.save()
                consultorio.alocacao = alocacao
                consultorio.save()
            except:
                paciente=None

            try:
                n1=Consulta.objects.filter(paciente_id=paciente.id).last()
            except:
                n1=None
           
            context={
            'medicos':medico,
            'consul':n1,
            'consultas':BancoUrgencia.objects.filter(status='em atendimento').all(),
            'pontos':Ponto.objects.all(),
            'paciente':paciente,
            'alocamentos':Alocacao.objects.all(),
            'consultorio':consultorio,
            'id':id,
            }
            return render(request,'dashboards/medico_dashboard.html',context)
        else:
            return render(request, 'alert.html', {'message': 'Não há um consultorio disponivel.', 'redirect_url': f'/login/'})

    else:
        return render(request, 'alert.html', {'message': 'Você não está autorizada a fazer esta operação.', 'redirect_url': f'/login/'})

        
                    



@login_required
def medicoperfil(request):
    if request.user.is_authenticated:
        if request.user.is_medico:
            medico=Medico.objects.filter(nome__iexact=request.user.username).first()
            context={
            'medicos':medico,
            
            
        }
        return render(request,'dashboards/medico_perfil.html',context)






@login_required
def atendentedash(request):
    if request.user.is_authenticated:
        if request.user.is_atendente:
            pedidos=ConsultaAgenda.objects.filter(status='pendente').all()

            total=pedidos.count()

            context={
                'consultas':Consulta.objects.all(),
                'pacientes':Paciente.objects.all(),
                'atendentes':Atendete.objects.filter(nome__iexact=request.user.username).first(),
                'total':total,

            }
            return render(request,'dashboards/atendente_dashboard.html',context)


@login_required
def pacientedash(request):
    if request.user.is_authenticated:
        if request.user.is_paciente:
            

            context={
                'consultas':Consulta.objects.all(),
                'pacientes':Paciente.objects.filter(nome__iexact=request.user.username).first(),
                'consultas1':ConsultaAgenda.objects.all(),

            }
            return render(request,'dashboards/paciente_dashboard.html',context)


@receiver(post_save, sender=BancoUrgencia)
def criar_consulta_de_urgencia(sender, instance, created, **kwargs):
    if created:
        
        consulta = Consulta.objects.create(
            
            paciente_id=instance.paciente,
            
            
        )
        
        instance.consulta = consulta
        instance.save()




class BancoUrgenciaCreate(CreateView,LoginRequiredMixin):
    model=BancoUrgencia
    fields=['paciente','especialidade','prioridade','status']
    success_url=reverse_lazy('dashboard-atendente')

class BancoUrgenciaUpdate(UpdateView,LoginRequiredMixin):
    model=BancoUrgencia
    fields=['status','prioridade','paciente']
    success_url=reverse_lazy('dashboard-atendente')
    def form_valid(self, form):
        consulta = form.cleaned_data['status']
        paciente=form.cleaned_data['paciente']
        consulta1 = form.save(commit=False)
        
        if consulta == 'concluida' and self.request.user.is_medico:
            consulta1.save()
            paciente1=Consulta.objects.filter(paciente_id=paciente).last()
            
            paciente1.estado='Pagamento'
            paciente1.save()

            return redirect ('receita-create')

class BancoUrgenciaDelete(DeleteView,LoginRequiredMixin):
    model=BancoUrgencia
    success_url=reverse_lazy('dashboard-atendente')

@login_required
def urgencialist(request):
    if request.user.is_authenticated:
        if request.user.is_atendente:
            try:
                urgencia=BancoUrgencia.objects.all()
                urgencia_paginator=Paginator(urgencia,6)
                page_num=request.GET.get('page')
                page=urgencia_paginator.get_page(page_num)
            except:
                page=None
            try:
                pedidos=ConsultaAgenda.objects.filter(status='pendente').all()

                total=pedidos.count()
            except:
                total=0
            context={
                'urgencias':urgencia,
                'atendentes':Atendete.objects.filter(nome__iexact=request.user.username).first(),
                'page':page,
                'total':total,

            }
            return render(request,'home/urgencia_list.html',context)
        else:
            return HttpResponse('erro')
        
@login_required
def PontoCreate(request):
    if request.user.is_authenticated:
        if request.user.is_medico:
            medico=Medico.objects.filter(nome__iexact=request.user.username).first()
            Ponto.objects.create(medico=medico)
            return redirect('atribuir-consultorio')

class PontoDelete(DeleteView,LoginRequiredMixin):
    model=Ponto
    success_url=reverse_lazy('dashboard-medico')
 

def atribuir_paciente_a_consultorio(request):
    if request.user.is_authenticated and request.user.is_medico:
        
        medico = Medico.objects.get(nome__iexact=request.user.username)

        try:
            paciente = BancoUrgencia.objects.filter(prioridade='alta',status='pendente').order_by('prioridade').first().paciente
        except:
            
                paciente=None
        try:
                n1=Consulta.objects.filter(paciente_id=paciente.id).last()
        except:
                n1=None

        
        hora_agora = timezone.now()
        hora_limite = hora_agora + timezone.timedelta(minutes=30)
        consultorios_livres = Consultorio.objects.filter(
            Q(alocacao__isnull=True) | Q(alocacao__horario_fim__lte=hora_agora)
        )

        if consultorios_livres:
            consultorio = consultorios_livres.first()

            alocacao=Alocacao.objects.filter(medico=medico).first()

            if alocacao:
                return render(request, 'alert.html', {'message': 'já existe uma alocacao para si.', 'redirect_url': f'/dashboard-medico/'})

                

            
            alocacao = Alocacao.objects.create(
                medico=medico,
                consultorio=consultorio,
                paciente=paciente,
                horario_inicio=timezone.now(),
               
                horario_fim=timezone.now() + timezone.timedelta(minutes=30)
            )

            try:
                paciente.status = 'em atendimento'
                paciente.save()
                consultorio.alocacao = alocacao
                consultorio.save()
            except:
                paciente=None

           
            context={
            'medicos':medico,
            'consultas':Consulta.objects.all(),
            'consul':n1,
            'pontos':Ponto.objects.all(),
            'paciente':paciente,
            'alocamentos':Alocacao.objects.all(),
            'consultorio':consultorio,
            }
            return render(request,'dashboards/medico_dashboard.html',context)
        else:
            return render(request, 'alert.html', {'message': 'Não há consultórios livres disponíveis.', 'redirect_url': f'/dashboard-medico/'})

            
    else:
        return render(request, 'alert.html', {'message': 'Você não está autorizado a vizualiar está página.', 'redirect_url': f'/login/'})


        
                    




def apagar_alocacoes_expiradas():
    alocacoes_expiradas = Alocacao.objects.filter(horario_fim__lte=timezone.now())
    alocacoes_expiradas.delete()

scheduler = BackgroundScheduler()
scheduler.add_job(apagar_alocacoes_expiradas, 'interval', minutes=5)
scheduler.start()

@receiver(post_save, sender=ConsultaAgenda)
def criar_consulta_de_agenda(sender, instance, created, **kwargs):
    if created:
        
        consulta = Consulta.objects.create(
            
            paciente_id=instance.paciente_id,
            
            
        )
        
        instance.consulta = consulta
        instance.save()

class ConsultaAgendaCreate(CreateView,LoginRequiredMixin):
    model=ConsultaAgenda
    fields=['especielidade']
    success_url=reverse_lazy('dashboard-paciente')
    def form_valid(self, form):
        if self.request.user.is_paciente:
            paciente=Paciente.objects.filter(nome__iexact=self.request.user.username).first()
            especialidade=form.cleaned_data['especielidade']

            ConsultaAgenda.objects.create(paciente_id=paciente,especielidade=especialidade)

            return redirect('dashboard-paciente')


class ConsultaAgendaUpdate(UpdateView,LoginRequiredMixin):
    model=ConsultaAgenda
    fields=['paciente_id','especielidade','status','data','medico_id']
    success_url=reverse_lazy('dashboard-atendente')

    def form_valid(self, form):
        paciente=form.cleaned_data['paciente_id']
        status = form.cleaned_data['status']

        if status == 'aceite' and self.request.user.is_atendente:
            form.save()
            return redirect('dashboard-atendente')
        elif status == 'concluida' and self.request.user.is_medico:
            form.save()
            Consulta.objects.create(paciente_id=form.cleaned_data['paciente_id'])
            return redirect('receita-create')
        
        else:
            return render(self.request, 'alert.html', {'message': 'você não está autorizado a realizar esta opção.', 'redirect_url': f'/agenda-update/{paciente.id}'})

           





def pedidoslist(request):
    if request.user.is_authenticated and request.user.is_atendente:
        pedidos=ConsultaAgenda.objects.filter(status='pendente').all()

        total=pedidos.count()

        context={
            'pedidos':pedidos,
            'total':total,
            'atendentes':Atendete.objects.filter(nome__iexact=request.user.username).first(),
        }

        return render(request,'dashboards/pedidos.html',context)
    return HttpResponse('erro')


def pacientesearch(request):
    if request.method == 'GET':
        paciente=request.GET.get('paciente')
        try:
            pacientes=Paciente.objects.filter(nome__icontains=paciente).all()
        except:
            pacientes=None
        if request.user.is_atendente:
            atendente=Atendete.objects.filter(nome__iexact=request.user.username).first()
        
            n1=True

            if pacientes:
                n1=False
                paciente_paginator=Paginator(pacientes,4)
                page_num=request.GET.get('page')
                page=paciente_paginator.get_page(page_num)
                context={
                'pacientes':pacientes,
                'n1':n1,
                'user':request.user,
                
                'page':page,

            }

                return render(request,'home/paciente_search.html',context)
    else:
            return render(request, 'alert.html', {'message': 'erro.', 'redirect_url': '/dashboard-atendente/'})
        






def not_found(request,exception):
    return render(request,'home/not_found.html',status=404)





@login_required
def email_change(request):
    if request.method == 'POST':
        form = EmailChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Seu email foi alterado com sucesso.')
           
            if request.user.is_admin:
                return redirect('admin-dashboard')  
            elif request.user.is_professor:
                return redirect('home-professor')  
            elif request.user.is_aluno:
                return redirect('dashboard-aluno')  
            else:
                return redirect('profile')  
    else:
        form = EmailChangeForm(instance=request.user)
    return render(request, 'registration/email_change_form.html', {'form': form})




@login_required
def buscar_analise(request):
    if 'q' in request.GET:
        query = request.GET.get('q')
        analises = Analise.objects.filter(nome__icontains=query)
        results = [{'id': analise.id, 'nome': analise.nome} for analise in analises]
        return JsonResponse(results, safe=False)
    return JsonResponse([], safe=False)
@login_required
def AnaliseReceitaCreate(request):
    if request.user.is_authenticated:
        if request.user.is_medico:
            if request.method == 'POST':
                receita_form = ReceitaForm(request.POST)
                if receita_form.is_valid():
                    receita = receita_form.save()
                    medicamentos_ids = request.POST.getlist('analises')
                    

                    
                    medicamentos_com_dosagem = set(medicamentos_ids)

                   
                    for medicamento_id in medicamentos_com_dosagem:
                        try:
                            medicamento_id = int(medicamento_id)  
                            medicamento = Analise.objects.get(id=medicamento_id)
                            ReceitaAnalise.objects.create(
                                receita=receita,
                                analise=medicamento,
                                
                            )
                        except ValueError:
                            
                            print(f"O ID do medicamento '{medicamento_id}' não é um número válido.")
                        except Analise.DoesNotExist:
                           
                            print(f"O medicamento com ID {medicamento_id} não existe.")
                    paciente1=BancoUrgencia.objects.filter(paciente=receita.paciente_id)
            
                    paciente1.update(status='em atendimento')

                    return redirect('detalhe_analise', receita_id=receita.id)
            else:
                receita_form = ReceitaForm()

            return render(request, 'home/analise_form.html', {'receita_form': receita_form})
        


@login_required
def detalhe_analise(request, receita_id):
    if request.user.is_authenticated:
        if request.user.is_medico:
            receita = get_object_or_404(Receita, pk=receita_id)
            codigo_unico = gerar_codigo_unico(receita)
            codigo=gerar_codigo_unico_numerico(codigo_unico)
            qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
            qr.add_data(codigo_unico)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            
            img.save(f"media/codigos_de_barras/qr_code_{receita.id}.png")

            
            
            num=ReceitaAnalise.objects.filter(receita=receita_id).all()
            
            precos=sum(receita.analise.preco for receita in num)
            tax=(13*precos)/100
            total=precos+tax
            data=datetime.today()
            
            
            return render(request, 'home/analise_doc.html', {'receita': receita,'Analise':ReceitaAnalise.objects.all(),'Medico':Medico.objects.filter(nome__iexact=request.user.username).first(),'total':total,'tax':tax,'precos':precos,'data':data,'codigo':f"/media/codigos_de_barras/qr_code_{receita.id}.png",})




