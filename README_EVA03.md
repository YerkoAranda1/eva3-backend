# GameGo evaluación 03

El proyecto adapta el ejemplo App-Tareas-102-4B del profesor a los videojuegos existentes. Mantiene las clases APIView, authenticate, Token.objects.get_or_create, TokenAuthentication, IsAuthenticated, get_object_or_404 y Response. Las páginas usan fetch, JSON y sessionStorage como el ejemplo.

## Cómo ejecutar

Desde la carpeta del proyecto en PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Antes de migrar, inicia MySQL en XAMPP. La configuración existente usa la base `gamego`, usuario `root`, contraseña vacía y puerto 3306. Si la base todavía no existe, créala en phpMyAdmin con el nombre `gamego`. No borres una base existente.

Abre http://127.0.0.1:8000/ e ingresa con un usuario de Django. Se creó el usuario local gamego para iniciar sesión. Su contraseña inicial se entregó en el chat. Si ya tienes otro usuario, también puedes utilizarlo. El login obtiene un token y lo guarda en sessionStorage. Las solicitudes protegidas llevan el encabezado `Authorization: Token <token>`. Cerrar sesión elimina el token en Django y después lo retira del navegador; las demás pestañas que usen ese mismo token deberán iniciar sesión otra vez.

## Rutas

| Ruta | Método | Función |
| --- | --- | --- |
| `/api/login/` | POST | Autenticar username y password y entregar token |
| `/api/logout/` | POST | Invalidar el token actual |
| `/api/videojuegos/` | GET | Listar videojuegos |
| `/api/videojuegos/` | POST | Crear videojuego |
| `/api/videojuegos/ID/` | GET | Consultar videojuego |
| `/api/videojuegos/ID/` | PUT | Actualizar los seis campos |
| `/api/videojuegos/ID/` | DELETE | Eliminar videojuego |

La raíz muestra el login; `/videojuegos/` muestra el inventario. Crear, ver, editar y eliminar usan las rutas HTML anteriores y consultan la API. Las páginas HTML entregan la estructura de la interfaz; los datos y las operaciones están protegidos en el servidor mediante el token. Abrir una página sin token redirige al login.

Ejemplo de cuerpo JSON para POST o PUT:

```json
{
  "titulo": "Juego de ejemplo",
  "plataforma": "PC",
  "genero": "Aventura",
  "precio": 29990,
  "stock": 0,
  "fecha_estreno": "2026-11-05"
}
```

Respuestas: 200 para consultas y actualizaciones, 201 para creación, 204 para eliminación, 400 para datos inválidos, 401 para autenticación ausente o inválida y 404 para un ID inexistente.

## Adaptaciones y agregados autorizados

| Archivo | Procedencia o cambio |
| --- | --- |
| `app_videojuegos/views.py` | Login y clases API adaptadas de `tareasapp/views.py`; mismos métodos y respuestas mediante diccionarios |
| `app_videojuegos/urls.py` | Rutas equivalentes a las de tareas, con nombres de videojuegos |
| `tienda/settings.py` | rest_framework, authtoken y configuración de permisos del ejemplo; conexión MySQL existente conservada |
| `templates/app_videojuegos/login.html` | Login del profesor con textos de GameGo y redirección al inventario |
| Plantillas del CRUD | Apariencia existente de GameGo y scripts GET, POST, PUT y DELETE adaptados de las plantillas del profesor |
| `validar_videojuego` | Agregado autorizado para completar las validaciones exigidas |
| `LogoutAPIView` y botón Cerrar sesión | Agregados autorizados para revocar el token |
| `migrations/0002_videojuego_fecha_estreno.py` | Corrección del default entero inválido por la fecha `2000-01-01` |

Las validaciones comprueban textos obligatorios y longitudes; precio entero mayor que cero; stock entero no negativo; límites del IntegerField de MySQL; fecha real en formato AAAA-MM-DD y año entre 1000 y 9999. POST y PUT validan antes de guardar. Los mensajes aparecen en los formularios.

No se agregó una nueva migración porque no cambió la estructura del modelo. La corrección de la migración 0002 permite aplicarla a una base nueva. Si esa migración se aplica a una tabla antigua con registros sin fecha, usa `2000-01-01` como valor inicial y luego debes editar esos registros con sus fechas reales. Las bases donde la migración ya fue aplicada no se modifican por editar su archivo.

## Demostración de la rúbrica

1. Intenta entrar con una contraseña incorrecta y después con credenciales válidas.
2. En las herramientas de desarrollo del navegador, revisa el token y el encabezado Authorization de las solicitudes.
3. Crea un videojuego, lista el inventario y abre su detalle.
4. Modifica el stock y comprueba el resultado después de recargar.
5. En phpMyAdmin revisa `app_videojuegos_videojuego` y confirma el registro creado y los cambios.
6. Envía un precio negativo, un decimal, una fecha imposible o un campo vacío a la API y comprueba el error 400 sin guardar cambios.
7. Consulta un ID inexistente y comprueba el error 404.
8. Elimina el registro de prueba y verifica su ausencia en el inventario y MySQL.
9. Cierra sesión y repite una consulta con el token anterior: debe responder 401.

## Trabajo en parejas y Git

El código por sí solo no acredita los aportes de ambos integrantes. Cada persona debe trabajar realmente en su rama, hacer commits descriptivos, publicar su rama y explicar sus cambios. No se deben inventar aportes ni autores.

Una distribución posible es autenticación y API para una persona, e interfaz y pruebas para la otra. Acuerden primero qué archivos editará cada integrante. Luego creen sus ramas a partir de la versión acordada, hagan sus cambios y commits, publiquen cada rama e integren en main mediante merge. Comprueben el funcionamiento después de integrar. El repositorio remoto y la defensa individual siguen siendo parte de la entrega de ustedes.

Para la defensa: explica qué hace urls.py, cómo una APIView usa el modelo, por qué un token ausente produce 401, qué distingue POST de PUT, por qué DELETE responde sin cuerpo y cómo una migración crea o modifica tablas en MySQL.

## Verificación realizada

Se ejecutaron 150 comprobaciones de backend sobre una base SQLite temporal y otras 150 sobre MySQL: login, token ausente e inválido, los cuatro métodos, validaciones, IDs inexistentes, plantillas y revocación del token. También se ejecutaron 20 comprobaciones de los scripts de la interfaz con un DOM simulado. Se confirmó POST, PUT y DELETE desde una segunda conexión MySQL después de guardar los cambios y se retiraron todos los registros de prueba. No se realizó una revisión visual en un navegador.

La conexión a gamego quedó comprobada y las migraciones de tokens fueron aplicadas. Como la columna fecha_estreno ya existía con el tipo correcto, se registró la migración 0002 como aplicada sin volver a crear la columna. El inventario quedó vacío y se creó una cuenta local gamego. No se crearon ramas, commits ni publicaciones remotas: los aportes de ambos integrantes y la integración mediante merge siguen pendientes.
