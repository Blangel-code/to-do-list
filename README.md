# to-do-list

Aplicación de escritorio para gestionar tareas, desarrollada en Python. Proporciona una interfaz gráfica con Flet, almacenamiento mediante SQLite, ejecución en segundo plano (bandeja del sistema) y notificaciones nativas del sistema operativo.

## Descripción

Esta es una aplicación modular para crear, editar, buscar y organizar tareas. Está pensada para usarse en Windows (interfaz Flet) pero es portable a otros sistemas con pequeñas adaptaciones para las notificaciones y la bandeja del sistema.

La estructura principal del proyecto está separada en tres capas: acceso a datos (`querys.py`), lógica de negocio y servicios (`backend.py`) y la interfaz de usuario (`main.py`) construida con Flet.

## Características nuevas y principales

- Interfaz gráfica de usuario (GUI) construida con Flet.
- CRUD completo: crear, leer, actualizar y eliminar tareas.
- Búsqueda en tiempo real y filtrado por estado (Pendientes, Completadas, Todas).
- Persistencia con SQLite (archivo local `tasks.db` o similar).
- Notificaciones nativas del sistema (Windows/Linux/macOS) para recordatorios y tareas vencidas.
- Ejecución en segundo plano / bandeja del sistema para mantener la aplicación activa sin ocupar la pantalla.
- Diseño modular (separación: `querys.py`, `backend.py`, `main.py`) para facilitar mantenimiento y extensiones.
- Soporte básico multiplataforma para notificaciones (bibliotecas alternativas según SO).

## Requisitos

- Python 3.8 o superior.
- Archivo `requirements.txt` en la raíz con las dependencias necesarias. Revisa su contenido antes de la instalación.

Dependencias habituales (pueden variar, mira `requirements.txt`):
- flet
- pystray
- winotify
- Pillow

## Instalación

1. Clona el repositorio:

   git clone https://github.com/Blangel-code/to-do-list.git
   cd to-do-list

2. (Opcional) Crea y activa un entorno virtual:

   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   .venv\Scripts\activate    # Windows

3. Instala las dependencias desde `requirements.txt`:

   pip install -r requirements.txt

Si necesitas instalar paquetes individuales: `pip install <paquete>`.

## Uso

- Ejecutar la interfaz gráfica (ejemplo):

  python main.py

  o, si tu instalación de Flet requiere el runner:

  flet run main.py

- La aplicación muestra la lista de tareas, permite crear nuevas, editar existentes, marcarlas como completadas y filtrarlas.
- Para ejecutar la aplicación en segundo plano en Windows, la aplicación soporta minimización a la bandeja del sistema; consulta la implementación en `main.py` y `backend.py`.

## Notificaciones y segundo plano

- La lógica de notificaciones y ejecución en segundo plano está centralizada en `backend.py`.
- En Windows se usan `win10toast` o `plyer` para mostrar notificaciones nativas.
- En Linux `notify2` o `plyer` pueden emplearse; en macOS puede usarse `osascript` o adaptadores compatibles.
- Asegúrate de tener las dependencias necesarias instaladas para tu SO.

## Estructura del proyecto

- querys.py  — funciones de acceso a SQLite (creación de tablas y consultas parametrizadas).
- backend.py — lógica de negocio, validaciones, programación de notificaciones y manejo de segundo plano.
- main.py    — interfaz de usuario con Flet y handlers de eventos.

Consulta los archivos para ver la API interna y extender funcionalidades.

## Contribuir

Si quieres contribuir con mejoras, correcciones o nuevas características:

1. Haz fork del repositorio.
2. Crea una rama: `git checkout -b feature/nombre-feature`.
3. Realiza tus cambios y haz commit: `git commit -m "Describe tu cambio"`.
4. Envía un Pull Request describiendo el cambio y cómo probarlo.

Se agradecen pruebas automatizadas y documentación de las nuevas funciones.

---

Hecho por: Blangel-code

Licencia: Este proyecto está bajo la licencia MIT. Si deseas el texto completo de la licencia, entra al  archivo `LICENSE` con el contenido de la MIT o consulta https://opensource.org/licenses/MIT
