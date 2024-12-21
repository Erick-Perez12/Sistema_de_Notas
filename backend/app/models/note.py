from app.connectionPool.pool import MySQLPool

mysql_pool = MySQLPool()

class NoteModel:
    def __init__(self, id=None, estudiante_id=None, materia=None, calificacion=None, semestre=None):
        self.id = id
        self.estudiante_id = estudiante_id
        self.materia = materia
        self.calificacion = calificacion
        self.semestre = semestre

    @classmethod
    def get_by_student_id(cls, estudiante_id):
        sql = "SELECT * FROM Notas WHERE estudiante_id = %s"
        result = mysql_pool.execute(sql, (estudiante_id,))
        notes = [cls(*note) for note in result]
        return notes

    @classmethod
    def create(cls, estudiante_id, materia, calificacion, semestre):
        sql = """
            INSERT INTO Notas (estudiante_id, materia, calificacion, semestre)
            VALUES (%s, %s, %s, %s)
        """
        mysql_pool.execute(sql, (estudiante_id, materia, calificacion, semestre), commit=True)

    @classmethod
    def update(cls, note_id, calificacion):
        sql = """
            UPDATE Notas
            SET calificacion = %s, fecha_actualizacion = CURRENT_TIMESTAMP
            WHERE id = %s
        """
        mysql_pool.execute(sql, (calificacion, note_id), commit=True)

    @classmethod
    def delete(cls, note_id):
        sql = "DELETE FROM Notas WHERE id = %s"
        mysql_pool.execute(sql, (note_id,), commit=True)
