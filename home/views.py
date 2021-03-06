from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Usuario, Proyecto, Tarea
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist


# index
def index(request):
    return render(request, 'home/Pages/login.html')  

#Login_Logout views
def loginPage(request):
    return render(request, 'home/Pages/login.html')

def hacer_login(request):

    # Obtiene los datos de autenticacion
    username = request.POST['username']
    password = request.POST['password']

    # Obtiene el usuario con los datos de autenticacion
    
    try:
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff:
                return HttpResponseRedirect(reverse('visualizar_proyectos'))
            else:
                return HttpResponseRedirect(reverse('pant_usuario'))
        else:
            contexto = {
                'error': 'Usuario o contraseña incorrecto'
            }
            return render(request, 'home/Pages/login.html', contexto)
    except Usuario.user.DoesNotExist:
        contexto = {
            'error': 'Usuario no encontrado'
        }
        return render(request, 'home/Pages/login.html', contexto)

def hacer_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))     



#User views
@login_required(login_url='login')
def pant_usuario(request):
    current_user = request.user.id
    usr = Usuario.objects.get(usuario_id=current_user)
    usr2 = usr.id
    proyectos = Proyecto.objects.filter(participantes=usr2)
    usuarios = Usuario.objects.all()
    contexto = {'proyectos': proyectos, 'participantes':usuarios}
    return render(request, 'home/Pages/pant_usuario.html', contexto)

@login_required(login_url='login')
def proyectos_user(request,id):

    current_user = request.user.id
    usr = Usuario.objects.get(usuario_id=current_user)
    usr2 = usr.id
    proyecto = Proyecto.objects.get(pk=id)
    tarea = Tarea.objects.filter(usuario=usr2)
    tareas = Tarea.objects.all()

    a = tareas.filter(estado='En proceso').count()
    b = tareas.filter(estado='Finalizada').count()
    i = a+b

    if i >= 1:
        progreso_tot = (b/i)*100
    else:
        progreso_tot = 0

    c = tarea.filter(estado='En proceso').count()
    d = tarea.filter(estado='Finalizada').count()
    e = c+d 

    if e >= 1:
        progreso_ind = (d/e)*100
    else: 
        progreso_ind = 0


    contexto = {'proyecto': proyecto, 'tarea':tarea, 'progreso_ind': progreso_ind, 'progreso_tot': progreso_tot}
    return render(request, 'home/Pages/proyecto_user.html', contexto)

@login_required(login_url='login')
def cambiar_pass(request):
    return render(request, 'home/Pages/cambiar_pass.html')

@login_required(login_url='login')
def cambiar_pass_accion(request):
    password = request.POST['password']

    current_user=request.user.id
    user = User.objects.get(id=current_user)
    user.set_password(password)
    user.save()
    messages.info(request, '¡Tu contraseña ha sido modificada satisfactoriamente!, por favor ingresa de nuevo')
    return render(request, 'home/Pages/login.html')

@login_required(login_url='login')
def actualizar_tareas_user(request, id):
    tarea = Tarea.objects.get(pk=id)

    if tarea.archivo.name: var='true'
    else: var='false'

    contexto = {'tarea':tarea, 'var':var}  
    return render(request, 'home/Pages/tareas_user.html', contexto)

@login_required(login_url='login')
def act_tarea_accion(request, id):
    valor_estado = request.POST.get('estado')   
    valor_archivo = request.FILES.get('archivo')
    tarea = Tarea.objects.get(pk=id)
    tarea.estado=valor_estado
    
    if request.FILES:
        valor_archivo = request.FILES['archivo']
        tarea.archivo=valor_archivo
 
    tarea.save()
    return HttpResponseRedirect(reverse('pant_usuario'))


#Admin views
@staff_member_required(login_url='login')
def crear_usuario(request):
    usuarios = Usuario.objects.all()

    contexto = {'usuarios': usuarios}
    return render(request, 'home/Pages/crear_usuario.html', contexto)

