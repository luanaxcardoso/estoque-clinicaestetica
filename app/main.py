import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from app.models.produto import Produto
from app.models.categoria import Categoria
from app.models.usuario import Usuario
from app.models.movimentacao import Movimentacao
from app.database import Database

def testar_conexao():
    db = Database()
    if db.conectar():
        print("Conexão bem-sucedida!")
        return True
    print("Falha na conexão")
    return False


def cadastrar_categoria():
    print("\nCadastro de Categoria")
    nome = input("Nome da Categoria: ")
    descricao = input("Descrição: ")
    
    categoria = Categoria(nome, descricao)
    if categoria_id := categoria.salvar():
        print(f"Categoria cadastrada com ID: {categoria_id}")
    else:
        print("Falha ao cadastrar categoria")

def listar_categorias():
    print("\nLista de Categorias")
    if categorias := Categoria.listar_todas():
        for cat in categorias:
            print(f"\nID: {cat['id_categoria']}")
            print(f"Nome: {cat['nome']}")
            print(f"Descrição: {cat['descricao']}")
    else:
        print("Nenhuma categoria cadastrada")


def cadastrar_produto():
    print("\n=== CADASTRO DE PRODUTO ===")
    listar_categorias()  
    print("=======================================================")
    print("📌Escolha uma categoria acima para cadastrar o produto")
    print("=======================================================")
    
    try:
        dados = {
            'categoria_id': int(input("ID da Categoria: ")),
            'nome': input("Nome do produto: "),
            'descricao': input("Descrição do produto: "),
            'quantidade': int(input("Quantidade Inicial: "))
        }
        
        produto = Produto(**dados)
        if produto_id := produto.salvar():
            print("=======================================")
            print(f"Produto cadastrado com ID: {produto_id}")
            print("========================================")
        else:
            print("Falha ao cadastrar produto")
    except ValueError:
        print("Erro: Digite números válidos para ID e Quantidade")


def listar_produtos():
    print("\n=== LISTA DE PRODUTOS ===")
    if produtos := Produto.listar_todos():
        for p in produtos:
            print(f"""
ID: {p['id_produto']}
Nome: {p['nome']}
Descrição: {p['descricao']}
Categoria: {p['categoria_nome']}
Estoque: {p['quantidade']}""")
    else:
        print("Nenhum produto cadastrado")



def cadastrar_usuario():
    print("\n=== CADASTRO DE USUÁRIO ===")
    
    try:
        
        dados = {
            'nome': input("Nome: "),
            'email': input("Email: "),
            'senha': input("Senha: "),
            'status': 'S'
        }
     
        
        niveis = {
            '1': 'administrador',
            '2': 'gerente',
            '3': 'biomedico',
            '4': 'esteticista',
            '5': 'recepcionista'
        }
        
        print("\nNíveis de acesso disponíveis:")
        print("1 - Administrador")
        print("2 - Gerente")
        print("3 - Biomédico")
        print("4 - Esteticista")
        print("5 - Recepcionista")
        print("========================")
        
        while True:
            opcao = input("Escolha o nível de acesso: ")
            if opcao in niveis:
                dados['nivel_de_acesso'] = niveis[opcao]
                break
            else:
                print("Opção inválida! Digite um número entre 1 e 5.")
        
        
        usuario = Usuario(**dados)
        if usuario_id := usuario.salvar():
            print("\n====================================")
            print("  USUÁRIO CADASTRADO COM SUCESSO!")
            print("====================================")
            print(f"ID: {usuario_id}")
            print(f"Nome: {dados['nome']}")
            print(f"Email: {dados['email']}")
            print(f"Nível de acesso: {dados['nivel_de_acesso'].capitalize()}")
            print("====================================")
        else:
            print("Falha ao cadastrar usuário")
            
    except Exception as e:
        print(f"\nErro: {str(e)}")
        

def listar_usuarios():
    print("\n=== LISTA DE USUÁRIOS ===")
    if usuarios := Usuario.listar_todos():
        for u in usuarios:
            print(f"""
ID: {u['id_usuario']}
Nome: {u['nome']}
Email: {u['email']}
Nível de Acesso: {u['nivel_de_acesso'].capitalize()}""")
    else:
        print("Nenhum usuário cadastrado ou erro ao carregar a lista")


