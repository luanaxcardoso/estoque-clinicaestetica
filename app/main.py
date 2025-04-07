from datetime import datetime
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from app.models.produto import Produto
from app.models.categoria import Categoria
from app.models.usuario import Usuario
from app.models.movimentacao import Movimentacao
from app.database import Database
from colorama import init, Fore, Style

init(autoreset=True)

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

def alterar_categoria():
    print("\n=== ALTERAR CATEGORIA ===")
    listar_categorias()
    
    try:
        id_categoria = int(input("\nID da Categoria a alterar: "))
        categoria = Categoria.listar_todas()
        categoria = next((c for c in categoria if c['id_categoria'] == id_categoria), None)
        
        if not categoria:
            print("Categoria não encontrada!")
            return
            
        print("\nDeixe em branco para manter o valor atual")
        novos_dados = {
            'nome': input(f"Nome [{categoria['nome']}]: ") or categoria['nome'],
            'descricao': input(f"Descrição [{categoria['descricao']}]: ") or categoria['descricao']
        }
        
        if Categoria.atualizar_categoria(id_categoria, novos_dados):
            print("\n Categoria atualizada com sucesso!")
        else:
            print("\n Falha ao atualizar categoria!")
            
    except ValueError:
        print("ID deve ser um número!")
    finally:
        input("\nPressione Enter para continuar...")

def deletar_categoria():
    print("\n=== DELETAR CATEGORIA ===")
    listar_categorias()
    
    try:
        id_categoria = int(input("\nID da Categoria a deletar (0 para cancelar): "))
        if id_categoria == 0:
            return
            
        if Categoria.deletar_categoria(id_categoria):
            print("\n Categoria deletada com sucesso!")
        else:
            print("\n Falha ao deletar categoria ou categoria em uso!")
    except ValueError:
        print("ID deve ser um número!")
    finally:
        input("\nPressione Enter para continuar...")


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
    print("\n=== 🔸 CADASTRO DE PRODUTO 🔸 ===")
    print("(Digite '0' a qualquer momento para cancelar)\n")
    
    listar_categorias()
    print("\n" + "="*50)
    print("📌 Escolha uma categoria ou digite 0 para voltar")
    print("="*50)
    
    try:
        
        categoria_id = input("\nID da Categoria: ").strip()
        if categoria_id == '0':
            print("\nOperação cancelada pelo usuário.")
            return
            
        dados = {
            'categorias_id_categoria': int(categoria_id),
            'nome': '',
            'descricao': '',
            'quantidade': 0,
            'valor_unitario': 0.0
        }
        
   
        nome = input("Nome do produto (ou 0 para cancelar): ").strip()
        if nome == '0':
            print("\nOperação cancelada pelo usuário.")
            return
        dados['nome'] = nome
        
   
        descricao = input("Descrição do produto (ou 0 para cancelar): ").strip()
        if descricao == '0':
            print("\nOperação cancelada pelo usuário.")
            return
        dados['descricao'] = descricao
     
        while True:
            qtd = input("Quantidade Inicial (ou 0 para cancelar): ").strip()
            if qtd == '0':
                print("\nOperação cancelada pelo usuário.")
                return
            try:
                dados['quantidade'] = max(0, int(qtd))
                break
            except ValueError:
                print("Erro: Digite um número inteiro válido!")
        
        while True:
            valor = input("Valor Unitário (R$) (ou 0 para cancelar): ").strip()
            if valor == '0':
                print("\nOperação cancelada pelo usuário.")
                return
            try:
                dados['valor_unitario'] = max(0.0, float(valor))
                break
            except ValueError:
                print("Erro: Digite um valor decimal válido (ex: 99.90)!")
        
        
        print("\n" + "="*50)
        print("CONFIRME OS DADOS DO PRODUTO:")
        print(f"Categoria ID: {dados['categorias_id_categoria']}")
        print(f"Nome: {dados['nome']}")
        print(f"Descrição: {dados['descricao']}")
        print(f"Quantidade: {dados['quantidade']}")
        print(f"Valor Unitário: R$ {dados['valor_unitario']:.2f}")
        print("="*50)
        
        confirmacao = input("\nConfirmar cadastro? (S/N): ").strip().upper()
        if confirmacao != 'S':
            print("\nCadastro cancelado!")
            return
        
      
        produto = Produto(**dados)
        if produto_id := produto.salvar():
            print("\n" + "="*50)
            print("🔸 PRODUTO CADASTRADO COM SUCESSO! 🔸")
            print("="*50)
            print(f"ID: {produto_id}")
            print(f"Nome: {dados['nome']}")
            print(f"Estoque: {dados['quantidade']}")
            print(f"Valor Unitário: R$ {dados['valor_unitario']:.2f}")
            print("="*50)
        else:
            print("\nFalha ao cadastrar produto. Verifique os dados e tente novamente.")
            
    except ValueError as e:
        print(f"\nErro: {str(e)}")
        print("Certifique-se de que:")
        print("- ID da Categoria é um número válido")
        print("- Quantidade é um número inteiro positivo")
        print("- Valor Unitário é um número decimal válido")
    except Exception as e:
        print(f"\nErro inesperado: {str(e)}")
    finally:
        input("\nPressione Enter para continuar...")

