from app.database import Database
from typing import Optional, List, Dict
import mysql.connector  # type: ignore

class Categoria:
    def __init__(self, nome: str, descricao: str):
        self.nome = nome
        self.descricao = descricao

    def salvar(self) -> Optional[int]:
        """Salva uma nova categoria no banco de dados e retorna o ID gerado"""
        with Database() as db:
            if not db.connection or not db.connection.is_connected():
                return None
                
            cursor = db.connection.cursor()
            try:
                cursor.execute("""
                    INSERT INTO categorias (nome, descricao)
                    VALUES (%s, %s)
                """, (self.nome, self.descricao))
                db.connection.commit()
                return cursor.lastrowid
            except mysql.connector.Error as err:
                print(f"Erro ao salvar categoria: {err}")
                db.connection.rollback()
                return None
            finally:
                cursor.close()

    @classmethod
    def listar_todas(cls) -> Optional[List[Dict]]:
        """Retorna todas as categorias cadastradas ou None em caso de erro"""
        with Database() as db:
            if not db.connection or not db.connection.is_connected():
                return None
                
            cursor = db.connection.cursor(dictionary=True)
            try:
                cursor.execute("SELECT * FROM categorias")
                return cursor.fetchall()
            except mysql.connector.Error as err:
                print(f"Erro ao listar categorias: {err}")
                return None
            finally:
                cursor.close()