from datetime import datetime
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
    print("\n=== 🔸  CADASTRO DE PRODUTO  🔸 ===")
    listar_categorias()  
    print("=======================================================")
    print("📌 Escolha uma categoria acima para cadastrar o produto")
    print("=======================================================")
    
    try:
        dados = {
            'categorias_id_categoria': int(input("ID da Categoria: ")),
            'nome': input("Nome do produto: ").strip(),
            'descricao': input("Descrição do produto: ").strip(),
            'quantidade': max(0, int(input("Quantidade Inicial: "))),
            'valor_unitario': max(0.0, float(input("Valor Unitário (R$): ")))
        }
        
        produto = Produto(**dados)
        if produto_id := produto.salvar():
            print("\n=======================================")
            print(" 🔸  PRODUTO CADASTRADO COM SUCESSO! 🔸  ")
            print("=======================================")
            print(f"ID: {produto_id}")
            print(f"Nome: {dados['nome']}")
            print(f"Categoria ID: {dados['categorias_id_categoria']}")
            print(f"Estoque: {dados['quantidade']}")
            print(f"Valor Unitário: R$ {dados['valor_unitario']:.2f}")
            print("=======================================")
        else:
            print("\n Falha ao cadastrar produto. Verifique os dados e tente novamente.")
    except ValueError as e:
        print(f"\n Erro: {str(e)}")
        print("Certifique-se de que:")
        print("- ID da Categoria é um número válido")
        print("- Quantidade é um número inteiro positivo")
        print("- Valor Unitário é um número decimal válido")


def alterar_produto():
    print("\n=== ALTERAR PRODUTO ===")
    listar_produtos()
    
    try:
        id_produto = int(input("\n▶ ID do Produto a alterar (0 para cancelar): "))
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
            novo_valor = input(f"▶ Valor Unitário [{produto['valor_unitario']}]: ").strip()
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
            
       
        print("\n=== RESUMO DA ALTERAÇÃO ===")
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


def listar_produtos():
    print("\n=== 🔸  LISTA DE PRODUTOS  🔸 ===")
    if produtos := Produto.listar_todos():
        for p in produtos:
            print(f"""
ID: {p['id_produto']}
Nome: {p['nome']}
Descrição: {p['descricao']}
Categoria: {p['categoria_nome']} (ID: {p['categorias_id_categoria']})
Estoque: {p['quantidade']}
Valor Unitário: R$ {float(p.get('valor_unitario', 0)):.2f}
Data Cadastro: {p.get('data_cadastro', '').strftime('%d/%m/%Y %H:%M') if p.get('data_cadastro') else 'N/A'}
---------------------------------------""")
        input("\nPressione Enter para voltar...")
    else:
        print("\nNenhum produto cadastrado no sistema")
        input("Pressione Enter para voltar...")


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
        print("\n🔸 MENU PRODUTOS 🔸")
        print("1. Cadastrar produto")
        print("2. Listar produtos")
        print("3. Alterar produto")
        print("4. Deletar produto")
        print("5. Registrar entrada de estoque")
        print("6. Registrar saída de estoque")
        print("7. Ajustar estoque manualmente")
        print("8. Histórico de movimentações")
        print("9. Voltar")
        
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
            registrar_movimentacao('entrada')
        elif opcao == "6":
            registrar_movimentacao('saida')
        elif opcao == "7":
            ajustar_estoque()
        elif opcao == "8":
            listar_movimentacoes()
        elif opcao == "9":
            break
        else:
            print("Opção inválida!")

def menu_categorias():
    while True:
        print("\n🔸 MENU CATEGORIAS 🔸")
        print("1. Cadastrar categoria")
        print("2. Listar categorias")
        print("3. Alterar categoria")
        print("4. Deletar categoria")
        print("5. Voltar")
        
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
        print("\n🔸 MENU USUÁRIOS 🔸")
        print("1. Cadastrar usuário")
        print("2. Listar usuários")
        print("3. Alterar usuário")
        print("4. Deletar usuário")
        print("5. Voltar")
       
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
        print("\n🔸 MENU MOVIMENTAÇÕES 🔸")
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
            print(" Opção inválida!")

def menu_principal():
    while True:
        print("\n🔸 MENU PRINCIPAL 🔸 ")
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
            print(" Opção inválida!")

if __name__ == "__main__":
    if testar_conexao():
        menu_principal()