def menu_principal():
    
    while True:
        print("\n=== MENU PRINCIPAL ===")
        print("1. Gerenciar Produtos")
        print("2. Gerenciar Categorias")
        print("3. Gerenciar Usuários")
        print("4. Sair")
        
        opcao = input("Opção: ")
        
        if opcao == "1":
            menu_produtos()
        elif opcao == "2":
            menu_categorias()
        elif opcao == "3":
            menu_usuarios()
        elif opcao == "4":
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida!")

def menu_produtos():
    while True:
        print("\n=== MENU PRODUTOS ===")
        print("1. Cadastrar produto")
        print("2. Listar produtos")
        print("3. Voltar")
        
        opcao = input("Opção: ")
        
        if opcao == "1":
            cadastrar_produto()
        elif opcao == "2":
            listar_produtos()
        elif opcao == "3":
            break
        else:
            print("Opção inválida")

def menu_categorias():
    while True:
        print("\n=== MENU CATEGORIAS ===")
        print("1. Cadastrar categoria")
        print("2. Listar categorias")
        print("3. Voltar")
        
        opcao = input("Opção: ")
        
        if opcao == "1":
            cadastrar_categoria()
        elif opcao == "2":
            listar_categorias()
        elif opcao == "3":
            break
        else:
            print("Opção inválida")

def registrar_movimentacao(tipo: str):
    """Registra entrada ou saída de estoque"""
    tipo_nome = "ENTRADA" if tipo == "entrada" else "SAÍDA"
    print(f"\n=== REGISTRAR {tipo_nome} DE ESTOQUE ===")
    
    
    listar_produtos()
    
    try:
        id_produto = int(input("\nID do Produto: "))
        quantidade = int(input("Quantidade: "))
        motivo = input("Motivo: ")
        
        
        print("\nUsuários disponíveis:")
        listar_usuarios()
        id_usuario = int(input("\nID do Usuário responsável: "))
        
        mov = Movimentacao(
            tipo=tipo,
            quantidade=quantidade,
            motivo=motivo,
            id_usuario=id_usuario,
            id_produto=id_produto
        )
        
        if id_movimentacao := mov.salvar():
            print(f"\n Movimentação registrada com ID: {id_movimentacao}")
            print(f"Tipo: {tipo_nome}")
            print(f"Quantidade: {quantidade}")
            print(f"Produto ID: {id_produto}")
        else:
            print("\n Falha ao registrar movimentação")
            
    except ValueError as ve:
        print(f"\nErro: {str(ve)}")

def listar_movimentacoes():
    """Lista todas as movimentações"""
    print("\n=== HISTÓRICO DE MOVIMENTAÇÕES ===")
    
    print("\nOpções de filtro:")
    print("1. Listar todas as movimentações")
    print("2. Listar por produto específico")
    print("3. Voltar")
    
    opcao = input("Opção: ")
    
    if opcao == "1":
        movimentacoes = Movimentacao.listar_todas()
    elif opcao == "2":
        listar_produtos()
        id_produto = input("\nID do Produto (ou deixe em branco para cancelar): ")
        if id_produto:
            movimentacoes = Movimentacao.listar_por_produto(int(id_produto))
        else:
            return
    elif opcao == "3":
        return
    else:
        print("Opção inválida")
        return
    
    if movimentacoes:
        print("\n=== RESULTADOS ===")
        for mov in movimentacoes:
            print(f"""
ID Movimentação: {mov['id_movimentacao']}
Data: {mov['data_movimentacao'].strftime('%d/%m/%Y %H:%M')}
Tipo: {'Entrada' if mov['tipo'] == 'entrada' else 'Saída'}
Produto: {mov['produto_nome']} (ID: {mov['produtos_id_produto']})
Quantidade: {mov['quantidade']}
Motivo: {mov['motivo']}
Registrado por: {mov['usuario_nome']} (ID: {mov['usuarios_id_usuario']})""")
    else:
        print("Nenhuma movimentação encontrada")

