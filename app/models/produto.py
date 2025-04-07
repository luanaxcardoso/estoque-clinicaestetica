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
    def listar_todos(cls):
        """Lista todos os produtos ordenados por data de cadastro """
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
                    ORDER BY p.data_cadastro ASC  
                """)
                return cursor.fetchall()
            except mysql.connector.Error as err:
                print(f"Erro ao listar produtos: {err}")
                return None
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

    @classmethod
    def atualizar_produto(cls, id_produto: int, novos_dados: Dict[str, Union[str, int, float]]) -> bool:
        """Atualiza os dados de um produto existente"""
        with Database() as db:
            if not db.connection or not db.connection.is_connected():
                return False
                
            cursor = db.connection.cursor()
            try:
                
                cursor.execute("SELECT 1 FROM produtos WHERE id_produto = %s", (id_produto,))
                if not cursor.fetchone():
                    print("Produto não encontrado!")
                    return False
                
                
                campos_permitidos = ['nome', 'descricao', 'valor_unitario', 'categorias_id_categoria']
                dados_filtrados = {k: v for k, v in novos_dados.items() if k in campos_permitidos}
                
                if not dados_filtrados:
                    print("Nenhum campo válido para atualização")
                    return False
                    
                
                set_clause = ", ".join([f"{k} = %s" for k in dados_filtrados.keys()])
                valores = list(dados_filtrados.values())
                valores.append(id_produto)
                
                query = f"UPDATE produtos SET {set_clause} WHERE id_produto = %s"
                cursor.execute(query, valores)
                db.connection.commit()
                return cursor.rowcount > 0
                
            except mysql.connector.Error as err:
                print(f"Erro ao atualizar produto: {err}")
                db.connection.rollback()
                return False
            finally:
                cursor.close()

    @classmethod
    def deletar_produto(cls, id_produto: int) -> bool:
        """Remove um produto do sistema"""
        with Database() as db:
            if not db.connection or not db.connection.is_connected():
                return False
                
            cursor = db.connection.cursor()
            try:
                
                cursor.execute("SELECT 1 FROM produtos WHERE id_produto = %s", (id_produto,))
                if not cursor.fetchone():
                    print("Produto não encontrado!")
                    return False
                
                
                cursor.execute("""
                    SELECT COUNT(*) FROM movimentacao
                    WHERE produtos_id_produto = %s
                """, (id_produto,))
                
                if cursor.fetchone()[0] > 0:
                    print("Erro: Produto possui movimentações associadas")
                    return False
                
            
                cursor.execute("DELETE FROM produtos WHERE id_produto = %s", (id_produto,))
                db.connection.commit()
                
                if cursor.rowcount > 0:
                    print("Produto deletado com sucesso!")
                    return True
                return False
                
            except mysql.connector.Error as err:
                print(f"Erro ao deletar produto: {err}")
                db.connection.rollback()
                return False
            finally:
                cursor.close()