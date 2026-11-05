from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_pagina, name='login_pagina'),
    path('videojuegos/', views.listar_juegos, name='listar_juegos'),
    path('crear/', views.crear_juego, name='crear_juego'),
    path('detalle/<int:id>/', views.detalle_juego, name='detalle_juego'),
    path('editar/<int:id>/', views.editar_juego, name='editar_juego'),
    path('eliminar/<int:id>/', views.eliminar_juego, name='eliminar_juego'),
    path('api/logout/', views.LogoutAPIView.as_view(), name='logout_api'),
    path('api/login/', views.LoginAPIView.as_view(), name='login_api'),
    path('api/videojuegos/', views.VideojuegosApiView.as_view(), name='api_videojuegos'),
    path('api/videojuegos/<int:id>/', views.VideojuegoDetalleApiView.as_view(), name='api_videojuego_detalle'),
]
