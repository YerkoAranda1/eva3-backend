from datetime import datetime


from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication

from .models import Videojuego


def login_pagina(request):
    return render(request, 'app_videojuegos/login.html')


def listar_juegos(request):
    return render(request, 'app_videojuegos/listar_juegos.html')


def crear_juego(request):
    return render(request, 'app_videojuegos/crear_juego.html')


def detalle_juego(request, id):
    return render(request, 'app_videojuegos/detalle_juego.html')


def editar_juego(request, id):
    return render(request, 'app_videojuegos/editar_juego.html')


def eliminar_juego(request, id):
    return render(request, 'app_videojuegos/eliminar_juego.html')


# Agregado para la rúbrica: tipos, formatos y reglas del inventario.
def validar_videojuego(datos):
    if not isinstance(datos, dict):
        return 'Debes enviar un objeto JSON con los datos del videojuego.'

    for campo, limite in [('titulo', 30), ('plataforma', 30), ('genero', 30)]:
        valor = datos.get(campo)
        if not isinstance(valor, str) or not valor.strip():
            return f'El campo {campo} debe ser un texto obligatorio.'
        if len(valor.strip()) > limite:
            return f'El campo {campo} admite como máximo {limite} caracteres.'

    for campo, minimo in [('precio', 1), ('stock', 0)]:
        valor = datos.get(campo)
        if type(valor) not in (str, int):
            return f'El campo {campo} debe ser un número entero.'
        if isinstance(valor, str) and (not valor.isascii() or not valor.isdigit()):
            return f'El campo {campo} solo admite dígitos del 0 al 9, sin puntos, signos ni espacios.'
        try:
            numero = int(valor)
        except (ValueError, TypeError):
            return f'El campo {campo} debe ser un número entero.'
        if numero < minimo or numero > 2147483647:
            return f'El campo {campo} debe estar entre {minimo} y 2147483647.'

    fecha = datos.get('fecha_estreno')
    if not isinstance(fecha, str):
        return 'La fecha de estreno es obligatoria y debe usar AAAA-MM-DD.'
    try:
        fecha_validada = datetime.strptime(fecha, '%Y-%m-%d').date()
    except ValueError:
        return 'La fecha de estreno debe ser una fecha real con formato AAAA-MM-DD.'
    if fecha_validada.isoformat() != fecha or fecha_validada.year < 1000:
        return 'La fecha debe usar AAAA-MM-DD y un año entre 1000 y 9999.'

    return None


class LoginAPIView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        if not isinstance(request.data, dict):
            return Response({'error': 'Debes enviar usuario y contraseña en un objeto JSON.'}, status=status.HTTP_400_BAD_REQUEST)

        username= request.data.get('username')
        password= request.data.get('password')

        if not isinstance(username, str) or not isinstance(password, str) or not username.strip() or not password:
            return Response({'error': 'El usuario y la contraseña son obligatorios.'}, status=status.HTTP_400_BAD_REQUEST)

        usuario = authenticate(
            username=username,
            password=password
        )

        if usuario is not None:

            token, creado = Token.objects.get_or_create(
                user=usuario
            )

            return Response({
                'mensaje': 'Autenticacion Correcta',
                'usuario': usuario.username,
                'token': token.key
            }, status=status.HTTP_200_OK)
        return Response({
            'error': 'Usuario o contraseña incorrectos'
        }, status=status.HTTP_401_UNAUTHORIZED)


class VideojuegosApiView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # GET Listar todos los videojuegos

    def get(self, request):

        juegos = Videojuego.objects.all()

        datos = []

        for juego in juegos:
            datos.append({
               'id': juego.id,
               'titulo': juego.titulo,
               'plataforma': juego.plataforma,
               'genero': juego.genero,
               'precio': juego.precio,
               'stock': juego.stock,
               'fecha_estreno': juego.fecha_estreno, 
            }) 
        return Response(datos, status=status.HTTP_200_OK)
        
    
    def post(self, request):

        # recibir los datos enviados por el cliente

        error = validar_videojuego(request.data)
        if error:
            return Response({'error': error}, status=status.HTTP_400_BAD_REQUEST)

        titulo = request.data.get('titulo').strip()
        plataforma = request.data.get('plataforma').strip()
        genero = request.data.get('genero').strip()
        precio = int(request.data.get('precio'))
        stock = int(request.data.get('stock'))
        fecha_estreno = datetime.strptime(request.data.get('fecha_estreno'), '%Y-%m-%d').date()

        
        juego = Videojuego.objects.create(
            titulo=titulo, 
            plataforma=plataforma,
            genero=genero,
            precio=precio,
            stock=stock,
            fecha_estreno=fecha_estreno,
        )

        #Devolver el videojuego

        return Response({
            'mensaje':'Videojuego creado correctamente',
            'juego':{
                'id':juego.id,
                'titulo': juego.titulo,
                'plataforma': juego.plataforma,
                'genero': juego.genero,
                'precio': juego.precio,
                'stock': juego.stock,
                'fecha_estreno': juego.fecha_estreno,
            }

        }, status=status.HTTP_201_CREATED)
    
class VideojuegoDetalleApiView(APIView):

    authentication_classes= [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # GET Consultar por un videojuego por id
    def get(self, request, id):
        juego = get_object_or_404(Videojuego, id=id)

        return Response({
            'id':juego.id,
            'titulo':juego.titulo,
            'plataforma': juego.plataforma,
            'genero': juego.genero,
            'precio': juego.precio,
            'stock': juego.stock,
            'fecha_estreno': juego.fecha_estreno,
        }, status=status.HTTP_200_OK)

    #DELETE: Eliminar un videojuego
    def delete(self, request, id):
        juego = get_object_or_404(Videojuego, id=id)
        juego.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


    #PUT: Actualizar un videojuego completo
    def put(self, request, id):
        juego = get_object_or_404(Videojuego, id=id)

        error = validar_videojuego(request.data)
        if error:
            return Response({'error': error}, status=status.HTTP_400_BAD_REQUEST)

        titulo = request.data.get('titulo').strip() 
        plataforma = request.data.get('plataforma').strip()
        genero = request.data.get('genero').strip()
        precio = int(request.data.get('precio'))
        stock = int(request.data.get('stock'))
        fecha_estreno = datetime.strptime(request.data.get('fecha_estreno'), '%Y-%m-%d').date() 


        juego.titulo = titulo
        juego.plataforma = plataforma
        juego.genero = genero
        juego.precio = precio
        juego.stock = stock
        juego.fecha_estreno = fecha_estreno
        juego.save()

        return Response({
          'mensaje': 'Videojuego actualizado correctamente',
          'id': juego.id,
          'titulo': juego.titulo,
          'plataforma': juego.plataforma,
          'genero': juego.genero,
          'precio': juego.precio,
          'stock': juego.stock,
          'fecha_estreno': juego.fecha_estreno,
        }, status=status.HTTP_200_OK)
            


class LogoutAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Agregado para la rúbrica: el token deja de autorizar solicitudes.
        request.auth.delete()
        return Response({'mensaje': 'Sesión cerrada correctamente.'}, status=status.HTTP_200_OK)
