"""Consultas SQL parametrizadas de la aplicación de tareas.

Este módulo contiene únicamente sentencias SQL. La apertura de conexiones,
las transacciones y el tratamiento de errores pertenecen a ``backend.py``.
"""

# Busca tareas por ID o nombre.
QUERY_SEARCH = """SELECT * FROM Task WHERE (TaskID LIKE ? OR Name LIKE ?) 
AND (? IS NULL OR Notified = ?)
ORDER BY Date ASC
"""
# Elimina una tarea por ID.
QUERY_DELETE = "DELETE FROM Task WHERE TaskID = ?"
# Añade una tarea pendiente.
QUERY_ADD = "INSERT INTO Task (Name,Date,Notified) Values (?,?,0)"
# Obtiene tareas vencidas que todavía no han sido notificadas.
QUERY_VERIFY = "SELECT TaskID, Name FROM Task WHERE Date <= datetime('now','localtime') AND Notified = 0"
# Invierte el estado de notificación/completado.
QUERY_MODIFY_NOTIFIED = "UPDATE Task SET Notified = 1 - Notified WHERE TaskID = ?"
# Modifica nombre y fecha de una tarea.
QUERY_MODIFY_TASK = "UPDATE Task SET Name = ?, Date = ? WHERE TaskID = ?"
# Elimina todas las tareas completadas.
QUERY_DELETE_ALL_COMPLETED = "DELETE FROM Task WHERE Notified = 1"
# Crea la tabla principal si todavía no existe.
QUERY_CREATE_TABLE = """CREATE TABLE IF NOT EXISTS Task (
	"TaskID"  INTEGER,
	"Name"	TEXT NOT NULL,
	"Date"	TEXT NOT NULL,
	"Notified"	INTEGER NOT NULL,
	PRIMARY KEY("TaskID" AUTOINCREMENT)
);"""
# Consultas actualmente no utilizadas por la interfaz Flet.
# Vacía la tabla principal.
QUERY_VACIAR_TABLA = "DELETE FROM Task"
# Reinicia el contador interno de SQLite.
QUERY_VACIAR_CONTADOR = "DELETE FROM sqlite_sequence WHERE name = 'Task'"