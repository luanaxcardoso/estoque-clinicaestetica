Instalar as dependencias

Para atualizar o arquivo requirements.txt depois de instalar uma nova dependência
```bash
pip freeze > requirements.txt 
```
Para instalar as dependencias do requirements.txt
```bash
pip install -r requirements.txt
```


Para entrar no ambiente virtual 
```bash
conda activate clinica-estetica 
```	

Para rodar o projeto

```bash
python run.py

```

Para rodar os testes simples

```bash
python testes.py
```

Criei um arquivo seed.py para popular o banco de dados com dados iniciais de categoria. Para rodar, execute o seguinte comando:

```bash
python seed.py
```

- Foi instalado o Werkzeug, que serve para criar hash de senhas. Para criar um hash de senha, no banco de dados.
- Foi instalado colorama para colorir o terminal. 
- Foi instalado o mysql-connector-python para conectar ao banco de dados MySQL.