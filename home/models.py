from django.db import models
from django.contrib.auth.models import User


class Usuario(models.Model):
    PREVENTA = 'Ingeniero Preventa'
    COORDINADOR_PREVENTA = 'Coordinador Preventa'
    OPERADOR_SET = 'Operador SET'
    OPERADOR_GTI = 'Operador GTI'
    ING_CLOUD = 'Arquitecto Cloud'
    ING_ESPECIALISTA = 'Ingeniero Especialista'
    AGENTE = 'Agente de mesa'
    GERENTE = 'Gerente de proyecto'
    CONTADOR = 'Contador'
    ANALISTA = 'Analista ITIL'
    ING_IMP = 'Ingeniero implementacion'
    LIDER_IMP = 'Lider de implementacion'
    LIDER_NOC = 'Lider NOC'
    LIDER_SOC = 'Lider SOC'

    TIPO_CARGO_CHOICES = [
        (PREVENTA, 'Ingeniero Preventa'),
        (COORDINADOR_PREVENTA, 'Coordinador Preventa'),
        (OPERADOR_SET, 'Operador SET'),
        (OPERADOR_GTI, 'Operador GTI'),
        (ING_CLOUD, 'Arquitecto Cloud'),
        (ING_ESPECIALISTA, 'Ingeniero Especialista'),
        (AGENTE, 'Agente de mesa'),
        (GERENTE,'Gerente de proyecto'),
        (CONTADOR, 'Contador'),
        (ANALISTA, 'Analista ITIL'),
        (ING_IMP, 'Ingeniero implementacion'),
        (LIDER_IMP, 'Lider de implementacion'),
        (LIDER_NOC, 'Lider NOC'),
        (LIDER_SOC, 'Lider SOC')
    ]
    tipo_cargo = models.CharField(max_length=30,
        choices=TIPO_CARGO_CHOICES,
        default="Ingeniero Preventa",null=False)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.usuario.first_name) + " " +  (self.usuario.last_name)

    class Meta:
        app_label = 'home'


class Proyecto(models.Model):
    GTI = 'GTI'
    SET = 'SET'
    CLOUD = 'CLOUD'
    TIPO_LINEA_CHOICES = [
        (GTI, 'GTI'),
        (SET, 'SET'),
        (CLOUD, 'CLOUD')
    ]
    IPC = 'IPC'
    SLMV = 'SLMV'
    INCREMENTO_CHOICES = [
        (IPC, 'IPC'),
        (SLMV, 'SLMV'),
    ]
    COP = 'COP'
    USD = 'USD'
    MONEDA_CHOICES = [
        (COP, 'COP'),
        (USD, 'USD'),
    ]
    MES_VENCIDO = 'Mes Vencido'
    MES_CORRIENTE = 'Mes Corriente'
    FACTURACION_CHOICES = [
        (MES_VENCIDO, 'Mes Vencido'),
        (MES_CORRIENTE, 'Mes Corriente'),
    ]
    noventa_cinco = '95'
    noventa_siete = '97'
    nonventa_nueve = '99'
    ANS_CHOICES = [
        (noventa_cinco, '95'),
        (noventa_siete, '97'),
        (nonventa_nueve, '99'),
    ]
    SI = 'SI'
    NO = 'NO'
    IMP_CHOICES = [
        (SI, 'SI'),
        (NO, 'NO'),
    ]
    nombre_proyecto = models.CharField(null=False, max_length=50)
    descripcion = models.CharField(null=False, max_length=50)
    tipo_proy = models.CharField(max_length=7,
        choices=TIPO_LINEA_CHOICES,
        default="GTI",null=False)
    participantes = models.ManyToManyField(Usuario, related_name='participantes')  
    fecha_kick = models.DateField(null=False)
    fecha_inicio = models.DateField(null=False)
    moneda = models.CharField(max_length=7,
        choices=MONEDA_CHOICES,
        default="COP",null=False)
    trm = models.IntegerField(null=False)
    costo_implementacion = models.IntegerField(null=False)
    margen = models.IntegerField(null=False)
    ans = models.CharField(max_length=7,
        choices=ANS_CHOICES,
        default="95",null=False)
    incremento = models.CharField(max_length=7,
        choices=INCREMENTO_CHOICES,
        default="IPC",null=False)
    costo_imp_diferido = models.CharField(max_length=7,
        choices=IMP_CHOICES,
        default="SI",null=False)
    facturacion = models.CharField(max_length=13,
        choices=FACTURACION_CHOICES,
        default="MES_VENCIDO",null=False)
    penal = models.IntegerField(null=False)
    duracion_total = models.IntegerField(null=False)
    duracion_implementacion = models.IntegerField(null=False)
    costo_mensual = models.IntegerField(null=False)
    cotizador = models.FileField(upload_to='media/', blank = True)
    documento = models.FileField(upload_to='media/', blank = True)
    vista = models.BooleanField(null=True)
    def __str__(self):
        return self.nombre_proyecto

    class Meta:
        app_label = 'home'

class Tarea(models.Model):
    PROCESO = 'En proceso'
    FINALIZADA = 'Finalizada'
    ESTADO_CHOICES = [
        (PROCESO, 'En proceso'),
        (FINALIZADA, 'Finalizada'),
    ]
    nombre_tarea = models.CharField(null=False, max_length=50)
    descripcion_tarea = models.CharField(null=False, max_length=100)
    estado = models.CharField(max_length=10,
        choices=ESTADO_CHOICES,
        default="PROCESO",null=True)
    usuario = models.ForeignKey(Usuario,
                 related_name='tarea_usuario',
                 on_delete=models.CASCADE,
                 null=True)
    proyecto = models.ForeignKey(Proyecto,
                 related_name='tarea_proyecto',
                 on_delete=models.CASCADE,
                 null=True)
    archivo = models.FileField(upload_to='media/', blank = True, null=True)
    def __str__(self):
        return self.nombre_tarea

    class Meta:
        app_label = 'home'