def listar_produtos():
    print(f"\n{Fore.CYAN}{Style.BRIGHT}=== 🔸  LISTA DE PRODUTOS  🔸 ==={Style.RESET_ALL}")
    if produtos := Produto.listar_todos():  
        for p in produtos:
            print(f"""
{Fore.YELLOW}ID: {Style.RESET_ALL}{p['id_produto']}
{Fore.YELLOW}Nome: {Style.RESET_ALL}{p['nome']}
{Fore.YELLOW}Descrição: {Style.RESET_ALL}{p['descricao']}
{Fore.YELLOW}Categoria: {Style.RESET_ALL}{p['categoria_nome']} {Fore.YELLOW}(ID: {Style.RESET_ALL}{p['categorias_id_categoria']})
{Fore.YELLOW}Estoque: {Style.RESET_ALL}{p['quantidade']}
{Fore.YELLOW}Valor Unitário: {Fore.GREEN}R$ {float(p.get('valor_unitario', 0)):.2f}{Style.RESET_ALL}
{Fore.YELLOW}Data Cadastro: {Style.RESET_ALL}{p.get('data_cadastro', '').strftime('%d/%m/%Y %H:%M') if p.get('data_cadastro') else 'N/A'}
{Fore.BLUE}{'-'*40}{Style.RESET_ALL}""")
    else:
        print(f"\n{Fore.RED}Nenhum produto cadastrado no sistema{Style.RESET_ALL}")
    
    input(f"\n{Fore.CYAN}Pressione Enter para voltar...{Style.RESET_ALL}")
        

def alterar_produto():
    print("\n=== ALTERAR PRODUTO ===")
    listar_produtos()
    
    try:
        id_produto = int(input("\n ID do Produto a alterar (0 para cancelar): "))
        if id_produto == 0:
            return
            
        produto = Produto.obter_por_id(id_produto)
        
        if not produto:
            print("\n Produto não encontrado!")
            input("\nPressione Enter para continuar...")
            return
            
        print("\nDeixe em branco para manter o valor atual")
        novos_dados = {}
        
        novo_nome = input(f"\n Nome [{produto['nome']}]: ").strip()
        if novo_nome:
            novos_dados['nome'] = novo_nome
        
        nova_desc = input(f"▶ Descrição [{produto['descricao']}]: ").strip()
        if nova_desc:
            novos_dados['descricao'] = nova_desc
            
        while True:
            novo_valor = input(f" Valor Unitário [{produto['valor_unitario']}]: ").strip()
            if not novo_valor:
                break
            try:
                novos_dados['valor_unitario'] = float(novo_valor)
                break
            except ValueError:
                print(" Valor inválido! Digite um número decimal (ex: 99.90)")
                
        if not novos_dados:
            print("\n Nenhuma alteração foi realizada.")
            input("\nPressione Enter para continuar...")
            return
            
        print("\n=== ALTERAÇÃO ===")
        print(f"ID do Produto: {id_produto}")
        for campo, valor in novos_dados.items():
            print(f"{campo.capitalize()}: {valor}")
        print("==========================")
        
        confirmacao = input("\n Confirmar alteração? (S/N): ").strip().upper()
        if confirmacao != 'S':
            print("\n Alteração cancelada!")
            input("\nPressione Enter para continuar...")
            return
        
        if Produto.atualizar_produto(id_produto, novos_dados):
            print("\n Produto atualizado com sucesso!")
        else:
            print("\n Falha ao atualizar produto!")
            
    except ValueError:
        print("\n Erro: ID deve ser um número inteiro!")
    except Exception as e:
        print(f"\n Erro inesperado: {str(e)}")
    finally:
        input("\nPressione Enter para continuar...")


