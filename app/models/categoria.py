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
    
    
    @classmethod
    def atualizar_categoria(cls, id_categoria: int, novos_dados: Dict[str, str]) -> bool:
        """Atualiza os dados de uma categoria existente"""
        with Database() as db:
            if not db.connection or not db.connection.is_connected():
                return False
                
            cursor = db.connection.cursor()
            try:
                
                cursor.execute("SELECT 1 FROM categorias WHERE id_categoria = %s", (id_categoria,))
                if not cursor.fetchone():
                    print("Categoria não encontrada!")
                    return False
                
                
                campos_permitidos = ['nome', 'descricao']
                dados_filtrados = {k: v for k, v in novos_dados.items() if k in campos_permitidos}
                
                if not dados_filtrados:
                    print("Nenhum campo válido para atualização")
                    return False
                    
            
                set_clause = ", ".join([f"{k} = %s" for k in dados_filtrados.keys()])
                valores = list(dados_filtrados.values())
                valores.append(id_categoria)
                
                query = f"UPDATE categorias SET {set_clause} WHERE id_categoria = %s"
                cursor.execute(query, valores)
                db.connection.commit()
                return cursor.rowcount > 0
                
            except mysql.connector.Error as err:
                print(f"Erro ao atualizar categoria: {err}")
                db.connection.rollback()
                return False
            finally:
                cursor.close()
                    


    @classmethod
    def deletar_categoria(cls, id_categoria: int) -> bool:
        """Remove uma categoria (se não estiver em uso por produtos)
        
        Args:
            id_categoria: ID da categoria a ser removida
            
        Returns:
            bool: True se removida com sucesso, False caso contrário
        """
        with Database() as db:
            if not db.connection or not db.connection.is_connected():
                return False
                
            cursor = db.connection.cursor()
            try:
                
                cursor.execute("SELECT 1 FROM categorias WHERE id_categoria = %s", (id_categoria,))
                if not cursor.fetchone():
                    print(f"Erro: Categoria com ID {id_categoria} não encontrada")
                    return False
                
            
                cursor.execute("SELECT COUNT(*) FROM produtos WHERE categorias_id_categoria = %s", 
                            (id_categoria,))
                if cursor.fetchone()[0] > 0:
                    print(f"Erro: Categoria {id_categoria} está em uso por produtos")
                    return False
                    
            
                cursor.execute("DELETE FROM categorias WHERE id_categoria = %s", (id_categoria,))
                db.connection.commit()
                return cursor.rowcount > 0
                
                
            except mysql.connector.Error as err:
                print(f"Erro ao deletar categoria (ID: {id_categoria}): {err}")
                db.connection.rollback()
                return False
            finally:
                cursor.close()