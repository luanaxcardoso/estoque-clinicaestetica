from app.database import Database
from typing import Optional, List, Dict
import mysql.connector  # type: ignore

class Produto:
    def __init__(self, nome: str, descricao: str, categoria_id: int, quantidade: int = 0):
        self.nome = nome
        self.descricao = descricao
        self.categoria_id = categoria_id
        self.quantidade = quantidade

    def salvar(self) -> Optional[int]:
        with Database() as db:
            if not db.connection or not db.connection.is_connected():
                return None
                
            cursor = db.connection.cursor()
            try:
                cursor.execute("""
                    INSERT INTO produtos (nome, descricao, categorias_id_categoria, quantidade)
                    VALUES (%s, %s, %s, %s)
                """, (self.nome, self.descricao, self.categoria_id, self.quantidade))
                db.connection.commit()
                return cursor.lastrowid
            except mysql.connector.Error as err:
                print(f"Erro ao salvar produto: {err}")
                db.connection.rollback()
                return None
            finally:
                cursor.close()

    @classmethod
    def listar_todos(cls) -> List[Dict]:
        with Database() as db:
            if not db.connection or not db.connection.is_connected():
                return []
                
            cursor = db.connection.cursor(dictionary=True)
            try:
                cursor.execute("""
                    SELECT p.*, c.nome as categoria_nome 
                    FROM produtos p
                    JOIN categorias c ON p.categorias_id_categoria = c.id_categoria
                """)
                return cursor.fetchall()
            except mysql.connector.Error as err:
                print(f"Erro ao listar produtos: {err}")
                return []
            finally:
                cursor.close()