def deletar_produto():
    print("\n=== DELETAR PRODUTO ===")
    listar_produtos()
    
    try:
        id_produto = int(input("\nID do Produto a deletar (0 para cancelar): "))
        if id_produto == 0:
            return
            
        produto = Produto.obter_por_id(id_produto)
        if not produto:
            print("Produto não encontrado!")
            return
            
        print(f"\nVocê está prestes a deletar permanentemente:")
        print(f"Produto: {produto['nome']}")
        print(f"Estoque atual: {produto['quantidade']}")
        
        confirmacao = input("\nTem certeza? (S/N): ").strip().upper()
        if confirmacao == 'S':
            if Produto.deletar_produto(id_produto):
                print("\n Produto deletado com sucesso!")
            else:
                print("\n Falha ao deletar produto!")
    except ValueError:
        print("ID deve ser um número!")
    finally:
        input("\nPressione Enter para continuar...")





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
        for k, v in niveis.items():
            print(f"{k} - {v.capitalize()}")
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
            print(" USUÁRIO CADASTRADO COM SUCESSO!")
            print("====================================")
            print(f"ID: {usuario_id}")
            print(f"Nome: {dados['nome']}")
            print(f"Email: {dados['email']}")
            print(f"Nível de acesso: {dados['nivel_de_acesso'].capitalize()}")
            print("====================================")
        else:
            print(" Falha ao cadastrar usuário")
            
    except Exception as e:
        print(f"\n Erro: {str(e)}")

def listar_usuarios():
    print("\n=== LISTA DE USUÁRIOS ===")
    if usuarios := Usuario.listar_todos():
        for u in usuarios:
            print(f"""
ID: {u['id_usuario']}
Nome: {u['nome']}
Email: {u['email']}
Nível de Acesso: {u['nivel_de_acesso'].capitalize()}
---------------------------------------""")
        input("\nPressione Enter para voltar...")
    else:
        print("Nenhum usuário cadastrado")
        input("Pressione Enter para voltar...")


def alterar_usuario():
    print("\n=== ALTERAR USUÁRIO ===")
    usuarios = Usuario.listar_todos()
    for usuario in usuarios:
        print(f"{usuario['id_usuario']}: {usuario['nome']} - {usuario['email']}")

    try:
        id_usuario = int(input("\nID do Usuário a alterar (0 para cancelar): "))
        if id_usuario == 0:
            return

        usuario = Usuario.obter_por_id(id_usuario)
        if not usuario:
            print("Usuário não encontrado!")
            return

        print("\nDeixe em branco para manter o valor atual")
        novo_nome = input(f"Nome [{usuario['nome']}]: ").strip() or usuario['nome']
        novo_email = input(f"Email [{usuario['email']}]: ").strip() or usuario['email']
        nova_senha = input("Nova senha (deixe em branco para não alterar): ").strip()
        nivel = input(f"Nível de acesso [{usuario['nivel_de_acesso']}]: ").strip() or usuario['nivel_de_acesso']

        print("\n=== RESUMO DA ALTERAÇÃO ===")
        print(f"ID: {id_usuario}")
        print(f"Nome: {novo_nome}")
        print(f"Email: {novo_email}")
        print(f"Nível de Acesso: {nivel}")
        if nova_senha:
            print("Senha: ****** (alterada)")
        print("==========================")

        confirmacao = input("Confirmar alteração? (S/N): ").strip().upper()
        if confirmacao != 'S':
            print("Alteração cancelada.")
            return

        sucesso = Usuario.alterar(
            id_usuario=id_usuario,
            nome=novo_nome,
            email=novo_email,
            nivel_de_acesso=nivel,
            senha=nova_senha if nova_senha else None
        )

        if sucesso:
            print("\nUsuário atualizado com sucesso!")
        else:
            print("\nFalha ao atualizar usuário!")

    except ValueError:
        print("ID deve ser um número!")
    except Exception as e:
        print(f"Erro inesperado: {str(e)}")
    finally:
        input("\nPressione Enter para continuar...")


