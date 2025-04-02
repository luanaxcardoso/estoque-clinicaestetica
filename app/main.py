import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from app.models.produto import Produto
from app.models.categoria import Categoria
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
    """Cadastra um novo produto no sistema"""
    print("\n=== CADASTRO DE PRODUTO ===")
    listar_categorias()  
    
    try:
        dados = {
            'nome': input("Nome: "),
            'descricao': input("Descrição: "),
            'categoria_id': int(input("ID da Categoria (numérico): ")),
            'quantidade': int(input("Quantidade Inicial: "))
        }
        
        produto = Produto(**dados)
        if produto_id := produto.salvar():
            print(f"Produto cadastrado com ID: {produto_id}")
        else:
            print("Falha ao cadastrar produto")
    except ValueError:
        print("Erro: Digite um número válido para ID e Quantidade")

def listar_produtos():
    """Exibe todos os produtos cadastrados"""
    print("\n=== LISTA DE PRODUTOS ===")
    if produtos := Produto.listar_todos():
        for p in produtos:
            print(f"""
ID: {p['id_produto']}
Nome: {p['nome']}
Descrição: {p['descricao']}
Categoria: {p['categoria_nome']}
Estoque: {p['quantidade']}
Cadastrado em: {p['data_cadastro']}""")
    else:
        print("Nenhum produto cadastrado")

def menu_produtos():
    """Menu de operações com produtos"""
    while True:
        print("\n=== MENU PRODUTOS ===")
        print("1. Cadastrar novo produto")
        print("2. Listar produtos")
        print("3. Voltar ao menu principal")
        
        opcao = input("Opção: ")
        
        if opcao == "1":
            cadastrar_produto()
        elif opcao == "2":
            listar_produtos()
        elif opcao == "3":
            break
        else:
            print("Opção inválida!")


def menu_categorias():
    """Menu de operações com categorias"""
    while True:
        print("\n=== MENU CATEGORIAS ===")
        print("1. Cadastrar nova categoria")
        print("2. Listar categorias")
        print("3. Voltar ao menu principal")
        
        opcao = input("Opção: ")
        
        if opcao == "1":
            cadastrar_categoria()
        elif opcao == "2":
            listar_categorias()
        elif opcao == "3":
            break
        else:
            print("Opção inválida!")


def menu_principal():
    """Menu principal do sistema"""
    while True:
        print("\n=== SISTEMA DE ESTOQUE ===")
        print("1. Gerenciar Produtos")
        print("2. Gerenciar Categorias")
        print("3. Sair")
        
        opcao = input("Opção: ")
        
        if opcao == "1":
            menu_produtos()
        elif opcao == "2":
            menu_categorias()
        elif opcao == "3":
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    if testar_conexao():
        menu_principal()