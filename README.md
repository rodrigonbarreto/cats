# Adote um gato
## É um projeto de exemplo DE POS GRADUACAO DA PUC-RJ

Esta aplicação usa a API pública [TheCatAPI](https://api.thecatapi.com) para buscar informações sobre gatos.

## Tecnologias utilizadas

- Python 3.10
- FastAPI
- Uvicorn
- SQLModel
- Pydantic
- Httpx

## Como executar com Docker

### Pré-requisitos

- Docker
- Docker Compose

### Passos para execução

1. Clone o repositório

2. Construa e inicie os contêineres:

```bash
# Iniciar aplicação
docker compose up --build

# Ou use -d para rodar em segundo plano
docker compose up --build -d
```

3. Acesse a aplicação:

```
http://localhost:8181
```

4. Para parar a aplicação:

```bash
docker compose down
```

## Desenvolvimento local sem Docker

1. Crie e ative um ambiente virtual:

```bash
# Criar ambiente virtual
python -m venv cats

# Ativar no Linux/Mac
source cats/bin/activate  

# Ou ativar no Windows
.\cats\Scripts\activate
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Execute a aplicação:

```bash
# Usando uvicorn diretamente
uvicorn main:app --host 0.0.0.0 --port 8181 --log-level info --reload

# Ou usando o script principal
python main.py
```

## Swagger URL
http://localhost:8181/docs

## Gerenciamento do Banco de Dados

### Com Docker

Para criar ou recriar o banco de dados usando Docker:

```bash
# Criar ou recriar o banco de dados 
docker compose run --rm cats_app python create_tables.py
```

### Localmente

Para recriar o banco de dados localmente:

```bash
# Remover o banco de dados existente (se necessário)
rm cats.db

# Criar o banco de dados
python create_tables.py
```

## API Pública de Gatos

A aplicação consome a API pública do TheCatAPI:

URL base: `https://api.thecatapi.com/v1/images/search?limit=10`

## Verificação da versão do Python

Esta aplicação foi desenvolvida e testada com Python 3.10.1