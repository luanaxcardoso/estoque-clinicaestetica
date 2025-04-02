from dotenv import load_dotenv
import mysql.connector  # type: ignore
import os

load_dotenv()

class Database:
    def __init__(self):
        self._host = os.getenv("DB_HOST")  
        self._user = os.getenv("DB_USER")
        self._password = os.getenv("DB_PASSWORD")
        self._database = os.getenv("DB_NAME")
        self.connection = None  
    
    def __enter__(self):
        self.conectar()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.desconectar()
        if exc_type:
            print(f"Erro: {exc_val}")
            return False
        return True
        
    def conectar(self):
        """Estabelece conexão com o banco MySQL"""
        try:
            self.connection = mysql.connector.connect(
                host=self._host,
                user=self._user,
                password=self._password,
                database=self._database
            )
            return True
        except mysql.connector.Error as err:
            print(f"Erro na conexão: {err}")
            return False
    
    def desconectar(self):
        """Fecha a conexão com o banco de dados"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            self.connection = None

    def executar(self, query, params=None, retornar_id=False, fetch_one=False, fetch_all=False):
        """Executa uma query no banco de dados"""
        if not self.connection or not self.connection.is_connected():
            if not self.conectar():
                print("Não foi possível estabelecer conexão com o banco de dados")
                return False

        cursor = None
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            
            if retornar_id:
                self.connection.commit()
                return cursor.lastrowid
            elif fetch_one:
                result = cursor.fetchone()
                return result
            elif fetch_all:
                result = cursor.fetchall()
                return result
            else:
                self.connection.commit()
                return True
                
        except mysql.connector.Error as err:
            print(f"Erro na execução da query: {err}")
            self.connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()