from app.database import Database
from app.models.movimentacao import Movimentacao

def testar_conexao():
    db = Database()
    if db.conectar():
        print("Conexão bem-sucedida!")
        db.desconectar()  
        return True
    print("Falha na conexão")
    return False

def listar_produtos(mostrar_no_console=True):
    """Lista produtos e opcionalmente mostra no console"""
    try:
        db = Database()
        if not db.conectar():  
            return None
            
        with db.connection.cursor(dictionary=True) as cursor:  
            cursor.execute("SELECT * FROM produtos")
            produtos = cursor.fetchall()
            
            if mostrar_no_console:
                if not produtos:
                    print("Nenhum produto encontrado na base de dados")
                else:
                    print("\nLISTA DE PRODUTOS:")
                    print("-" * 50)
                    for produto in produtos:
                        print(f"ID: {produto.get('id_produto', 'N/A')}")
                        print(f"Nome: {produto.get('nome', 'N/A')}")
                        print(f"Estoque: {produto.get('quantidade', 0)}")
                        print(f"Valor: R${produto.get('valor_unitario', 0):.2f}")
                        print("-" * 50)
            
            return produtos
            
    except Exception as e:
        print(f"Erro ao acessar o banco: {str(e)}")
        return None
    finally:
        if db.connection:
            db.desconectar()

def listar_usuarios(mostrar_no_console=True):
    """Lista todos os usuários cadastrados"""
    try:
        db = Database()
        if not db.conectar():
            return None
            
        with db.connection.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM usuarios")
            usuarios = cursor.fetchall()
            
            if mostrar_no_console:
                if not usuarios:
                    print("Nenhum usuário encontrado")
                else:
                    print("\nLISTA DE USUÁRIOS:")
                    print("-" * 50)
                    for usuario in usuarios:
                        print(f"ID: {usuario.get('id_usuario', 'N/A')}")
                        print(f"Nome: {usuario.get('nome', 'N/A')}")
                        print(f"Email: {usuario.get('email', 'N/A')}")
                        print(f"Nível: {usuario.get('nivel_de_acesso', 'N/A')}")
                        print("-" * 50)
            
            return usuarios
            
    except Exception as e:
        print(f"Erro ao listar usuários: {str(e)}")
        return None
    finally:
        if db.connection:
            db.desconectar()

if __name__ == "__main__":
    print("=== TESTE DO SISTEMA ===")
    
    
    if not testar_conexao():
        exit()
    
    
    print("\n1. Testando listagem de produtos...")
    produtos = listar_produtos()
    print(f"\nTotal de produtos encontrados: {len(produtos) if produtos else 0}")
    
    
    print("\n2. Testando listagem de usuários...")
    usuarios = listar_usuarios()
    print(f"\nTotal de usuários encontrados: {len(usuarios) if usuarios else 0}")
    

def testar_movimentacao():
    print("\nTESTE DE MOVIMENTACAO")
    
    id_produto_teste = 2
    id_usuario_teste = 2
    
    try:
        print("\n1. Testando ENTRADA no estoque")
        entrada = Movimentacao(
            tipo='entrada',
            quantidade=5,
            motivo="Reposicao de estoque",
            id_usuario=id_usuario_teste,
            id_produto=id_produto_teste
        )
        
        if id_entrada := entrada.salvar():
            print("Entrada registrada com ID:", id_entrada)
        else:
            print("Falha ao registrar entrada")
            return False
        
        print("\n2. Testando listagem de movimentacoes")
        movimentacoes = Movimentacao.listar_todas()
        if movimentacoes:
            print("Total de movimentacoes:", len(movimentacoes))
            print("Ultima movimentacao:", movimentacoes[0]['tipo'], movimentacoes[0]['quantidade'])
        else:
            print("Nenhuma movimentacao encontrada")
            return False
        
        print("\n3. Testando listagem por produto")
        mov_produto = Movimentacao.listar_por_produto(id_produto_teste)
        if mov_produto:
            print("Movimentacoes para o produto:", len(mov_produto))
        else:
            print("Nenhuma movimentacao para o produto")
            return False
        
        print("\n4. Testando SAIDA do estoque")
        saida = Movimentacao(
            tipo='saida',
            quantidade=1,
            motivo="Uso interno",
            id_usuario=id_usuario_teste,
            id_produto=id_produto_teste
        )
        
        if id_saida := saida.salvar():
            print("Saida registrada com ID:", id_saida)
        else:
            print("Falha ao registrar saida")
            return False
        
        
        return True
        
    except Exception as e:
        print("Erro durante os testes:", str(e))
        return False

if __name__ == "__main__":
    print("TESTES DO SISTEMA")
    
    if not testar_conexao():
        exit()
    
    if testar_movimentacao():
        print("\nTestes de movimentacao concluidos com sucesso")
    else:
        print("\nTestes de movimentacao com falhas")