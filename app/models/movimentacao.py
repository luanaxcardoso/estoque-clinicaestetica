from app.database import Database
from datetime import datetime

class Movimentacao:
    def __init__(self, tipo, quantidade, usuario_id, produto_id, motivo=None):
        self.tipo = tipo  # 'entrada' ou 'saida'
        self.quantidade = quantidade
        self.usuario_id = usuario_id
        self.produto_id = produto_id
        self.motivo = motivo
        self.data_movimentacao = datetime.now()

    def salvar(self):
        db = Database()
        query = """
        INSERT INTO movimentacao 
        (tipo, quantidade, motivo, usuarios_id_usuario, produtos_id_produto)
        VALUES (%s, %s, %s, %s, %s)
        """
        params = (self.tipo, self.quantidade, self.motivo, 
                 self.usuario_id, self.produto_id)
        return db.executar(query, params, retornar_id=True)

    @staticmethod
    def listar_por_produto(produto_id):
        db = Database()
        query = """
        SELECT m.*, u.nome as usuario_nome, p.nome as produto_nome
        FROM movimentacao m
        JOIN usuarios u ON m.usuarios_id_usuario = u.id_usuario
        JOIN produtos p ON m.produtos_id_produto = p.id_produto
        WHERE m.produtos_id_produto = %s
        ORDER BY m.data_movimentacao DESC
        """
        return db.executar(query, (produto_id,), fetch_all=True)

    @staticmethod
    def listar_todas():
        db = Database()
        query = """
        SELECT m.*, u.nome as usuario_nome, p.nome as produto_nome
        FROM movimentacao m
        JOIN usuarios u ON m.usuarios_id_usuario = u.id_usuario
        JOIN produtos p ON m.produtos_id_produto = p.id_produto
        ORDER BY m.data_movimentacao DESC
        """
        return db.executar(query, fetch_all=True)