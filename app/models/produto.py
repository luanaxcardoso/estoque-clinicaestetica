from app.database import Database
from typing import Optional, List, Dict, Union
import mysql.connector  # type: ignore
from datetime import datetime

class Produto:
    def __init__(self, 
                nome: str, 
                descricao: str, 
                categorias_id_categoria: int, 
                quantidade: int = 0,
                valor_unitario: float = 0.0):
        """
        Inicializa um novo produto
        
        Args:
            nome: Nome do produto
            descricao: Descrição detalhada
            categorias_id_categoria: ID da categoria (chave estrangeira)
            quantidade: Quantidade em estoque (default: 0)
            valor_unitario: Valor unitário do produto (default: 0.0)
        """
        self.nome = nome
        self.descricao = descricao
        self.categorias_id_categoria = categorias_id_categoria  
        self.quantidade = quantidade
        self.valor_unitario = valor_unitario
        self.data_cadastro = datetime.now()  #
    def salvar(self) -> Optional[int]:
        """
        Salva o produto no banco de dados
        
        Returns:
            int: ID do produto criado ou None em caso de erro
        """
        with Database() as db:
            if not db.connection or not db.connection.is_connected():
                print("Erro: Conexão com o banco de dados falhou")
                return None
                
            cursor = db.connection.cursor()
            try:
                db.connection.start_transaction()
                
                
                cursor.execute("SELECT id_categoria FROM categorias WHERE id_categoria = %s", 
                              (self.categorias_id_categoria,))
                if not cursor.fetchone():
                    raise ValueError(f"Categoria com ID {self.categorias_id_categoria} não encontrada")
                
               
                cursor.execute("""
                    INSERT INTO produtos 
                    (nome, descricao, categorias_id_categoria, quantidade, valor_unitario, data_cadastro)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    self.nome, 
                    self.descricao, 
                    self.categorias_id_categoria, 
                    self.quantidade,
                    self.valor_unitario,
                    self.data_cadastro
                ))
                
                id_produto = cursor.lastrowid
                db.connection.commit()
                return id_produto
                
            except mysql.connector.Error as err:
                print(f"Erro ao salvar produto: {err}")
                db.connection.rollback()
                return None
            except ValueError as ve:
                print(f"Erro de validação: {ve}")
                db.connection.rollback()
                return None
            finally:
                cursor.close()

    @classmethod
    def listar_todos(cls) -> List[Dict]:
        """Lista todos os produtos com informações da categoria"""
        with Database() as db:
            if not db.connection or not db.connection.is_connected():
                return []
                
            cursor = db.connection.cursor(dictionary=True)
            try:
                cursor.execute("""
                    SELECT 
                        p.id_produto,
                        p.nome,
                        p.descricao,
                        p.quantidade,
                        p.valor_unitario,
                        p.data_cadastro,
                        p.categorias_id_categoria,  
                        c.nome as categoria_nome
                    FROM produtos p
                    JOIN categorias c ON p.categorias_id_categoria = c.id_categoria
                    ORDER BY p.nome
                """)
                return cursor.fetchall()
            except mysql.connector.Error as err:
                print(f"Erro ao listar produtos: {err}")
                return []
            finally:
                cursor.close()

    @classmethod
    def obter_por_id(cls, id_produto: int) -> Optional[Dict]:
        """Obtém um produto específico pelo ID"""
        with Database() as db:
            if not db.connection or not db.connection.is_connected():
                return None
                
            cursor = db.connection.cursor(dictionary=True)
            try:
                cursor.execute("""
                    SELECT 
                        p.*,
                        c.nome as categoria_nome
                    FROM produtos p
                    JOIN categorias c ON p.categorias_id_categoria = c.id_categoria
                    WHERE p.id_produto = %s
                """, (id_produto,))
                return cursor.fetchone()
            except mysql.connector.Error as err:
                print(f"Erro ao obter produto: {err}")
                return None
            finally:
                cursor.close()
    @classmethod
    def listar_por_categoria(cls, id_categoria: int) -> List[Dict]:
        """Lista todos os produtos de uma categoria específica"""
        with Database() as db:
            if not db.connection or not db.connection.is_connected():
                return []
                
            cursor = db.connection.cursor(dictionary=True)
            try:
                cursor.execute("""
                    SELECT 
                        p.id_produto,
                        p.nome,
                        p.descricao,
                        p.quantidade,
                        p.valor_unitario,
                        p.data_cadastro,
                        c.nome as categoria_nome
                    FROM produtos p
                    JOIN categorias c ON p.categorias_id_categoria = c.id_categoria
                    WHERE p.categorias_id_categoria = %s
                    ORDER BY p.nome
                """, (id_categoria,))
                return cursor.fetchall()
            except mysql.connector.Error as err:
                print(f"Erro ao listar produtos por categoria: {err}")
                return []
            finally:
                cursor.close()            

    @classmethod
    def atualizar_estoque(cls, id_produto: int, quantidade: int) -> bool:
        """Atualiza a quantidade em estoque de um produto"""
        with Database() as db:
            if not db.connection or not db.connection.is_connected():
                return False
                
            cursor = db.connection.cursor()
            try:
                cursor.execute("""
                    UPDATE produtos 
                    SET quantidade = %s 
                    WHERE id_produto = %s
                """, (quantidade, id_produto))
                db.connection.commit()
                return cursor.rowcount > 0
            except mysql.connector.Error as err:
                print(f"Erro ao atualizar estoque: {err}")
                db.connection.rollback()
                return False
            finally:
                cursor.close()