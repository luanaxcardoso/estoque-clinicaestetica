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
Criei um arquivo seed.py para popular o banco de dados com dados iniciais de categoria. Para rodar, execute o seguinte comando:

```bash
python seed.py
```