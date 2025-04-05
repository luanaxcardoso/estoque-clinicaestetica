# Modelo de Dados - Clínica Estética

## 1. USUÁRIOS (`usuarios`)
- **Chave Primária**: `id_usuario`
- **Relacionamentos**:
  - `1:N` com `movimentacao` (um usuário pode ter várias movimentações)
- **Atributos**:
  - `nivel_de_acesso`: Define permissões (administrador, gerente, biomédico, esteticista, recepcionista)
  - `status`: Ativo (S) ou Inativo (N)


## 2. CATEGORIAS (`categorias`)
- **Chave Primária**: `id_categoria`
- **Relacionamentos**:
  - `1:N` com `produtos` (uma categoria pode ter muitos produtos)


## 3. PRODUTOS (`produtos`)
- **Chave Primária**: `id_produto`
- **Relacionamentos**:
  - `N:1` com `categorias` (pertence a uma categoria)
  - `1:N` com `movimentacao` (pode ter várias movimentações)
- **Atributos**:
  - `quantidade`: Estoque atual
  - `valor_unitario`: Preço unitário
  

## 4. MOVIMENTAÇÃO (`movimentacao`)
- **Chave Primária**: `id_movimentacao`
- **Relacionamentos**:
  - `N:1` com `usuarios` (feita por um usuário)
  - `N:1` com `produtos` (referente a um produto)
- **Atributos**:
  - `tipo`: Entrada (▲) ou Saída (▼)
  - `data_movimentacao`: Data/hora do registro
  - `quantidade`: Quantidade movimentada
    - 