def deletar_usuario():
    print("\n=== DELETAR USUÁRIO ===")
    listar_usuarios()
    
    try:
        id_usuario = int(input("\nID do Usuário a deletar (0 para cancelar): "))
        if id_usuario == 0:
            return
        
        usuario = Usuario.obter_por_id(id_usuario)
        if not usuario:
            print("Usuário não encontrado!")
            return
        
        print(f"\nVocê está prestes a deletar permanentemente:")
        print(f"Nome: {usuario['nome']}")
        print(f"Email: {usuario['email']}")
        
        confirmacao = input("\nTem certeza? (S/N): ").strip().upper()
        if confirmacao == 'S':
            if Usuario.deletar_usuario(id_usuario):
                print("\n Usuário deletado com sucesso!")
            else:
                print("\n Falha ao deletar usuário!")
        else:
            print("\n Ação cancelada pelo usuário.")
            
    except ValueError:
        print("ID deve ser um número!")
    finally:
        input("\nPressione Enter para continuar...")



def registrar_movimentacao(tipo: str):
    tipo_nome = "ENTRADA" if tipo == "entrada" else "SAÍDA"
    
    while True:  
        print("\n" + "="*50)
        print(f" REGISTRAR {tipo_nome} DE ESTOQUE".center(50))
        print("="*50)
        
       
        print("\n LISTA DE PRODUTOS DISPONÍVEIS:")
        produtos = Produto.listar_todos()
        if not produtos:
            print(" Nenhum produto cadastrado!")
            input("\nPressione Enter para voltar...")
            return
            
        for prod in produtos:
            print(f"\nID: {prod['id_produto']}")
            print(f"Nome: {prod['nome']}")
            print(f"Estoque: {prod['quantidade']}")
            print(f"Categoria: {prod.get('categoria_nome', 'N/A')}")
            print("-"*40)
        
        try:
            id_produto = int(input("\n▶ ID do Produto (0 para cancelar): "))
            if id_produto == 0:
                return
                
            produto = Produto.obter_por_id(id_produto)
            if not produto:
                print(" Produto não encontrado!")
                continue
                
            print("\n" + "="*50)
            print(f" PRODUTO SELECIONADO:")
            print(f"▪ Nome: {produto['nome']}")
            print(f"▪ Estoque Atual: {produto['quantidade']}")
            print(f"▪ Categoria: {produto.get('categoria_nome', 'N/A')}")
            print("="*50)
            
            while True:
                try:
                    quantidade = int(input("\n▶ Quantidade: "))
                    if quantidade <= 0:
                        print(" A quantidade deve ser maior que zero!")
                        continue
                        
                    if tipo == 'saida' and produto['quantidade'] < quantidade:
                        print(f" Estoque insuficiente! Disponível: {produto['quantidade']}")
                        continue
                    break
                except ValueError:
                    print(" Digite um número válido!")
            
            if tipo == 'saida':
                print("\n" + "="*50)
                print(f" CONFIRMAÇÃO DE SAÍDA")
                print(f"▪ Produto: {produto['nome']}")
                print(f"▪ Quantidade: {quantidade}")
                print(f"▪ Estoque após saída: {produto['quantidade'] - quantidade}")
                print("="*50)
                
                confirmacao = input("\n▶ Confirmar saída? (S/N): ").strip().upper()
                if confirmacao != 'S':
                    print("Operação cancelada!")
                    continue
            
            print("\n" + "="*50)
            print(" SELECIONE O USUÁRIO RESPONSÁVEL:")
            usuarios = Usuario.listar_todos()
            if not usuarios:
                print(" Nenhum usuário cadastrado!")
                input("\nPressione Enter para voltar...")
                return
                
            for user in usuarios:
                print(f"\nID: {user['id_usuario']}")
                print(f"Nome: {user['nome']}")
                print(f"Nível: {user['nivel_de_acesso'].capitalize()}")
                print("-"*40)
            
            while True:
                try:
                    id_usuario = int(input("\n▶ ID do Responsável: "))
                    usuario = next((u for u in usuarios if u['id_usuario'] == id_usuario), None)
                    if usuario:
                        break
                    print(" Usuário não encontrado!")
                except ValueError:
                    print(" Digite um número válido!")
            
            motivo = input("\n▶ Motivo: ").strip()
            
            
            print("\n" + "="*50)
            print(" RESUMO DA MOVIMENTAÇÃO")
            print(f"▪ Tipo: {tipo_nome}")
            print(f"▪ Produto: {produto['nome']} (ID: {id_produto})")
            print(f"▪ Quantidade: {quantidade}")
            print(f"▪ Responsável: {usuario['nome']} (ID: {id_usuario})")
            print(f"▪ Motivo: {motivo}")
            print("="*50)
            
            confirmacao_final = input("\n Confirmar registro? (S/N): ").strip().upper()
            if confirmacao_final != 'S':
                print("Operação cancelada!")
                continue
            
        
            mov = Movimentacao(
                tipo=tipo,
                quantidade=quantidade,
                motivo=motivo,
                id_usuario=id_usuario,
                id_produto=id_produto
            )
            
            if id_movimentacao := mov.salvar():
                produto_atualizado = Produto.obter_por_id(id_produto)
                
                print("\n" + "="*50)
                print(f" {tipo_nome} REGISTRADA COM SUCESSO!")
                print("="*50)
                print(f"▪ ID Movimentação: {id_movimentacao}")
                print(f"▪ Produto: {produto['nome']}")
                print(f"▪ Quantidade: {quantidade}")
                print(f"▪ Estoque Atualizado: {produto_atualizado['quantidade']}")
                print(f"▪ Responsável: {usuario['nome']}")
                print(f"▪ Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
                print("="*50)
                
                
                if input("\n▶ Registrar outra movimentação? (S/N): ").strip().upper() != 'S':
                    break
            else:
                print(" Falha ao registrar movimentação!")
                
        except Exception as e:
            print(f" Erro inesperado: {str(e)}")
            continue
        
    input("\nPressione Enter para voltar ao menu...")


def listar_movimentacoes():
    while True:  
        print("\n" + "="*50)
        print(" HISTÓRICO DE MOVIMENTAÇÕES".center(50))
        print("="*50)
        print("\nOpções de filtro:")
        print("1. Listar todas as movimentações")
        print("2. Listar por produto específico")
        print("3. Voltar ao menu anterior")
        
        opcao = input("\nOpção: ").strip()
        
        if opcao == "1":
            movimentacoes = Movimentacao.listar_todas()
            titulo = "TODAS AS MOVIMENTAÇÕES"
        elif opcao == "2":
            listar_produtos()
            id_produto = input("\nID do Produto (ou deixe em branco para voltar): ").strip()
            if not id_produto:
                continue
            try:
                movimentacoes = Movimentacao.listar_por_produto(int(id_produto))
                produto = Produto.obter_por_id(int(id_produto))
                titulo = f"MOVIMENTAÇÕES DO PRODUTO: {produto['nome']}" if produto else "MOVIMENTAÇÕES DO PRODUTO"
            except ValueError:
                print(" ID deve ser um número inteiro!")
                continue
        elif opcao == "3":
            return
        else:
            print(" Opção inválida!")
            continue
        
        if movimentacoes:
            print("\n" + "="*50)
            print(f" {titulo}".center(50))
            print("="*50)
            
          
            print(f"\n{'ID':<5} {'Data/Hora':<16} {'Tipo':<8} {'Produto':<20} {'Qtd':<6} {'Responsável':<20} {'Motivo'}")
            print("-"*90)
            
            for mov in movimentacoes:
                print(f"{mov['id_movimentacao']:<5} "
                      f"{mov['data_movimentacao'].strftime('%d/%m/%Y %H:%M'):<16} "
                      f"{'▲' if mov['tipo'] == 'entrada' else '▼':<8} "
                      f"{mov['produto_nome'][:18]:<20} "
                      f"{mov['quantidade']:<6} "
                      f"{mov['usuario_nome'][:18]:<20} "
                      f"{mov['motivo'][:20]}")
            
       
            entradas = sum(m['quantidade'] for m in movimentacoes if m['tipo'] == 'entrada')
            saidas = sum(m['quantidade'] for m in movimentacoes if m['tipo'] == 'saida')
            
            print("\n" + "="*50)
            print(f"📌 RESUMO ESTATÍSTICO".center(50))
            print(f"Total de entradas: {entradas} unidades")
            print(f"Total de saídas: {saidas} unidades")
            print(f"Saldo: {entradas - saidas} unidades")
            print("="*50)
        else:
            print("\n Nenhuma movimentação encontrada com os filtros selecionados")
        
        input("\nPressione Enter para continuar...")
        

def ajustar_estoque():
    print("\n=== AJUSTE DE ESTOQUE ===")
    listar_produtos()
    
    try:
      
        id_produto = int(input("\nID do Produto: "))
        produto = Produto.obter_por_id(id_produto)
        if not produto:
            print("Produto não encontrado!")
            return
            
        print(f"\n🔎 Produto Selecionado: {produto['nome']}")
        print(f"   Estoque Atual: {produto['quantidade']}")
        
        
        nova_quantidade = int(input("Nova quantidade em estoque: "))
        motivo = input("Motivo do ajuste: ")
        
     
        print("\n=== USUÁRIOS DISPONÍVEIS ===")
        usuarios = Usuario.listar_todos()
        if not usuarios:
            print(" Nenhum usuário cadastrado!")
            return
            
        for user in usuarios:
            print(f"ID: {user['id_usuario']} | Nome: {user['nome']} | Nível: {user['nivel_de_acesso']}")
        
        id_usuario = int(input("\nID do Usuário Responsável: "))
        
        
        usuario_responsavel = next((u for u in usuarios if u['id_usuario'] == id_usuario), None)
        if not usuario_responsavel:
            print(" Usuário não encontrado!")
            return
        
        diferenca = nova_quantidade - produto['quantidade']
        
        if diferenca == 0:
            print("Quantidade não alterada")
            return
            
        tipo = 'entrada' if diferenca > 0 else 'saida'
        quantidade_ajuste = abs(diferenca)
        
       
        print(f"\n CONFIRMAR AJUSTE:")
        print(f"Produto: {produto['nome']} (ID: {id_produto})")
        print(f"Tipo: {'Entrada' if tipo == 'entrada' else 'Saída'}")
        print(f"Quantidade: {quantidade_ajuste}")
        print(f"Estoque anterior: {produto['quantidade']}")
        print(f"Novo estoque: {nova_quantidade}")
        print(f"Responsável: {usuario_responsavel['nome']} (ID: {id_usuario})")
        print(f"Motivo: {motivo}")
        
        confirmacao = input("\nConfirmar ajuste? (S/N): ").strip().upper()
        if confirmacao != 'S':
            print("Operação cancelada!")
            return
        
        
        mov = Movimentacao(
            tipo=tipo,
            quantidade=quantidade_ajuste,
            motivo=motivo,
            id_usuario=id_usuario,
            id_produto=id_produto
        )
        
        if id_movimentacao := mov.salvar():
            produto_atualizado = Produto.obter_por_id(id_produto)
            
            print("\n" + "="*50)
            print(" AJUSTE DE ESTOQUE REGISTRADO COM SUCESSO")
            print("="*50)
            print(f"▪ ID Movimentação: {id_movimentacao}")
            print(f"▪ Produto: {produto['nome']} (ID: {id_produto})")
            print(f"▪ Tipo: {'Entrada' if tipo == 'entrada' else 'Saída'}")
            print(f"▪ Quantidade Ajustada: {quantidade_ajuste}")
            print(f"▪ Estoque Anterior: {produto['quantidade']}")
            print(f"▪ Novo Estoque: {produto_atualizado['quantidade']}")
            print(f"▪ Responsável: {usuario_responsavel['nome']} (ID: {id_usuario})")
            print(f"▪ Motivo: {motivo}")
            print(f"▪ Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
            print("="*50)
        else:
            print(" Falha ao registrar ajuste de estoque!")
            
    except ValueError:
        print(" Erro: Valor inválido! Certifique-se de digitar números para ID e quantidade.")
    except Exception as e:
        print(f" Erro inesperado: {str(e)}")
    finally:
        input("\nPressione Enter para continuar...")
        

def menu_produtos():
    while True:
        print(f"\n{Fore.CYAN}{Style.BRIGHT}🔸 MENU PRODUTOS 🔸{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}1. {Fore.MAGENTA}Cadastrar produto")
        print(f"{Fore.YELLOW}2. {Fore.MAGENTA}Listar produtos")
        print(f"{Fore.YELLOW}3. {Fore.MAGENTA}Alterar produto")
        print(f"{Fore.YELLOW}4. {Fore.MAGENTA}Deletar produto")
        print(f"{Fore.RED}5. Voltar{Style.RESET_ALL}")

        opcao = input("Opção: ")
        
        if opcao == "1":
            cadastrar_produto()
        elif opcao == "2":
            listar_produtos()
        elif opcao == "3":
            alterar_produto()
        elif opcao == "4":
            deletar_produto()
        elif opcao == "5":
            
            break
        else:
            print("Opção inválida!")


def menu_categorias():
    while True:
        print(f"\n{Fore.CYAN}{Style.BRIGHT}🔸 MENU CATEGORIAS 🔸{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}1. {Fore.MAGENTA}Cadastrar categoria")
        print(f"{Fore.YELLOW}2. {Fore.MAGENTA}Listar categorias")
        print(f"{Fore.YELLOW}3. {Fore.MAGENTA}Alterar categoria")
        print(f"{Fore.YELLOW}4. {Fore.MAGENTA}Deletar categoria")
        print(f"{Fore.RED}5. Voltar{Style.RESET_ALL}")
      
        opcao = input("Opção: ")
        
        if opcao == "1":
            cadastrar_categoria()
        elif opcao == "2":
            listar_categorias()
        elif opcao == "3":
            alterar_categoria()
        elif opcao == "4":
            deletar_categoria()
        elif opcao == "5":
            break
        else:
            print("Opção inválida!")
            

def menu_usuarios():
    while True:
        print(f"\n{Fore.CYAN}{Style.BRIGHT}🔸 MENU USUÁRIOS 🔸{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}1. {Fore.MAGENTA}Cadastrar usuário")
        print(f"{Fore.YELLOW}2. {Fore.MAGENTA}Listar usuários")
        print(f"{Fore.YELLOW}3. {Fore.MAGENTA}Alterar usuário")
        print(f"{Fore.YELLOW}4. {Fore.MAGENTA}Deletar usuário")
        print(f"{Fore.RED}5. Voltar{Style.RESET_ALL}")

        opcao = input("Opção: ")
        
        if opcao == "1":
            cadastrar_usuario()
        elif opcao == "2":
            listar_usuarios()
        elif opcao == "3":
            alterar_usuario()
        elif opcao == "4":
            deletar_usuario()
        elif opcao == "5":
            break
        else:
            print(" Opção inválida!")


def menu_movimentacoes():
    while True:
        print(f"\n{Fore.CYAN}{Style.BRIGHT}🔸 MENU MOVIMENTAÇÕES 🔸{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}1. {Fore.MAGENTA}Registrar entrada de estoque")
        print(f"{Fore.YELLOW}2. {Fore.MAGENTA}Registrar saída de estoque")
        print(f"{Fore.YELLOW}3. {Fore.MAGENTA}Ajustar estoque manualmente")
        print(f"{Fore.YELLOW}4. {Fore.MAGENTA}Histórico completo")
        print(f"{Fore.YELLOW}5. {Fore.MAGENTA}Histórico por produto")
        print(f"{Fore.RED}6. Voltar{Style.RESET_ALL}")

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
            print(" Opção inválida!")



def mostrar_menu(titulo, opcoes):
    """Função genérica para exibir menus com cores"""
    print(f"\n{Fore.BLUE}{Style.BRIGHT}🔸 {titulo.upper()} 🔸{Style.RESET_ALL}")
    
    for i, (opcao, _) in enumerate(opcoes, 1):
        print(f"{Fore.YELLOW}{i}. {Fore.MAGENTA}{opcao}")
    
    print(f"{Fore.RED}{len(opcoes)+1}. Sair{Style.RESET_ALL}")
    return input(f"\n{Fore.GREEN}▶ Opção: {Style.RESET_ALL}")
def menu_principal():
    while True:
        opcoes = [
            ("Gerenciar PRODUTOS", menu_produtos),
            ("Gerenciar CATEGORIAS", menu_categorias),
            ("Gerenciar USUÁRIOS", menu_usuarios),
            ("Gerenciar MOVIMENTAÇÕES", menu_movimentacoes)
        ]
        
        opcao = mostrar_menu("MENU PRINCIPAL", opcoes)
        
        try:
            if opcao == str(len(opcoes)+1):
                print("\nSaindo do sistema...")
                break
            elif opcao.isdigit() and 0 < int(opcao) <= len(opcoes):
                opcoes[int(opcao)-1][1]()  
            else:
                print("\n Opção inválida!")
        except Exception as e:
            print(f"\n Erro: {str(e)}")


if __name__ == "__main__":
    if testar_conexao():
        menu_principal()