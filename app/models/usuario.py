from app.database import Database
from werkzeug.security import generate_password_hash

class Usuario:
    def __init__(self, nome, email, senha, nivel_de_acesso, status='S'):
        self.nome = nome
        self.email = email
        self.senha = generate_password_hash(senha)
        self.nivel_de_acesso = nivel_de_acesso
        self.status = status

    def salvar(self):
        db = Database()
        try:
            query = """
            INSERT INTO usuarios 
            (nome, email, senha, nivel_de_acesso, status)
            VALUES (%s, %s, %s, %s, %s)
            """
            params = (self.nome, self.email, self.senha, 
                     self.nivel_de_acesso, self.status)
            return db.executar(query, params, retornar_id=True)
        except Exception as e:
            print(f"Erro ao salvar usuário: {str(e)}")
            return False
        finally:
            db.desconectar()

    @staticmethod
    def listar_todos():
        db = Database()
        try:
            query = """
            SELECT id_usuario, nome, email, nivel_de_acesso 
            FROM usuarios 
            WHERE status = 'S'
            """
            return db.executar(query, fetch_all=True)
        except Exception as e:
            print(f"Erro ao listar usuários: {str(e)}")
            return None
        finally:
            db.desconectar()