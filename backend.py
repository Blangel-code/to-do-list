import sqlite3, threading, pystray, querys as q
from pathlib import Path
from winotify import Notification, audio
from time import sleep
from PIL import Image

class ListaDeTareas:
    def __init__(self):
        self.path_base = Path(__file__).resolve().parent
        self.path_db = self.path_base / "data" / "data.db"
        self.path_icon = self.path_base / "notified_icon.ico"
        self.image_system_tray = Image.open(self.path_icon)
        self.evento_parar = threading.Event()
        self._make_dir()
        self._create_table()

    def _make_dir(self):
        self.path_db.parent.mkdir(parents=True,exist_ok=True)

    def _make_cursor(self,query:str,parameters:tuple = None,fetch:bool=False):
        conn = sqlite3.connect(self.path_db)
        try:
            cursor = conn.cursor()
            cursor.execute(query,parameters)
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
        self._make_cursor(q.QUERY_CREAR_TABLA)

    def _create_notification(self,task_to_show:str):
        notificacion_instancia = Notification(
            app_id="Lista De Tareas",
            title=task_to_show,
            msg="Tienes Esta Tarea Pendiente",
            icon=self.path_icon,
            duration="long"
        )
        notificacion_instancia.set_audio(audio.Reminder,False)
        notificacion_instancia.add_actions("Prosponer 1 Hora",self._propose_task)
        notificacion_instancia.show()

    def _propose_task(self):
        #configurar debidamente el código
        print("Tarea Propuesta")

    def _show_gui(self):
        pass
    
    def close_app(self):
        pass
        
    def buscar_tarea(self,ID_task_to_search:int):
        return self._make_cursor(q.QUERY_BUSCAR,(ID_task_to_search,),True)
        
    def añadir_tarea(self,name_task_add:str,date_task_add:str):
        return self._make_cursor(q.QUERY_ANADIR,(name_task_add,date_task_add))            
    
    def ver_tareas(self):
        return self._make_cursor(q.QUERY_SELECCIONAR,fetch=True)
    
    def eliminar_tarea(self, task_to_eliiminated):
        return self._make_cursor(q.QUERY_ELIMINAR,(str(task_to_eliiminated[0][0]),))
    
    def notified_tasks(self,evento_parar:threading.Event):
        while not evento_parar.is_set():
            tasks_to_notified = self._make_cursor(q.QUERY_VERIFICAR,fetch=True)
            for task_to_show in tasks_to_notified:
                self._create_notification(task_to_show[1])
                self._make_cursor(q.QUERY_ACTUALIZAR,(task_to_show[0],))
                sleep(5)
            sleep(60)
        
    def show_pytray(self):
        #LÓGICA PARA QUITAR LA GUI
        menu = pystray.Menu(
          pystray.MenuItem("Abrir Programa",self._show_gui),
          pystray.MenuItem("Cerrar Programa",self.close_app)
        )
        self.system_tray = pystray.Icon("Lista De Tareas",self.image_system_tray,"Lista De Tareas",menu)
        self.system_tray.run()
    