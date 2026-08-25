#Tareas Enteras
QUERY_SELECCIONAR = "SELECT * FROM Task"
#Busca Tarea Por ID
QUERY_BUSCAR = "SELECT * FROM Task WHERE TaskID = ?"
#Eliminar Tarea Por ID
QUERY_ELIMINAR = "DELETE FROM Task WHERE TaskID = ?"
#Añadir Tarea A La Tabla
QUERY_ANADIR = "INSERT INTO Task (Name,Date,Notified) Values (?,?,0)"
#Verificar Tareas
QUERY_VERIFICAR = "SELECT * FROM Task WHERE Date <= datetime('now','localtime') AND Notified = 0"
#Modificar Si Ya Fue Avisada
QUERY_ACTUALIZAR = "UPDATE Task SET Notified = 1 WHERE TaskID = ?"
#Crear La Tabla Principal ("Task")
QUERY_CREAR_TABLA = """CREATE TABLE "Task" (
	"TaskID"	INTEGER,
	"Name"	TEXT,
	"Date"	TEXT,
	"Notified"	INTEGER,
	PRIMARY KEY("TaskID" AUTOINCREMENT)
);"""
#Vaciando La Tabla Principal ("Task")
QUERY_VACIAR_TABLA = "DELETE FROM Task"
QUERY_VACIAR_CONTADOR = "DELETE FROM sqlite_sequence WHERE name = 'Task'"