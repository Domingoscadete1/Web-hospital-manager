from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    is_admin=models.BooleanField('Is admin',default=False)
    is_paciente=models.BooleanField('Is paciente',default=False)
    is_medico=models.BooleanField('Is medico',default=False)
    is_atendente=models.BooleanField('Is atendente',default=False)
    is_especialista=models.BooleanField('Is especialista',default=False)
GENERO=(
    ('Masculino','Masculino'),
    ('Feminino','Feminino'),

)
STATUS=(
    ('Pendente','Pendente'),
    ('Marcada','Marcada'),
    ('Realizada','Realizada'),
    ('Pagamento','Pagamento'),

)
ESTADO=(
    ('Solterio','Solteiro'),
    ('Casado','Casado')
)
TIPO=(
    ('Clinica Medica','Clinica Medica'),
    ('Pediatria','Pediatria'),
    ('Neurologia','Neurologia'),
    ('Cardiologia','Cardiologia'),
    ('Ginecologia','Ginecologia'),
    ('Ortopedia','Ortopedia'),
    
)
TIPO_CONSULTA=(
    ('Ginecologia','Ginecologia'),
    ('Cirugia','Cirugia'),
    ('Dermatologia','Dermatologia'),
    ('Odontologia','Odontolgia'),
    ('Oftamologia','Oftamologia'),
    ('Nutricao','Nutricao')
)
class Paciente(models.Model):
    nome=models.CharField(max_length=255,blank=False,null=False)
    idade=models.PositiveIntegerField()
    nif=models.CharField(max_length=255,blank=True,null=True)
    nacionalidade=models.CharField(max_length=120,null=False)
    genero=models.CharField(max_length=50,choices=GENERO)
    profissao=models.CharField(max_length=120)
    descricao=models.TextField()
    foto=models.ImageField(upload_to='imagens_paciente/')
    def __str__(self) -> str:
        return f'{self.nome}'
    
class Medico(models.Model):
    nome=models.CharField(max_length=255,blank=False,null=False)
    idade=models.PositiveIntegerField()
    nacionalidade=models.CharField(max_length=120,null=False)
    genero=models.CharField(max_length=50,choices=GENERO)
    profissao=models.CharField(max_length=120)
    descricao=models.TextField()
    especialidade=models.CharField(max_length=120,choices=TIPO,null=True,blank=True)
    formacao=models.TextField()
    foto=models.ImageField(upload_to='imagens_medico/')
    is_especialista=models.BooleanField('Is especialista',default=False)
    especialidade_agendamento=models.CharField(max_length=120,choices=TIPO_CONSULTA,null=True,blank=True)
    def __str__(self) -> str:
        return f'{self.nome}'
    
class Atendete(models.Model):
    nome=models.CharField(max_length=255,blank=False,null=False)
    idade=models.PositiveIntegerField()
    nacionalidade=models.CharField(max_length=120,null=False)
    genero=models.CharField(max_length=50,choices=GENERO)
    profissao=models.CharField(max_length=120)
    descricao=models.TextField()
    formacao=models.TextField()
    foto=models.ImageField(upload_to='imagens_atendente/')
    def __str__(self) -> str:
        return f'{self.nome}'

class Consulta(models.Model):
    medico_id=models.ForeignKey(Medico,on_delete=models.CASCADE,null=True,blank=True)
    paciente_id=models.ForeignKey(Paciente,on_delete=models.CASCADE,null=False)
    tipo=models.CharField(max_length=255,choices=TIPO,null=True,blank=True,default='banco urgência')
    estado=models.CharField(max_length=255,choices=STATUS,null=True,blank=True)
    data = models.DateField(auto_now_add=True)
    hora = models.TimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'Consulta nº{self.id}-{self.paciente_id.nome}-{self.tipo}-{self.data}-{self.hora}'

class BancoUrgencia(models.Model): 
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    especialidade = models.CharField(max_length=120,choices=TIPO)  
    prioridade = models.CharField(max_length=10, choices=[('alta', 'Alta'), ('media', 'Média'), ('baixa', 'Baixa')])
    status = models.CharField(max_length=20, choices=[('pendente', 'Pendente'), ('em atendimento', 'Em Atendimento'), ('concluida', 'Concluída')])
    consulta = models.OneToOneField(Consulta, on_delete=models.CASCADE, null=True, blank=True)

