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

    def conectar(self):
        """Estabelece conexão com o banco MySQL"""
        try:
            conn = mysql.connector.connect(
                host=self._host,
                user=self._user,
                password=self._password,
                database=self._database
            )
            print("Conexão feita com sucesso!")
            return conn
        except mysql.connector.Error as err:
            print(f" Erro na conexão: {err}")
            return None