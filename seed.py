from app.models.categoria import Categoria

CATEGORIAS_INICIAIS = [
    ("Medicamentos e Injetáveis", "Produtos injetáveis como Botox e preenchedores"),
    ("Toxina botulínica (Botox®)", "Neuromoduladores e toxinas botulínicas"),
    ("Ácido hialurônico", "Preenchedores faciais e corporais"),
    ("Anestésicos tópicos", "Cremes anestésicos como lidocaína"),
    ("Vitaminas para mesoterapia", "Complexos vitamínicos para terapia"),
    ("Cosméticos e Dermocosméticos", "Produtos para cuidados diários"),
    ("Equipamentos e Consumíveis", "Materiais descartáveis e equipamentos"),
    ("Produtos para Depilação", "Itens para procedimentos de depilação"),
    ("Produtos para Limpeza", "Higienização e antissépticos")
]

def popular_categorias():
    for nome, descricao in CATEGORIAS_INICIAIS:
        cat = Categoria(nome, descricao)
        if cat.salvar():
            print(f"Categoria '{nome}' cadastrada!")
        else:
            print(f"Falha ao cadastrar '{nome}'")

if __name__ == "__main__":
    print("Cadastrando categorias iniciais...")
    popular_categorias()
    print("Concluído!")