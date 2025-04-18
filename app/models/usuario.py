from typing import Dict, Optional, List
from app.database import Database
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario:
    def __init__(self, nome: str, email: str, senha: str, nivel_de_acesso: str, status: str = 'S'):
        self.nome = nome
        self.email = email
        self.senha = generate_password_hash(senha)
        self.nivel_de_acesso = nivel_de_acesso
        self.status = status

    def salvar(self) -> Optional[int]:
        """Salva o usuário no banco de dados e retorna o ID gerado"""
        db = Database()
        try:
            if not db.conectar():
                print("Erro: Não foi possível conectar ao banco de dados")
                return None
                
            cursor = db.connection.cursor(dictionary=True)
            query = """
            INSERT INTO usuarios 
            (nome, email, senha, nivel_de_acesso, status)
            VALUES (%s, %s, %s, %s, %s)
            """
            params = (self.nome, self.email, self.senha, 
                     self.nivel_de_acesso, self.status)
            
            cursor.execute(query, params)
            db.connection.commit()
            return cursor.lastrowid
            
        except Exception as e:
            print(f"Erro ao salvar usuário: {str(e)}")
            if db.connection:
                db.connection.rollback()
            return None
        finally:
            if db.connection:
                cursor.close()
            db.desconectar()

    @staticmethod
    def listar_todos() -> List[Dict]:
        """Lista todos os usuários ativos"""
        db = Database()
        try:
            if not db.conectar():
                print("Erro: Não foi possível conectar ao banco de dados")
                return []
                
            cursor = db.connection.cursor(dictionary=True)
            query = """
            SELECT id_usuario, nome, email, nivel_de_acesso, status
            FROM usuarios 
            WHERE status = 'S'
            """
            cursor.execute(query)
            return cursor.fetchall()
            
        except Exception as e:
            print(f"Erro ao listar usuários: {str(e)}")
            return []
        finally:
            if db.connection:
                cursor.close()
            db.desconectar()

    @staticmethod
    def obter_por_id(id_usuario: int) -> Optional[Dict]:
        """Obtém um usuário pelo ID"""
        db = Database()
        try:
            if not db.conectar():
                print("Erro: Não foi possível conectar ao banco de dados")
                return None
                
            cursor = db.connection.cursor(dictionary=True)
            query = """
            SELECT id_usuario, nome, email, nivel_de_acesso, status
            FROM usuarios 
            WHERE id_usuario = %s AND status = 'S'
            """
            cursor.execute(query, (id_usuario,))
            return cursor.fetchone()
            
        except Exception as e:
            print(f"Erro ao obter usuário: {str(e)}")
            return None
        finally:
            if db.connection:
                cursor.close()
            db.desconectar()

    @staticmethod
    def verificar_credenciais(email: str, senha: str) -> Optional[Dict]:
        """Verifica se as credenciais são válidas"""
        db = Database()
        try:
            if not db.conectar():
                print("Erro: Não foi possível conectar ao banco de dados")
                return None
                
            cursor = db.connection.cursor(dictionary=True)
            query = """
            SELECT id_usuario, nome, email, senha, nivel_de_acesso
            FROM usuarios 
            WHERE email = %s AND status = 'S'
            """
            cursor.execute(query, (email,))
            usuario = cursor.fetchone()
            
            if usuario and check_password_hash(usuario['senha'], senha):
                return usuario
            return None
            
        except Exception as e:
            print(f"Erro ao verificar credenciais: {str(e)}")
            return None
        finally:
            if db.connection:
                cursor.close()
            db.desconectar()

    @staticmethod
    def alterar(id_usuario: int, nome: str, email: str, nivel_de_acesso: str, senha: Optional[str] = None) -> bool:
        """Altera os dados de um usuário existente"""
        db = Database()
        try:
            if not db.conectar():
                print("Erro: Não foi possível conectar ao banco de dados")
                return False
                
            cursor = db.connection.cursor(dictionary=True)
            
           
            if senha:
                senha_hash = generate_password_hash(senha)
                query = """
                UPDATE usuarios 
                SET nome = %s, email = %s, nivel_de_acesso = %s, senha = %s
                WHERE id_usuario = %s AND status = 'S'
                """
                params = (nome, email, nivel_de_acesso, senha_hash, id_usuario)
            else:
                query = """
                UPDATE usuarios 
                SET nome = %s, email = %s, nivel_de_acesso = %s
                WHERE id_usuario = %s AND status = 'S'
                """
                params = (nome, email, nivel_de_acesso, id_usuario)
            
            cursor.execute(query, params)
            db.connection.commit()
            return cursor.rowcount > 0
            
        except Exception as e:
            print(f"Erro ao alterar usuário: {str(e)}")
            if db.connection:
                db.connection.rollback()
            return False
        finally:
            if db.connection:
                cursor.close()
            db.desconectar()

    @staticmethod
    def deletar(id_usuario: int) -> bool:
        """Marca um usuário como inativo (deleção lógica)"""
        db = Database()
        try:
            if not db.conectar():
                print("Erro: Não foi possível conectar ao banco de dados")
                return False
                
            cursor = db.connection.cursor(dictionary=True)
            query = """
            UPDATE usuarios 
            SET status = 'N'
            WHERE id_usuario = %s AND status = 'S'
            """
            cursor.execute(query, (id_usuario,))
            db.connection.commit()
            return cursor.rowcount > 0
            
        except Exception as e:
            print(f"Erro ao deletar usuário: {str(e)}")
            if db.connection:
                db.connection.rollback()
            return False
        finally:
            if db.connection:
                cursor.close()
            db.desconectar()


    @staticmethod
    def alterar_usuario (id_usuario: int, nome: str, email: str, nivel_de_acesso: str, senha: Optional[str] = None) -> bool:
        """Altera os dados de um usuário existente"""
        db = Database()
        try:
            if not db.conectar():
                print("Erro: Não foi possível conectar ao banco de dados")
                return False
                
            cursor = db.connection.cursor(dictionary=True)
            
            if senha:
                senha_hash = generate_password_hash(senha)
                query = """
                UPDATE usuarios 
                SET nome = %s, email = %s, nivel_de_acesso = %s, senha = %s
                WHERE id_usuario = %s AND status = 'S'
                """
                params = (nome, email, nivel_de_acesso, senha_hash, id_usuario)
            else:
                query = """
                UPDATE usuarios 
                SET nome = %s, email = %s, nivel_de_acesso = %s
                WHERE id_usuario = %s AND status = 'S'
                """
                params = (nome, email, nivel_de_acesso, id_usuario)
            
            cursor.execute(query, params)
            db.connection.commit()
            return cursor.rowcount > 0
            
        except Exception as e:
            print(f"Erro ao alterar usuário: {str(e)}")
            if db.connection:
                db.connection.rollback()
            return False
        finally:
            if db.connection:
                cursor.close()
            db.desconectar()
    
    @staticmethod
    def deletar_usuario (id_usuario: int) -> bool:
        """Marca um usuário como inativo (deleção lógica)"""
        db = Database()
        try:
            if not db.conectar():
                print("Erro: Não foi possível conectar ao banco de dados")
                return False
                
            cursor = db.connection.cursor(dictionary=True)
            query = """
            UPDATE usuarios 
            SET status = 'N'
            WHERE id_usuario = %s AND status = 'S'
            """
            cursor.execute(query, (id_usuario,))
            db.connection.commit()
            return cursor.rowcount > 0
            
        except Exception as e:
            print(f"Erro ao deletar usuário: {str(e)}")
            if db.connection:
                db.connection.rollback()
            return False
        finally:
            if db.connection:
                cursor.close()
            db.desconectar()