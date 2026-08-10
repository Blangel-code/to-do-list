# to-do-list

Archivo: requirements.txt incluido en la raíz del proyecto.

Una lista de tareas que funciona mediante consola, se ejecuta en segundo plano y envía notificaciones al escritorio.

## Descripción

Aplicación de línea de comandos escrita en Python para gestionar tareas. Permite crear, listar y marcar tareas como completadas desde la terminal; está pensada para ejecutarse en segundo plano (por ejemplo, como servicio/daemon) y enviar notificaciones de escritorio cuando sea necesario (nuevas tareas, recordatorios o tareas vencidas).

## Características

- Interfaz por consola (CLI) ligera y fácil de usar.
- Ejecución en segundo plano para monitorizar tareas continuamente.
- Notificaciones de escritorio para avisos y recordatorios.
- Almacenamiento simple (archivo local o base de datos ligera); revisa el código para detalles sobre persistencia.

## Requisitos

- Python 3.7 o superior.
- El repositorio incluye un archivo `requirements.txt` en la raíz con las dependencias necesarias para notificaciones y utilidades. Asegúrate de revisar ese archivo antes de la instalación.

Dependencias listadas en `requirements.txt`:
- notify2 (Linux)
- plyer (multiplataforma)
- win10toast (Windows)
- click (helpers para CLI)
- python-dateutil (manejo de fechas)

## Instalación

1. Clona el repositorio:

   git clone https://github.com/Blangel-code/to-do-list.git
   cd to-do-list

2. (Opcional) Crea y activa un entorno virtual:

   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   .venv\Scripts\activate    # Windows

3. Instala las dependencias desde el archivo `requirements.txt` que se encuentra en la raíz del proyecto:

   pip install -r requirements.txt

Si por alguna razón necesitas instalar solo dependencias específicas, abre `requirements.txt` y usa `pip install <paquete>` para instalarlas individualmente.

## Uso

Ejecuta la aplicación desde la terminal. La forma exacta de uso depende del CLI implementado en el proyecto; ejemplos generales:

- Ejecutar en primer plano:

  python main.py

- Ejecutar en segundo plano (Linux/macOS):

  nohup python main.py &

Para un uso en producción considera crear un servicio systemd (Linux) o una tarea programada/servicio en Windows.

Revisa el código para conocer los comandos disponibles y las opciones del CLI.

## Notificaciones de escritorio

La aplicación envía notificaciones cuando hay eventos relevantes (nueva tarea, recordatorio, tarea vencida).

- En Linux: `notify-send` o bibliotecas como `notify2`/`plyer`.
- En macOS: `osascript` o bibliotecas que usen las notificaciones nativas.
- En Windows: `win10toast` o `plyer`.

Asegúrate de tener instaladas las dependencias necesarias según tu sistema operativo.

## Configuración

Configura en el código o en archivos de configuración:

- Intervalos de comprobación (cada cuánto se revisan las tareas).
- Ruta de almacenamiento de datos.
- Opciones de notificación (activar/desactivar, sonidos, niveles de prioridad).

## Contribuir

Si quieres contribuir:

1. Haz fork del repositorio.
2. Crea una rama: `git checkout -b feature/nombre-feature`.
3. Realiza tus cambios y haz commit: `git commit -m "Describe tu cambio"`.
4. Envía un Pull Request describiendo el cambio.

Se agradecen correcciones, mejoras y pruebas automatizadas.

---

Hecho por: Blangel-code

Licencia: Este proyecto está bajo la licencia MIT. Si deseas el texto completo de la licencia, añade un archivo `LICENSE` con el contenido de la MIT o consulta `https://opensource.org/licenses/MIT`.
