from app.database import Database

def listar_produtos():
    with Database().conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM produtos")
        return cursor.fetchall()