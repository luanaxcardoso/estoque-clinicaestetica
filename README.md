## Projeto Integrado - UNIFEOB
## 🚀 Sistema de Gerenciamento de Estoque de uma clínica estética

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![MySQL](https://img.shields.io/badge/MySQL-8.0%2B-orange)


## 🔧 Instalação

1. Clone o repositório:
    ```bash
    git clone https://github.com/luanaxcardoso/estoque-clinicaestetica
    cd estoque-clinicaestetica
    ```
2. Crie um ambiente virtual:
    ```bash
    conda create -n clinica-estetica python=3.8
    conda activate clinica-estetica
    ```
3. Instale as dependências:
    ```bash 
    pip install -r requirements.txt
    ```
4. Configure o banco de dados MySQL e crie as tabelas necessárias.

----------------------------------------------------------------------------

Sistema para gestão de estoque de uma clínica estética, utilizando Python e MySQL. O sistema é projetado para facilitar o gerenciamento de produtos, categorias,usuarios e movimentações de estoque.

## ✨ Funcionalidades

- **Gestão de Produtos**
  - Cadastro de produtos
  - Edição de produtos
  - Busca e Listagem de produtos
  - Exclusão de produtos
  - Associação a categorias
  

- **Gestão de Categorias**
  - Cadastro de categorias
  - Edição de categorias
  - Exclusão de categorias
  - Listagem de categorias
  - Hierarquia de produtos dentro de categorias

- **Gestão de Movimentação de Estoque**
  - Cadastro de entradas/saídas
  - Listagem de movimentações


- **Gestão de Usuários**
  - Cadastro de usuários
  - Listagem de usuários
  - Edição de usuários
  - Exclusão de usuários
  - Hash de senhas


## 🛠️ Tecnologias

- **Backend**:
  - Python 3.8+
  - MySQL 8.0+
  - Werkzeug 3.1.3 (para hash de senhas)

- **Arquitetura**:
  - Programação Orientada a Objetos

  
## 📂 Principais características:
- **Navegação intuitiva** 
- **Controle de fluxo** 
- **CRUD** 
- **Organização por models**
- **Conexão com o banco de dados**
 