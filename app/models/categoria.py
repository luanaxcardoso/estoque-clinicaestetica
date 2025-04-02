from app.database import Database
from typing import Optional, List, Dict

class Categoria:
    def __init__(self, nome: str, descricao: str):
        self.nome = nome
        self.descricao = descricao

    def salvar(self):
        with Database().conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO categorias (nome, descricao)
                VALUES (%s, %s)
            """, (self.nome, self.descricao))
            conn.commit()
            return cursor.lastrowid

    @classmethod
    def listar_todas(cls):
        with Database().conectar() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM categorias")
            return cursor.fetchall()