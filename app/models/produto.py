from app.database import Database
from typing import Optional, List, Dict

class Produto:
    def __init__(self, nome: str, descricao: str, categoria_id: int, quantidade: int = 0):
        self.nome = nome
        self.descricao = descricao
        self.categoria_id = categoria_id
        self.quantidade = quantidade

    def salvar(self) -> Optional[int]:
        
        with Database().conectar() as conn:
            if not conn:
                return None
                
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO produtos (nome, descricao, categorias_id_categoria, quantidade)
                    VALUES (%s, %s, %s, %s)
                """, (self.nome, self.descricao, self.categoria_id, self.quantidade))
                conn.commit()
                return cursor.lastrowid
            except mysql.connector.Error as err: # type: ignore
                print(f"Erro ao salvar produto: {err}")
                conn.rollback()
                return None

    @classmethod
    def listar_todos(cls) -> List[Dict]:
       
        with Database().conectar() as conn:
            if not conn:
                return []
                
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT p.*, c.nome as categoria_nome 
                FROM produtos p
                JOIN categorias c ON p.categorias_id_categoria = c.id_categoria
            """)
            return cursor.fetchall()