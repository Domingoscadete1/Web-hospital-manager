from django.contrib import admin
from django.urls import path,include
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', home,name="home" ),
    path('register/',registro,name='cadastro' ),
    path('plataforma/',plataforma,name='plataforma' ),

    path('login/',login_view,name='login' ),
    path('logout/', logout_view, name='logout'),
    path('form/', form_modal, name='form_modal'),
    path('paciente-list/', pacientelist, name='paciente-list'),
    path('paciente-create/', PacienteCreate.as_view(), name='paciente-create'),
    path('paciente-update/<int:pk>', PacienteUpdate.as_view(), name='paciente-update'),
    path('paciente-delete/<int:pk>', PacienteDelete.as_view(), name='paciente-delete'),

    path('medico-list/', medicolist, name='medico-list'),
    path('medico-create/', MedicoCreate.as_view(), name='medico-create'),
    path('medico-update/<int:pk>', MedicoUpdate.as_view(), name='medico-update'),
    path('medico-delete/<int:pk>', MedicoDelete.as_view(), name='medico-delete'),

    path('consulta-create/', ConsultaCreate.as_view(), name='consulta-create'),
    path('consulta-update/<int:pk>', ConsultaUpdate.as_view(), name='consulta-update'),
    path('consulta-delete/<int:pk>', ConsultaDelete.as_view(), name='consulta-delete'),
    
    path('medicamento-list/', medicamentolist, name='medicamento-list'),
    path('medicamento-create/', MedicamentoCreate.as_view(), name='medicamento-create'),
    path('medicamento-update/<int:pk>', MedicamentoUpdate.as_view(), name='medicamento-update'),
    path('medicamento-delete/<int:pk>', MedicamentoDelete.as_view(), name='medicamento-delete'),

    path('buscar-medicamentos/', buscar_medicamentos, name='buscar_medicamentos'),
    path('receita-create/', ReceitaCreate, name='receita-create'),
    path('receita-update/<int:pk>', ReceitaUpdate.as_view(), name='receita-update'),
    path('receita-delete/<int:pk>', ReceitaDelete.as_view(), name='receita-delete'),
    path('receitas/<int:receita_id>/', detalhe_receita, name='detalhe_receita'),
    path('receitas/<int:receita_id>/download/', gerar_receita_texto, name='gerar_receita_texto'),

    
    path('factura-list/', facturalist, name='factura-list'),
    path('factura-create/', FacturaCreate.as_view(), name='factura-create'),
    path('factura-update/<int:pk>', FacturaUpdate.as_view(), name='factura-update'),
    path('factura-delete/<int:pk>', FacturaDelete.as_view(), name='factura-delete'),


    path('dashboard-medico/',medicodash,name='dashboard-medico'),
    path('perfil-medico/',medicoperfil,name='perfil-medico'),


    path('dashboard-atendente/', atendentedash,name='dashboard-atendente'),

    path('dashboard-paciente/', pacientedash,name='dashboard-paciente'),

    path('urgencia-create/',BancoUrgenciaCreate.as_view(),name='urgencia-create'),
    path('urgencia-update/<int:pk>',BancoUrgenciaUpdate.as_view(),name='urgencia-update'),
    path('urgencia-delete/<int:pk>',BancoUrgenciaDelete.as_view(),name='urgencia-delete'),
    path('urgencia-list/',urgencialist,name='urgencia-list'),
    path('ponto-create/',PontoCreate,name='ponto-create'),
    path('ponto-delete/<int:pk>',PontoDelete.as_view(),name='ponto-delete'),
    path('atribuir-consulutorio/',atribuir_paciente_a_consultorio,name='atribuir-consultorio'),
    path('agenda-create/',ConsultaAgendaCreate.as_view(),name='agenda-create'),
    path('agenda-update/<int:pk>',ConsultaAgendaUpdate.as_view(),name='agenda-update'),
    path('pedidos-list/',pedidoslist,name='pedidos-list'),
    path('dashboard-especialista/',especialistadash,name='dashboard-especialista'),

    path('paciente-search/',pacientesearch,name='paciente-search'),


    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    


    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change_form.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name='password_change_done'),


    path('email_change/', email_change, name='email_change'),

    path('analise-add/',AnaliseReceitaCreate,name='analise-add'),
    path('buscar-analise/',buscar_analise,name='buscar-analise'),
    path('analise/<int:receita_id>/', detalhe_analise, name='detalhe_analise'),

    


]