@staff_member_required(login_url='login')
def crear_usuario_accion(request):
    username = request.POST['username']
    valor_firstname = request.POST['firstName']
    valor_lastname = request.POST.get('lastN')
    email = request.POST['email']
    password = request.POST['password']
    cargo = request.POST['tipo_cargo']
    
    usr = User.objects.filter(username=username)
    correo = User.objects.filter(email=email)

    if len(usr) != 0:
        contexto = {
            'error': 'El nombre de usuario ya está siendo utilizado'
        }
        return render(request, 'home/Pages/crear_usuario.html', contexto)
    elif len(correo) !=0:
        contexto = {
            'error': 'El correo electrónico ya está siendo utilizado'
        }
        return render(request, 'home/Pages/crear_usuario.html', contexto)
    else:
        user = User(
        username=username,
        first_name=valor_firstname,
        last_name=valor_lastname,
        email=email,
        )
    
    user.set_password(password)
    user.save()

    parti = Usuario(usuario=user, tipo_cargo=cargo)
    parti.save()
    return HttpResponseRedirect(reverse('visualizar_usuarios'))

@staff_member_required(login_url='login')
def visualizar_usuarios(request):
    usuarios = Usuario.objects.all()

    contexto = {'usuarios':usuarios}
    return render(request, 'home/Pages/visualizar_usuarios.html', contexto)

@staff_member_required(login_url='login')
def editar_usuario(request, id):
    usuario = Usuario.objects.get(pk=id)

    contexto = {'usuario': usuario }
    return render(request, 'home/Pages/editar_usuario.html', contexto)

@staff_member_required(login_url='login')
def editar_usuario_accion(request,id):
    username = request.POST['username']
    valor_firstname = request.POST['firstName']
    valor_lastname = request.POST.get('lastN')
    email = request.POST['email']
    cargo = request.POST['tipo_cargo']

    usuario = User.objects.get(pk=id)
    usr = Usuario.objects.get(usuario_id=id)

    print(usr)
    usuario.username=username
    usuario.first_name=valor_firstname
    usuario.last_name=valor_lastname
    usuario.email=email
    usr.tipo_cargo=cargo

    usuario.save()
    usr.save()
    return HttpResponseRedirect(reverse('visualizar_usuarios'))

@staff_member_required(login_url='login')
def eliminar_usuario(request,id):
    usuario = Usuario.objects.get(pk=id)
    usuario.delete()
    return HttpResponseRedirect(reverse('visualizar_usuarios'))

@staff_member_required(login_url='login')
def crear_proyecto(request):
    usuarios = Usuario.objects.all()

    contexto = {'usuarios': usuarios}
    return render(request, 'home/Pages/crear_proyecto.html', contexto)

@staff_member_required(login_url='login')
def crear_proyecto_accion(request):
    valor_nombre = request.POST['nombre']
    valor_descripcion = request.POST['descripcion']
    valor_tipo_proy = request.POST['tipo_proy']
    valor_fecha_kick = request.POST['fecha_kick']
    valor_fecha_inicio = request.POST['fecha_inicio']
    valor_moneda = request.POST['moneda']
    valor_trm = request.POST['trm']
    valor_costo_implementacion = request.POST['costo_implementacion']
    valor_margen = request.POST['margen']
    valor_ans = request.POST['ans']
    valor_incremento = request.POST['incremento']
    valor_costo_imp_diferido = request.POST['costo_imp_diferido']
    valor_facturacion = request.POST['facturacion']
    valor_penal = request.POST['penal']
    valor_duracion_total = request.POST['duracion_total']
    valor_duracion_implementacion = request.POST['duracion_implementacion']
    valor_costo_mensual = request.POST['costo_mensual']
    valor_cotizador = request.FILES['cotizador']
    valor_documento = request.FILES['documento'] 
    valor_participantes = request.POST.getlist('participantes')   

    instance = Proyecto.objects.create(nombre_proyecto=valor_nombre,descripcion=valor_descripcion,
    tipo_proy=valor_tipo_proy, fecha_kick=valor_fecha_kick,
    fecha_inicio=valor_fecha_inicio, moneda=valor_moneda, trm = valor_trm, costo_implementacion= valor_costo_implementacion,
    margen=valor_margen, ans=valor_ans, incremento=valor_incremento, costo_imp_diferido=valor_costo_imp_diferido,
    facturacion=valor_facturacion, penal=valor_penal, duracion_total=valor_duracion_total,
    duracion_implementacion=valor_duracion_implementacion, costo_mensual=valor_costo_mensual, 
    cotizador=valor_cotizador, documento=valor_documento)
    
    for c in valor_participantes:        
        users = Usuario.objects.filter(usuario=c)
        instance.participantes.add(*users)
 
    return HttpResponseRedirect(reverse('visualizar_proyectos'))

