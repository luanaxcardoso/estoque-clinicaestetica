from app.database import Database
from typing import Optional, List, Dict, Literal
import mysql.connector  # type: ignore
from datetime import datetime

class Movimentacao:
    def __init__(self, 
                tipo: Literal['entrada', 'saida'],
                quantidade: int,
                motivo: str,
                id_usuario: int,
                id_produto: int):
        """
        Inicializa uma nova movimentação de estoque
        
        Args:
            tipo: 'entrada' ou 'saida'
            quantidade: Quantidade do produto (deve ser positiva)
            motivo: Descrição/justificativa da movimentação
            id_usuario: ID do usuário que registrou a movimentação
            id_produto: ID do produto movimentado
        """
        if not isinstance(quantidade, int) or quantidade <= 0:
            raise ValueError("Quantidade deve ser um inteiro positivo")
            
        self.tipo = tipo
        self.quantidade = quantidade
        self.motivo = motivo
        self.id_usuario = id_usuario
        self.id_produto = id_produto
        self.data_movimentacao = datetime.now()

    def salvar(self) -> Optional[int]:
        """
        
        Returns:
            int: ID da movimentação criada ou None em caso de erro
        """
        with Database() as db:
            if not db.connection or not db.connection.is_connected():
                print("Erro: Não foi possível conectar ao banco de dados")
                return None
                
            cursor = db.connection.cursor()
            try:
                db.connection.start_transaction()
                
                
                cursor.execute("SELECT 1 FROM usuarios WHERE id_usuario = %s", 
                            (self.id_usuario,))
                if not cursor.fetchone():
                    raise ValueError(f"Usuário ID {self.id_usuario} não encontrado")
                
                
                cursor.execute("SELECT quantidade FROM produtos WHERE id_produto = %s", 
                            (self.id_produto,))
                produto = cursor.fetchone()
                if not produto:
                    raise ValueError(f"Produto ID {self.id_produto} não encontrado")
                
                estoque_atual = produto[0]
                
                
                if self.tipo == 'saida' and estoque_atual < self.quantidade:
                    raise ValueError(
                        f"Estoque insuficiente. Disponível: {estoque_atual}, "
                        f"Tentativa de retirada: {self.quantidade}"
                    )
                
                
                if self.tipo == 'entrada':
                    novo_estoque = self.quantidade  
                else:
                    novo_estoque = estoque_atual - self.quantidade
                
                
                cursor.execute("""
                    INSERT INTO movimentacao (
                        tipo, quantidade, motivo, 
                        data_movimentacao, usuarios_id_usuario, produtos_id_produto
                    ) VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    self.tipo,
                    self.quantidade,
                    self.motivo,
                    self.data_movimentacao,
                    self.id_usuario,
                    self.id_produto
                ))
                
                id_movimentacao = cursor.lastrowid
                
                
                cursor.execute("""
                    UPDATE produtos 
                    SET quantidade = %s 
                    WHERE id_produto = %s
                """, (novo_estoque, self.id_produto))
                
                db.connection.commit()
                return id_movimentacao
                
            except mysql.connector.Error as err:
                print(f"Erro no banco de dados: {err}")
                db.connection.rollback()
                return None
            except ValueError as ve:
                print(f"Erro de validação: {ve}")
                db.connection.rollback()
                return None
            finally:
                cursor.close()


    @classmethod
    def listar_todas(cls) -> List[Dict]:
            """Lista todas as movimentações com informações completas"""
            with Database() as db:
                if not db.connection or not db.connection.is_connected():
                    return []
                    
                cursor = db.connection.cursor(dictionary=True)
                try:
                    query = """
                    SELECT 
                        m.id_movimentacao,
                        m.tipo,
                        m.quantidade,
                        m.motivo,
                        m.data_movimentacao,
                        m.usuarios_id_usuario,
                        u.nome as usuario_nome,
                        m.produtos_id_produto,
                        p.nome as produto_nome,
                        c.nome as categoria_nome
                    FROM movimentacao m
                    JOIN usuarios u ON m.usuarios_id_usuario = u.id_usuario
                    JOIN produtos p ON m.produtos_id_produto = p.id_produto
                    JOIN categorias c ON p.categorias_id_categoria = c.id_categoria
                    ORDER BY m.data_movimentacao ASC
                    """
                    cursor.execute(query)
                    return cursor.fetchall()
                except Exception as e:
                    print(f"Erro ao listar movimentações: {str(e)}")
                    return []
                finally:
                    cursor.close()


    @classmethod
    def listar_por_produto(cls, id_produto: int) -> List[Dict]:
        """Lista movimentações de um produto específico com informações completas"""
        with Database() as db:
            if not db.connection or not db.connection.is_connected():
                return []
                
            cursor = db.connection.cursor(dictionary=True)
            try:
                query = """
                SELECT 
                    m.id_movimentacao,
                    m.tipo,
                    m.quantidade,
                    m.motivo,
                    m.data_movimentacao,
                    m.usuarios_id_usuario,
                    u.nome as usuario_nome,
                    m.produtos_id_produto,
                    p.nome as produto_nome
                FROM movimentacao m
                JOIN usuarios u ON m.usuarios_id_usuario = u.id_usuario
                JOIN produtos p ON m.produtos_id_produto = p.id_produto
                WHERE m.produtos_id_produto = %s
                ORDER BY m.data_movimentacao ASC
                """
                cursor.execute(query, (id_produto,))
                return cursor.fetchall()
            except Exception as e:
                print(f"Erro ao listar movimentações por produto: {str(e)}")
                return []
            finally:
                cursor.close()

    @classmethod
    def obter_por_id(cls, id_movimentacao: int) -> Optional[Dict]:
            """Obtém uma movimentação específica pelo ID"""
            with Database() as db:
                if not db.connection or not db.connection.is_connected():
                    return None
                    
                cursor = db.connection.cursor(dictionary=True)
                try:
                    cursor.execute("""
                        SELECT 
                            m.id_movimentacao,
                        m.tipo,
                        m.quantidade,
                        m.motivo,
                        m.data_movimentacao,
                        m.usuarios_id_usuario,  
                        m.produtos_id_produto,   
                        u.nome as usuario_nome,
                        p.nome as produto_nome
                        FROM movimentacao m
                        JOIN usuarios u ON m.usuarios_id_usuario = u.id_usuario
                        JOIN produtos p ON m.produtos_id_produto = p.id_produto
                        WHERE m.id_movimentacao = %s
                    """, (id_movimentacao,))
                    return cursor.fetchone()
                except mysql.connector.Error as err:
                    print(f"Erro ao obter movimentação: {err}")
                    return None
                finally:
                    cursor.close()    