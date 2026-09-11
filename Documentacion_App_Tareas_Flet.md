# Documentación Técnica del Proyecto: Aplicación de Lista de Tareas (Flet + SQLite)

Este documento describe la arquitectura, estructura de código y funcionalidad de la aplicación de Lista de Tareas desarrollada en Python utilizando **Flet** y **SQLite**. Está diseñado específicamente para servir como contexto de alto nivel y referencia para **Agentes de IA** o desarrolladores que necesiten extender, depurar o refactorizar el código.

---

## 1. Visión General del Proyecto

La aplicación es un administrador de tareas de escritorio para Windows, construido de forma modular. Ofrece una interfaz moderna y fluida con soporte para notificaciones nativas del sistema operativo, ejecución en segundo plano (tray/minimize) y almacenamiento persistente relacional.

### Características Principales:
* **CRUD Completo:** Creación, lectura, edición y eliminación de tareas.
* **Búsqueda y Filtrado:** Búsqueda en tiempo real por palabra clave y filtrado por estado (p. ej., pendientes, completadas, todas).
* **Persistencia de Datos:** SQLite como motor de base de datos relacional ligero.
* **Notificaciones Nativas:** Integración con el sistema de notificaciones de Windows.
* **Ejecución en Segundo Plano:** La aplicación puede permanecer activa en la bandeja del sistema/segundo plano.
* **Diseño Modular:** Separación clara entre la capa de acceso a datos, la lógica de negocio y la interfaz de usuario.

---

## 2. Arquitectura de Módulos

El proyecto está organizado en 3 archivos principales, promoviendo el principio de **Separación de Responsabilidades (SoC)**:

```
project_root/
│
├── querys.py        # Capa de Datos (Data Access Layer - DAL)
├── backend.py       # Capa de Lógica de Negocio (Business Logic Layer)
└── main.py          # Capa de Presentación / Interfaz de Usuario (UI - Flet)
```

---

## 3. Detalle de los Módulos

### 3.1. `querys.py` — Capa de Base de Datos (Queries SQLite)
**Propósito:** Contiene exclusivamente las sentencias SQL puras y las funciones encargadas de interactuar de forma directa con la base de datos `SQLite`.

* **Responsabilidades:**
  * Crear las tablas requeridas si no existen (`CREATE TABLE IF NOT EXISTS`).
  * Ejecutar consultas SQL parametrizadas para evitar inyecciones SQL.
  * Proveer funciones CRUD atómicas:
    * `insert_task(...)`: Insertar nueva tarea.
    * `get_all_tasks(...)`: Obtener listado general o filtrado/buscado.
    * `update_task(...)`: Actualizar título, descripción, estado o fecha.
    * `delete_task(...)`: Eliminar registro por ID.
* **Esquema de la Tabla (`tasks`):**
  * `id` (INTEGER PRIMARY KEY AUTOINCREMENT)
  * `Name` (TEXT NOT NULL)
  * `Notified` (TEXT / BOOLEAN) — Estado de la tarea (ej. 'pending' (0), 'completed' (1))
  * `Date` (TIMESTAMP / TEXT) - Fecha a notificar de la tarea (2026-01-01 12:00)

---

### 3.2. `backend.py` — Capa de Lógica de Negocio y Notificaciones
**Propósito:** Actúa como puente entre la interfaz de usuario (`main.py`) y la base de datos (`querys.py`), manejando reglas de negocio, validaciones y servicios del sistema operativo (notificaciones y segundo plano).

* **Responsabilidades:**
  * **Procesamiento de Datos:** Validar datos recibidos de la UI antes de enviarlos a `querys.py`.
  * **Notificaciones Nativas de Windows:** Utiliza librerías como `plyer` o `win10toast` para lanzar alertas push cuando expira una tarea o se crea un evento relevante.
  * **Manejo de Segundo Plano:** Lógica para mantener vivos los procesos de monitoreo/notificación cuando la ventana principal se minimiza o cierra hacia la bandeja del sistema.
  * **Filtros y Búsqueda:** Métodos que procesan las cadenas de texto de búsqueda y aplican los filtros de estado correspondientes antes de solicitar los datos.

---

### 3.3. `main.py` — Capa de Interfaz de Usuario (Flet UI)
**Propósito:** Construye y gestiona la interfaz gráfica de usuario declarativa utilizando la librería **Flet** (basada en Flutter).

* **Responsabilidades:**
  * **Definición de Vistas y Componentes:**
    * Campo de entrada (`TextField`) para agregar o buscar tareas.
    * Contenedores de lista (`ListView` / `Column`) para renderizar cada tarjeta de tarea (`Container`, `Card`, `Checkbox`).
    * Diálogos modales (`AlertDialog`) para la edición avanzada de tareas.
  * **Manejo de Eventos (`Event Handlers`):**
    * Interceptar clicks de usuarios (añadir, editar, eliminar, marcar completado).
    * Actualizar dinámicamente el estado de la UI (`page.update()`).
  * **Configuración de Ventana:**
    * Manejar eventos de minimización a la bandeja del sistema (System Tray).

---

## 4. Flujo de Datos Típico

1. **Creación de Tarea:**
   * El usuario escribe la tarea en `main.py` y presiona "Agregar".
   * `main.py` llama al método correspondiente en `backend.py`.
   * `backend.py` valida la entrada y ejecuta la función de inserción en `querys.py`.
   * `querys.py` escribe en SQLite y confirma la transacción.
   * `main.py` recarga la lista de tareas y refresca la pantalla (`page.update()`).
   * (Opcional) `backend.py` programa una notificación nativa.

2. **Búsqueda / Filtrado:**
   * El usuario interactúa con la barra de búsqueda en `main.py`.
   * Se dispara un evento en tiempo real que invoca a `backend.py`.
   * `backend.py` consulta a `querys.py` filtrando por los criterios.
   * La UI actualiza la colección de componentes en pantalla.

---

## 5. Instrucciones para la IA (Prompting Context)

Cuando le pidas a un agente de IA que agregue una función o corrija un bug, utiliza las siguientes directrices según el módulo afectado:

* **Si pides modificar la base de datos o SQL:**
  * *"Edita `querys.py` para añadir la columna X a la tabla y actualiza las funciones de selección e inserción relacionadas."*
* **Si pides modificar notificaciones, lógica o tareas en segundo plano:**
  * *"Ajusta `backend.py` para modificar cómo se programan las notificaciones de Windows o cómo se procesa el filtro X."*
* **Si pides cambios visuales, componentes de Flet o interfaz de usuario:**
  * *"Modifica `main.py` para cambiar el diseño de las tarjetas de tareas o agregar un nuevo botón en la interfaz de Flet."*

---

## 6. Requisitos y Dependencias

* **Python:** 3.8+
* **Librerías principales:**
  * `flet`: Framework de UI.
  * `sqlite3`: Módulo nativo de Python para la BD.
  * `plyer` / `win10toast` / `pystray`: Para notificaciones nativas y soporte de bandeja del sistema en Windows.
