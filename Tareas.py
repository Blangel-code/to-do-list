import sqlite3
import pandas as pd
import os, threading, time, datetime, ctypes, pystray, sys
from winotify import Notification, audio
from PIL import Image
from subprocess import Popen

if os.name == 'nt' and "conhost.exe" not in os.popen('tasklist /FI "PID eq %d"' % os.getppid()).read():
  Popen(["Conhost.exe", sys.executable] + sys.argv)
  sys.exit()

kernel32 = ctypes.WinDLL("kernel32")
user32 = ctypes.WinDLL("user32")

consola = kernel32.GetConsoleWindow()

MOSTRAR_CONSOLA = 5
OCULTAR_CONSOLA = 0

ruta_final = os.path.dirname(os.path.abspath(__file__))+"\\Recordatorio.db"
#Tareas Enteras
query_selecionar = "SELECT * FROM Task"
#Busca Tarea Por ID
query_buscar = "SELECT * FROM Task WHERE TaskID = ?"
#Eliminar Tarea Por ID
query_eliminar = "DELETE FROM Task WHERE TaskID = ?"
#Añadir Tarea A La Tabla
query_añadir = "INSERT INTO Task (Name,Date,Notified) Values (?,?,0)"
#Verificar Tareas
query_verificar = "SELECT * FROM Task WHERE Date <= datetime('now','localtime') AND Notified = 0"
#Modificar Si Ya Fue Avisada
query_actualizar = "UPDATE Task SET Notified = 1 WHERE Date <= ?"

icon = None

class Regresar(Exception):
  pass

def mostrar_consola(icon):
  user32.ShowWindow(consola,MOSTRAR_CONSOLA)
  icon.stop()

def salir_total(icon):
  icon.stop()
  evento_parar.set()
  os._exit(0)

def mostrar_icono():
  global icon
  user32.ShowWindow(consola,OCULTAR_CONSOLA)
  image=Image.open(os.path.dirname(os.path.abspath(__file__))+"\\notificacion.ico")
  menu = pystray.Menu(
    pystray.MenuItem("Abrir Programa",mostrar_consola),
    pystray.MenuItem("Cerrar Programa",salir_total)
  )
  icon = pystray.Icon("Lista De Tareas",image,"Lista De Tareas",menu)
  icon.run()

def pedir_input(nombre_input):
  while True:
    input_devolver = input(nombre_input).strip()
    if input_devolver == "0" or input_devolver == "salir":
      raise Regresar
    else:
      return input_devolver

class ListaDeTareas():
  def buscar_tarea(self, tarea_a_buscar):
    with sqlite3.connect(ruta_final) as conn:
      return pd.read_sql_query(query_buscar,conn,params=[tarea_a_buscar])
  
  def añadir_tarea(self, tarea_a_añadir, fecha):
    try:
      with sqlite3.connect(ruta_final, timeout=2) as conn:
        conn.cursor().execute(query_añadir,(tarea_a_añadir.title(),fecha))
        conn.commit()
        return True
    except sqlite3.OperationalError as e:
      if "locked" in str(e).lower():
        print("\nBase De Datos Bloqueada")
        return False
      else:
        print("\nError Inesperado: "+type(e).__name__)
        return False
        
  def ver_tareas(self):
    with sqlite3.connect(ruta_final) as conn:
      tareas_enteras = pd.read_sql_query(query_selecionar,conn)
    return tareas_enteras

  def eliminar_tarea(self, tarea_eliminada):
    try:
      with sqlite3.connect(ruta_final, timeout=2) as conn:
        conn.cursor().execute(query_eliminar,(str(tarea_eliminada.iloc[0,0]),))
        conn.commit()
        return True
    except sqlite3.OperationalError as e:
      if "locked" in str(e).lower():
        print("\nBase De Datos Bloqueada")
        return False
      else:
        print("\nError Inesperado: "+type(e).__name__)
        return False

lista_de_tareas = ListaDeTareas()
evento_parar = threading.Event()

def notificar(evento_parar):
  while not evento_parar.is_set():
    with sqlite3.connect(ruta_final) as conn:
      tareas_a_notificar = pd.read_sql_query(query_verificar,conn)
      for indice,tarea_a_mostrar in tareas_a_notificar.iterrows():
        notificacion_instancia = Notification(
          app_id=tarea_a_mostrar["TaskID"],
          title=tarea_a_mostrar["Name"],
          msg="Tienes Esta Tarea Pendiente",
          icon=os.path.dirname(os.path.abspath(__file__))+"\\notificacion.ico"
        )
        notificacion_instancia.set_audio(audio.Reminder,False)
        notificacion_instancia.show()
        try:
          conn.cursor().execute("UPDATE Task SET Notified = 1 WHERE TaskID = ?",(tarea_a_mostrar["TaskID"],))
          conn.commit()
        except sqlite3.OperationalError as e:
          if "locked" in str(e).lower():
            print("\nBase De Datos Bloqueada")
        time.sleep(5)
    time.sleep(60)

hilo_notificar = threading.Thread(target=notificar,daemon=True,args=(evento_parar,))
if not hilo_notificar.is_alive():
  hilo_notificar.start()

mostrar_icono()

while True:
  print("\n---------LISTA DE TAREAS----------\n\n")
  print("1) Añadir Tarea")
  print("2) Ver Tareas Pendientes")
  print("3) Eliminar Tarea")
  
  opcion_elegida = input("\nSelecciona Que Quieres Hacer: ")
  try:
    if opcion_elegida == "1":
      while True:
        tarea_añadir = pedir_input("\nNombre De La Tarea A Añadir: ")
        if not tarea_añadir.isascii():
          print("\nTarea No Añadida (Uso de Caracteres No Permitidos)")
          continue
        fecha_añadir = pedir_input("\nFecha A Avisar De La Tarea (hora:minuto día/mes): ")
        fecha_añadir = fecha_añadir.strip()+"/"+str(datetime.datetime.now().year)
        try:
          fecha_añadir = datetime.datetime.strptime(fecha_añadir, "%H:%M %d/%m/%Y").strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
          print("\nTarea No Añadida (Fecha Mal Colocada)")
          continue
        if lista_de_tareas.añadir_tarea(tarea_añadir, fecha_añadir):
          print("\nTarea Añadida Con Exito")
          break
    elif opcion_elegida == "2":
      for indice,item in lista_de_tareas.ver_tareas().iterrows():
        print(f"\n{item["TaskID"]}, {item["Name"]}, {item["Date"]}, {"Si" if item["Notified"] == 1 else "No"}")
    elif opcion_elegida == "3":
      tarea_a_eliminar = pedir_input("\nID De La Tarea A Eliminar: ")
      tarea_eliminada = lista_de_tareas.buscar_tarea(tarea_a_eliminar)
      if tarea_eliminada.empty:
        print("\nTarea No Encontrada")  
        continue
      else:
        print("\nTarea Seleccionada: "+tarea_eliminada.loc[0,"Name"])
        confirmacion = input("\n¿Seguro que deseas elminar esta Tarea? (y): ")
        if not confirmacion.isalpha():
          print("\nTarea No Eliminada")
          continue
        if not confirmacion.lower() == "y":
          print("\nTarea No Eliminada")
          continue
        if lista_de_tareas.eliminar_tarea(tarea_eliminada):
          print("\nTarea Eliminada Con Exito")
        else:
          print("No Se Pudo Eliminar La Tarea, Intentelo Más Tarde")
    elif opcion_elegida == "0" or opcion_elegida == "salir":
      mostrar_icono()
      continue
  except Regresar:
    pass