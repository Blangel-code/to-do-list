"""Capa de persistencia y servicios de segundo plano de la aplicación.

La clase :class:`ToDoList` encapsula SQLite, las notificaciones de Windows y
la integración con la bandeja del sistema. La interfaz Flet debe comunicarse
con esta clase y no ejecutar SQL directamente.
"""

import sqlite3, threading, pystray, querys as q
from pathlib import Path
from winotify import Notification, audio
from time import sleep
from PIL import Image

class ToDoList:
    """Gestiona tareas, almacenamiento SQLite y notificaciones nativas."""

    def __init__(self):
        """Inicializa rutas, base de datos y el hilo de notificaciones."""
        self.path_base = Path (__file__).resolve().parent
        self.path_db = self.path_base / "data" / "data.db"
        self.path_icon = self.path_base / "notified_icon.ico"
        self.image_system_tray = Image.open(self.path_icon)
        self.event_stop = threading.Event()
        self._make_dir()
        self._create_table()
        self.thread_notify = threading.Thread(target=self.notified_tasks,daemon=True,args=(self.event_stop,))
        if not self.thread_notify.is_alive(): self.thread_notify.start()

    def _make_dir(self):
        """Crea el directorio de datos si todavía no existe."""
        self.path_db.parent.mkdir(parents=True,exist_ok=True)

    def _make_cursor(self,query:str,parameters:tuple = None,fetch:bool=False):
        """Ejecuta una consulta parametrizada en una conexión independiente.

        Args:
            query: Sentencia SQL a ejecutar.
            parameters: Valores para los marcadores de la sentencia.
            fetch: Si es ``True``, devuelve todas las filas obtenidas.

        Returns:
            Lista de filas, ``True`` si la escritura fue correcta o ``False``
            cuando SQLite informa de un error.
        """
        conn = sqlite3.connect(self.path_db)
        try:
            cursor = conn.cursor()
            cursor.execute(query,parameters) if parameters else cursor.execute(query)
            if fetch:
                return cursor.fetchall()
            conn.commit()
            return True
        except sqlite3.OperationalError as e:
            if "locked" in str(e).lower():
                print("\nBase De Datos Bloqueada")
                return False
            else:
                print("\nError Inesperado: "+type(e).__name__)
                return False
        except Exception as e:
            print(f"\nHa Ocurrido Un Error Inesperado {str(e)}")
            return False
        finally:
            conn.close()
    
    def _create_table(self):
        """Crea la tabla de tareas si no existe."""
        self._make_cursor(q.QUERY_CREATE_TABLE)

    def _create_notification(self,task_to_show:str):
        """Muestra una notificación nativa de Windows para una tarea."""
        notificacion_instancia = Notification(
            app_id="Lista De Tareas",
            title=task_to_show,
            msg="Tienes Esta Tarea Pendiente",
            icon=self.path_icon,
            duration="long",
        )
        notificacion_instancia.set_audio(audio.Reminder,False)
        notificacion_instancia.show()

    def start_system_tray(self,show_gui,close_gui):
        """Inicia la bandeja del sistema con acciones de abrir y cerrar.

        Args:
            show_gui: Callback que restaura la ventana principal.
            close_gui: Callback que finaliza la aplicación.
        """
        
        def _handle_show():
            """Restaura la interfaz y detiene el icono de bandeja."""
            show_gui()
            self.system_tray.stop()
        
        def _handle_exit():
            """Cierra la aplicación y detiene el icono de bandeja."""
            close_gui()
            self.system_tray.stop()
        
        menu = pystray.Menu(
            pystray.MenuItem("Abrir Programa",_handle_show,default=True),
            pystray.MenuItem("Cerrar Programa",_handle_exit)
        )
        self.system_tray = pystray.Icon("Lista De Tareas",self.image_system_tray,"Lista De Tareas",menu)
        self.system_tray.run_detached()

    def search_task(self,ID_task_to_search:int,name_task_to_search:str,filter_check:None,filter_parameter:int):
        """Busca tareas por ID/nombre y aplica el filtro de estado."""
        return self._make_cursor(q.QUERY_SEARCH,(f"%{ID_task_to_search}%",f"%{name_task_to_search}%",filter_check,filter_parameter),True)
        
    def añadir_tarea(self,name_task_add:str,date_task_add:str):
        """Inserta una tarea pendiente con nombre y fecha proporcionados."""
        return self._make_cursor(q.QUERY_ADD,(name_task_add,date_task_add))            
    
    def eliminar_tarea(self, task_to_eliiminated:int):
        """Elimina una tarea identificada por su ID."""
        return self._make_cursor(q.QUERY_DELETE,(task_to_eliiminated,))
    
    def modify_task_value_notified(self,task_id:int):
        """Invierte el estado de completado/notificación de una tarea."""
        return self._make_cursor(q.QUERY_MODIFY_NOTIFIED,(task_id,))

    def modify_task_value(self,name_for_modify:str,date_for_modify:str,task_id:int):
        """Actualiza el nombre y la fecha de una tarea existente."""
        return self._make_cursor(q.QUERY_MODIFY_TASK,(name_for_modify,date_for_modify,task_id))

    def delete_all_task_completed(self):
        """Elimina todas las tareas cuyo estado es completado."""
        return self._make_cursor(q.QUERY_DELETE_ALL_COMPLETED)

    def notified_tasks(self,evento_parar:threading.Event):
        """Notifica periódicamente las tareas vencidas hasta recibir la señal.

        Args:
            evento_parar: Evento compartido para detener el hilo de trabajo.
        """
        while not evento_parar.is_set():
            tasks_to_notified = self._make_cursor(q.QUERY_VERIFY,fetch=True)
            for task_to_show in tasks_to_notified:
                self._create_notification(task_to_show[1])
                self._make_cursor(q.QUERY_MODIFY_NOTIFIED,(task_to_show[0],))
                sleep(5)
            sleep(60)