class Medicamento(models.Model):
    nome=models.CharField(max_length=255,blank=False,null=False)
    especificacoes=models.TextField()
    recomendacoes=models.TextField()
    tipo=models.CharField(max_length=120)
    horario=models.CharField(max_length=255)
    def __str__(self) -> str:
        return f'{self.nome}'
    

class Receita(models.Model):
    medico_id=models.ForeignKey(Medico,on_delete=models.CASCADE,null=False)
    consulta_id=models.ForeignKey(Consulta,on_delete=models.CASCADE,null=False)
    paciente_id=models.ForeignKey(Paciente,on_delete=models.CASCADE,null=True)
    descricao=models.TextField()
    status = models.CharField(max_length=20, null=True, blank=True,choices=[('pendente', 'Pendente'), ('concluida', 'Concluída')],default='pendente')
    codigo=models.ImageField(upload_to='codigos_de_barras/',null=True, blank=True)


class ReceitaMedicamento(models.Model):
    receita = models.ForeignKey(Receita, on_delete=models.CASCADE)
    medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE)
    dosagem = models.CharField(max_length=255) 

    def __str__(self):
        return f"{self.receita} - {self.medicamento}"
class Factura(models.Model):
    consulta_id=models.ForeignKey(Consulta,on_delete=models.CASCADE,null=False)
    total=models.FloatField()
    paciente_id=models.ForeignKey(Paciente,on_delete=models.CASCADE,null=False)
    data = models.DateField(auto_now_add=True)
    hora = models.TimeField(auto_now_add=True)

class ConsultaAgenda(models.Model):
    paciente_id=models.ForeignKey(Paciente,on_delete=models.CASCADE,null=False,blank=False)
    especielidade=models.CharField(max_length=255,choices=TIPO_CONSULTA,null=False,blank=False)
    status = models.CharField(max_length=20, choices=[('pendente', 'Pendente'), ('aceite', 'Aceite'), ('concluida', 'Concluída')],default='pendente')
    consulta = models.OneToOneField(Consulta, on_delete=models.CASCADE, null=True, blank=True)
    data=models.DateField( null=True, blank=True)
    medico_id=models.ForeignKey(Medico,on_delete=models.CASCADE,null=True,blank=True)
    hora_pedido=models.TimeField(auto_now_add=True)








class Ponto(models.Model):
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    data = models.DateField(auto_now_add=True)
    hora = models.TimeField(auto_now_add=True)

class Consultorio(models.Model):
    numero = models.IntegerField()
    

class Alocacao(models.Model):
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    consultorio = models.ForeignKey(Consultorio, on_delete=models.CASCADE)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, null=True, blank=True)
    horario_inicio = models.DateTimeField()  
    horario_fim = models.DateTimeField()
    status = models.CharField(max_length=20, choices=[('pendente', 'Pendente'), ('em_atendimento', 'Em Atendimento'), ('concluida', 'Concluída')])
    ponto = models.ForeignKey(Ponto, on_delete=models.CASCADE, null=True, blank=True)  


class MedicoEspecialista(models.Model):
    nome=models.CharField(max_length=255,blank=False,null=False)
    idade=models.PositiveIntegerField()
    nacionalidade=models.CharField(max_length=120,null=False)
    genero=models.CharField(max_length=50,choices=GENERO)
    profissao=models.CharField(max_length=120)
    descricao=models.TextField()
    especialidade=models.CharField(max_length=120,choices=TIPO_CONSULTA)
    formacao=models.TextField()
    foto=models.ImageField(upload_to='imagens_medico/')
    def __str__(self) -> str:
        return f'{self.nome}'

class Analise(models.Model):
    nome=models.CharField(max_length=100)
    Area_corporal_amostra=models.CharField(max_length=100)
    Descricao=models.TextField()
    preco=models.FloatField()

    def __str__(self) -> str:
        return f'{self.nome}'
    


    
class ReceitaAnalise(models.Model):
    receita = models.ForeignKey(Receita, on_delete=models.CASCADE)
    analise= models.ForeignKey(Analise, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.receita} - {self.analise}"