@staff_member_required(login_url='login')
def eliminar_proyecto(request,id):
    proyecto = Proyecto.objects.get(pk=id)
    proyecto.delete()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

@staff_member_required(login_url='login')
def editar_proyecto(request, id):

    usuarios = Usuario.objects.all()
    proyecto = Proyecto.objects.get(pk=id)

    contexto = {'usuarios': usuarios, 'proyecto': proyecto }
    return render(request, 'home/Pages/editar_proyecto.html', contexto)

@staff_member_required(login_url='login')
def editar_proyecto_accion(request,id):
    valor_nombre = request.POST['nombre']
    valor_descripcion = request.POST['descripcion']
    valor_tipo_proy = request.POST['tipo_proy']
    valor_fecha_kick = request.POST['fecha_kick']
    valor_fecha_inicio = request.POST['fecha_inicio']
    valor_moneda = request.POST['moneda']
    valor_trm = request.POST['trm']
    valor_costo_implementacion = request.POST['costo_implementacion']
    valor_margen = request.POST['margen']
    valor_ans = request.POST['ans']
    valor_incremento = request.POST['incremento']
    valor_costo_imp_diferido = request.POST['costo_imp_diferido']
    valor_facturacion = request.POST['facturacion']
    valor_penal = request.POST['penal']
    valor_duracion_total = request.POST['duracion_total']
    valor_duracion_implementacion = request.POST['duracion_implementacion']
    valor_costo_mensual = request.POST['costo_mensual']
    valor_participantes = request.POST.getlist('participantes')

    proyecto = Proyecto.objects.get(pk=id)
 
    proyecto.nombre_proyecto=valor_nombre
    proyecto.descripcion=valor_descripcion
    proyecto.tipo_proy=valor_tipo_proy
    proyecto.fecha_kick=valor_fecha_kick
    proyecto.fecha_inicio=valor_fecha_inicio
    proyecto.moneda=valor_moneda
    proyecto.trm = valor_trm
    proyecto.costo_implementacion= valor_costo_implementacion
    proyecto.margen=valor_margen
    proyecto.ans=valor_ans
    proyecto.incremento=valor_incremento
    proyecto.costo_imp_diferido=valor_costo_imp_diferido
    proyecto.facturacion=valor_facturacion
    proyecto.penal=valor_penal
    proyecto.duracion_total=valor_duracion_total
    proyecto.duracion_implementacion=valor_duracion_implementacion
    proyecto.costo_mensual=valor_costo_mensual

    if request.FILES:
        valor_cotizador = request.FILES['cotizador']
        proyecto.cotizador=valor_cotizador
        valor_documento = request.FILES['documento']
        proyecto.documento=valor_documento

    if len(valor_participantes)>0:
        proyecto.participantes.clear()
        for c in valor_participantes:
            users = Usuario.objects.filter(usuario=c)
            proyecto.participantes.add(*users)
 
    proyecto.save()
    return HttpResponseRedirect(reverse('visualizar_proyectos'))