def ajustar_estoque():
    """Ajuste manual de estoque com registro de movimentação"""
    print("\n=== AJUSTE DE ESTOQUE ===")
    listar_produtos()
    
    try:
        id_produto = int(input("\nID do Produto: "))
        nova_quantidade = int(input("Nova quantidade em estoque: "))
        motivo = input("Motivo do ajuste: ")
        
        
        print("\nUsuários disponíveis:")
        listar_usuarios()
        id_usuario = int(input("\nID do Usuário responsável: "))
        
        
        produto = Produto.obter_por_id(id_produto)
        if not produto:
            print("Produto não encontrado")
            return
            
        diferenca = nova_quantidade - produto['quantidade']
        
        if diferenca == 0:
            print("Quantidade não alterada")
            return
            
        tipo = 'entrada' if diferenca > 0 else 'saida'
        
        mov = Movimentacao(
            tipo=tipo,
            quantidade=abs(diferenca),
            motivo=motivo,
            id_usuario=id_usuario,
            id_produto=id_produto
        )
        
        if mov.salvar():
            print("\n Estoque atualizado e movimentação registrada com sucesso!")
            print(f"Produto: {produto['nome']}")
            print(f"Estoque anterior: {produto['quantidade']}")
            print(f"Novo estoque: {nova_quantidade}")
            print(f"Diferença: {'+' if diferenca > 0 else ''}{diferenca}")
        else:
            print("\n Falha ao atualizar estoque")
            
    except ValueError as ve:
        print(f"\nErro: {str(ve)}")


def menu_produtos():
    while True:
        print("\n=== MENU PRODUTOS ===")
        print("1. Cadastrar produto")
        print("2. Listar produtos")
        print("3. Registrar entrada de estoque")
        print("4. Registrar saída de estoque")
        print("5. Ajustar estoque manualmente")
        print("6. Histórico de movimentações")
        print("7. Voltar")
        
        opcao = input("Opção: ")
        
        if opcao == "1":
            cadastrar_produto()
        elif opcao == "2":
            listar_produtos()
        elif opcao == "3":
            registrar_movimentacao('entrada')
        elif opcao == "4":
            registrar_movimentacao('saida')
        elif opcao == "5":
            ajustar_estoque()
        elif opcao == "6":
            listar_movimentacoes()
        elif opcao == "7":
            break
        else:
            print("Opção inválida")


def menu_principal():
    
    while True:
        print("\n=== MENU PRINCIPAL ===")
        print("1. Gerenciar Produtos")
        print("2. Gerenciar Categorias")
        print("3. Gerenciar Usuários")
        print("4. Gerenciar Movimentações")
        print("5. Sair")
        
        opcao = input("Opção: ")
        
        if opcao == "1":
            menu_produtos()
        elif opcao == "2":
            menu_categorias()
        elif opcao == "3":
            menu_usuarios()
        elif opcao == "4":
            menu_movimentacoes()
        elif opcao == "5":
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida!")


def menu_movimentacoes():
    while True:
        print("\n=== MENU MOVIMENTAÇÕES ===")
        print("1. Registrar entrada de estoque")
        print("2. Registrar saída de estoque")
        print("3. Ajustar estoque manualmente")
        print("4. Histórico completo")
        print("5. Histórico por produto")
        print("6. Voltar")
        
        opcao = input("Opção: ")
        
        if opcao == "1":
            registrar_movimentacao('entrada')
        elif opcao == "2":
            registrar_movimentacao('saida')
        elif opcao == "3":
            ajustar_estoque()
        elif opcao == "4":
            listar_movimentacoes()
        elif opcao == "5":
            listar_produtos()
            id_produto = input("\nID do Produto (ou deixe em branco para cancelar): ")
            if id_produto:
                movimentacoes = Movimentacao.listar_por_produto(int(id_produto))
                if movimentacoes:
                    print("\n=== MOVIMENTAÇÕES DO PRODUTO ===")
                    for mov in movimentacoes:
                        print(f"\nData: {mov['data_movimentacao'].strftime('%d/%m/%Y %H:%M')}")
                        print(f"Tipo: {'Entrada' if mov['tipo'] == 'entrada' else 'Saída'}")
                        print(f"Quantidade: {mov['quantidade']}")
                        print(f"Motivo: {mov['motivo']}")
                        print(f"Registrado por: {mov['usuario_nome']}")
                else:
                    print("Nenhuma movimentação encontrada para este produto")
        elif opcao == "6":
            break
        else:
            print("Opção inválida")

def menu_usuarios():
    while True:
        print("\n=== MENU USUÁRIOS ===")
        print("1. Cadastrar usuário")
        print("2. Listar usuários")
        print("3. Voltar")
        print("========================") 
        
        opcao = input("Opção: ")
        
        if opcao == "1":
            cadastrar_usuario()
        elif opcao == "2":
            listar_usuarios()
        elif opcao == "3":
            break
        else:
            print("Opção inválida")

if __name__ == "__main__":
    if testar_conexao():
        menu_principal()