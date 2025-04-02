import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from app.models.produto import Produto
from app.models.categoria import Categoria
from app.models.usuario import Usuario
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
    
    try:
        dados = {
            'nome': input("Nome: "),
            'descricao': input("Descrição: "),
            'categoria_id': int(input("ID da Categoria: ")),
            'quantidade': int(input("Quantidade Inicial: "))
        }
        
        produto = Produto(**dados)
        if produto_id := produto.salvar():
            print(f"Produto cadastrado com ID: {produto_id}")
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
            print("✅ USUÁRIO CADASTRADO COM SUCESSO!")
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
    """Menu principal simplificado"""
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

def menu_usuarios():
    while True:
        print("\n=== MENU USUÁRIOS ===")
        print("1. Cadastrar usuário")
        print("2. Listar usuários")
        print("3. Voltar")
        
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