@staff_member_required(login_url='login')
def visualizar_proyectos(request):
    proyectos = Proyecto.objects.all()
    usuarios = Usuario.objects.all()

    contexto = {'proyectos': proyectos, 'participantes':usuarios}
    return render(request, 'home/Pages/visualizar_proyectos.html', contexto)

@staff_member_required(login_url='login')
def proyecto(request,id):
    proyecto = Proyecto.objects.get(pk=id)
    tareas = Tarea.objects.all()

    a = tareas.filter(estado='En proceso').count()
    b = tareas.filter(estado='Finalizada').count()
    i = a+b

    if i >= 1:
        progreso_tot = (b/i)*100
    else:
        progreso_tot = 0

    contexto = {'proyecto': proyecto, 'progreso_tot':progreso_tot}
    return render(request, 'home/Pages/proyecto.html', contexto)

@staff_member_required(login_url='login')
def crear_tarea(request,id):
    proyecto = Proyecto.objects.get(pk=id)
    contexto = {'proyecto': proyecto}
    return render(request, 'home/Pages/crear_tarea.html', contexto)

@staff_member_required(login_url='login')
def crear_tarea_accion(request):
    valor_nombre_tarea = request.POST.get('nombre_tarea')
    valor_descripcion_tarea = request.POST['descripcion_tarea']
    valor_usuario = Usuario.objects.get(id=request.POST['usuario'])
    valor_proyecto = Proyecto.objects.get(id=request.POST['proyecto'])  
    valor_estado = request.POST['estado']

    print(valor_usuario)
    tar = Tarea(nombre_tarea=valor_nombre_tarea, descripcion_tarea=valor_descripcion_tarea, 
    usuario=valor_usuario, proyecto=valor_proyecto, estado=valor_estado)

    tar.save()
    return HttpResponseRedirect(reverse('visualizar_proyectos'))

@staff_member_required(login_url='login')
def editar_tarea(request, id):
    tarea = Tarea.objects.get(pk=id)
    proyecto = tarea.proyecto
    
    if tarea.archivo.name: var='true'
    else: var='false'

    contexto = {'tarea': tarea, 'proyecto':proyecto, 'var':var}
    return render(request, 'home/Pages/editar_tarea.html', contexto)

@staff_member_required(login_url='login')    
def editar_tarea_accion(request,id):
    valor_nombre_tarea = request.POST.get('nombre_tarea')
    valor_descripcion_tarea = request.POST['descripcion_tarea']
    valor_usuario = Usuario.objects.get(id=request.POST['usuario'])
    valor_proyecto = Proyecto.objects.get(id=request.POST['proyecto'])  
    valor_estado = request.POST['estado']

    print(valor_usuario)
    tarea = Tarea.objects.get(pk=id)
    tarea.nombre_tarea=valor_nombre_tarea
    tarea.descripcion_tarea=valor_descripcion_tarea
    tarea.usuario=valor_usuario
    tarea.estado=valor_estado
    tarea.proyecto=valor_proyecto

    tarea.save()
    return HttpResponseRedirect(reverse('visualizar_proyectos'))

@staff_member_required(login_url='login')
def eliminar_tarea(request,id):
    tarea = Tarea.objects.get(pk=id)
    tarea.delete()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

@staff_member_required(login_url='login')
def visualizar_tareas(request, id):
    proyecto = Proyecto.objects.get(pk=id)
    tareas = Tarea.objects.filter(proyecto=id)

    a = tareas.filter(estado='En proceso').count()
    b = tareas.filter(estado='Finalizada').count()
    i = a+b

    if i >= 1:
        progreso_tot = (b/i)*100
    else:
        progreso_tot = 0

    contexto = {'tareas': tareas, 'proyecto':proyecto, 'progreso_tot': progreso_tot}
    return render(request, 'home/Pages/listar_tareas.html', contexto)


def prueba(request):
    return HttpResponseRedirect(reverse('visualizar_proyectos'))

       