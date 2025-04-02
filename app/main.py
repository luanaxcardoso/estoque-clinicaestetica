from app.database import Database

def testar_conexao():
    db = Database()
    conn = db.conectar()
    
    if conn:
        print("Conexão bem-sucedida!")
        conn.close()
    else:
        print("Falha na conexão")

if __name__ == "__main__":
    testar_conexao()