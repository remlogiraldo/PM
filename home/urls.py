from django.urls import path
from django.conf import settings
from django.conf.urls import url
from . import views

#las vistas creadas

urlpatterns = [

    path('',views.index, name='index'),
    path('login/', views.loginPage, name='login'),
    path('hacer_login/?', views.hacer_login, name='hacer_login'),
    path('logout/', views.hacer_logout, name='logout'),
    
    #gestion admin usuarios
    path('admin/crear_usuario/', views.crear_usuario, name='crear_usuario'),
    path('admin/crear_usuario_accion/', views.crear_usuario_accion, name='crear_usuario_accion'),
    path('admin/visualizar_usuarios/',views.visualizar_usuarios, name='visualizar_usuarios'),
    path('admin/editar_usuario/<int:id>/', views.editar_usuario, name='editar_usuario'),
    path('admin/editar_usuario_accion/<int:id>/editar/?', views.editar_usuario_accion, name='editar_usuario_accion'),
    path('admin/eliminar_usuario/<int:id>/borrar/', views.eliminar_usuario, name='eliminar_usuario'),

    #gestion admin proyectos
    path('admin/crear_proyecto/', views.crear_proyecto, name='crear_proyecto'),
    path('admin/crear_proyecto_accion/', views.crear_proyecto_accion, name='crear_proyecto_accion'),
    path('admin/editar_proyecto/<int:id>/', views.editar_proyecto, name='editar_proyecto'),
    path('admin/editar_proyecto_accion/<int:id>/editar/?', views.editar_proyecto_accion, name='editar_proyecto_accion'),
    path('admin/visualizar_proyectos/',views.visualizar_proyectos, name='visualizar_proyectos'),
    path('admin/visualizar_proyectos/<int:id>/',views.proyecto, name='proyecto'),
    path('admin/crear_tarea/<int:id>/', views.crear_tarea, name='crear_tarea'),
    path('admin/crear_tarea_accion/', views.crear_tarea_accion, name='crear_tarea_accion'),
    path('admin/visualizar_tareas/<int:id>/',views.visualizar_tareas, name='visualizar_tareas'),
    path('admin/visualizar_tareas/editar_tarea/<int:id>/', views.editar_tarea, name='editar_tarea'),
    path('admin/editar_tarea_accion/<int:id>/editar/?', views.editar_tarea_accion, name='editar_tarea_accion'),
    path('admin/eliminar_proyecto/<int:id>/borrar/', views.eliminar_proyecto, name='eliminar_proyecto'),


    #interfaz usuarios
    path('usuario/pant_usuario/',views.pant_usuario, name='pant_usuario'),
    path('usuario/visualizar_proyectos_user/<int:id>/',views.proyectos_user, name='proyectos_user'),
    path('usuario/cambiar_pass/',views.cambiar_pass, name='cambiar_pass'),
    path('usuario/cambiar_pass_accion/',views.cambiar_pass_accion, name='cambiar_pass_accion'),
    path('usuario/actualizar_tareas_user/<int:id>/',views.actualizar_tareas_user, name='actualizar_tareas_user'),
    path('usuario/act_tarea_accion/<int:id>/act/?',views.act_tarea_accion, name='act_tarea_accion'),
    path('usuario/eliminar_tarea/<int:id>/borrar/', views.eliminar_tarea, name='eliminar_tarea'),


    path('prueba/', views.prueba, name='prueba'),
    
]