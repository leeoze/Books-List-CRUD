# 📚 API REST Assíncrona de Livros — FastAPI

API REST assíncrona construída com FastAPI, demonstrando os quatro métodos HTTP principais (GET, POST, PUT, DELETE) com `async def` e `await`.

---

## 🗂️ Estrutura do Projeto

```
projeto/
├── main.py        # Código completo da API
└── README.md      # Este arquivo
```

---

## ⚙️ Pré-requisitos

- Python **3.12.10**
- pip

---

## 🚀 Instalação e Execução

### 1. Clone ou baixe o projeto

```bash
# Se estiver usando git:
git clone <https://github.com/leeoze/Books-List-CRUD>
cd Books-List-CRUD

# Ou simplesmente coloque main.py em uma pasta e entre nela
```

### 2. Crie e ative um ambiente virtual (recomendado)

```bash
# Criar o ambiente virtual
python -m venv venv

# Ativar no Linux/macOS:
source venv/bin/activate

# Ativar no Windows:
venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install fastapi uvicorn
```

> **Por que esses dois pacotes?**
> - `fastapi` — o framework da API
> - `uvicorn` — servidor ASGI que executa a aplicação de forma assíncrona

### 4. Execute a aplicação

```bash
uvicorn main:app --reload
parar aplicação: CTRL+C
```

> `--reload` reinicia o servidor automaticamente ao salvar alterações. **Use apenas em desenvolvimento.**

A API estará disponível em: **http://127.0.0.1:8000**

---

## 📖 Documentação Automática

O FastAPI gera documentação interativa automaticamente:

| Interface | URL |
|-----------|-----|
| Swagger UI (interativo) | http://127.0.0.1:8000/docs |
| ReDoc (leitura) | http://127.0.0.1:8000/redoc |

---

## 🧪 Testando os Endpoints

A API já começa com 3 livros pré-cadastrados (IDs 1, 2 e 3).

---

### GET `/livros` — Listar todos os livros

```bash
curl -X GET http://127.0.0.1:8000/livros
```

**Resposta esperada (200 OK):**
```json
[
  {"id": 1, "titulo": "Clean Code", "autor": "Robert C. Martin", "ano": 2008, "disponivel": true},
  {"id": 2, "titulo": "O Programador Pragmático", "autor": "Andrew Hunt", "ano": 1999, "disponivel": true},
  {"id": 3, "titulo": "Domain-Driven Design", "autor": "Eric Evans", "ano": 2003, "disponivel": true}
]
```

---

### GET `/livros/{id}` — Buscar um livro pelo ID

```bash
# Livro existente
curl -X GET http://127.0.0.1:8000/livros/1

# Livro inexistente (deve retornar 404)
curl -X GET http://127.0.0.1:8000/livros/999
```

**Resposta de sucesso (200 OK):**
```json
{"id": 1, "titulo": "Clean Code", "autor": "Robert C. Martin", "ano": 2008, "disponivel": true}
```

**Resposta de erro (404 Not Found):**
```json
{"detail": "Livro com ID 999 não encontrado."}
```

---

### POST `/livros` — Criar um novo livro

```bash
curl -X POST http://127.0.0.1:8000/livros \
  -H "Content-Type: application/json" \
  -d '{"titulo": "The Pragmatic Programmer", "autor": "Dave Thomas", "ano": 2019, "disponivel": true}'
```

**Resposta esperada (201 Created):**
```json
{"id": 4, "titulo": "The Pragmatic Programmer", "autor": "Dave Thomas", "ano": 2019, "disponivel": true}
```

**Teste de validação — campo obrigatório ausente (deve retornar 422):**
```bash
curl -X POST http://127.0.0.1:8000/livros \
  -H "Content-Type: application/json" \
  -d '{"titulo": "Sem autor"}'
```

---

### PUT `/livros/{id}` — Atualizar um livro

Você pode enviar apenas os campos que deseja alterar (atualização parcial):

```bash
# Atualizar apenas a disponibilidade
curl -X PUT http://127.0.0.1:8000/livros/1 \
  -H "Content-Type: application/json" \
  -d '{"disponivel": false}'

# Atualizar título e ano
curl -X PUT http://127.0.0.1:8000/livros/2 \
  -H "Content-Type: application/json" \
  -d '{"titulo": "Novo Título", "ano": 2024}'

# Livro inexistente (deve retornar 404)
curl -X PUT http://127.0.0.1:8000/livros/999 \
  -H "Content-Type: application/json" \
  -d '{"titulo": "Fantasma"}'
```

**Resposta esperada (200 OK):**
```json
{"id": 1, "titulo": "Clean Code", "autor": "Robert C. Martin", "ano": 2008, "disponivel": false}
```

---

### DELETE `/livros/{id}` — Remover um livro

```bash
# Remover livro existente
curl -X DELETE http://127.0.0.1:8000/livros/3

# Remover livro inexistente (deve retornar 404)
curl -X DELETE http://127.0.0.1:8000/livros/999
```

**Resposta de sucesso (200 OK):**
```json
{"mensagem": "Livro 'Domain-Driven Design' (ID 3) removido com sucesso."}
```

**Resposta de erro (404 Not Found):**
```json
{"detail": "Livro com ID 999 não encontrado."}
```

---

## 🔁 Resumo dos Endpoints

| Método | Rota | Descrição | Status Sucesso |
|--------|------|-----------|----------------|
| GET | `/livros` | Lista todos os livros | 200 |
| GET | `/livros/{id}` | Busca livro por ID | 200 |
| POST | `/livros` | Cria novo livro | 201 |
| PUT | `/livros/{id}` | Atualiza livro por ID | 200 |
| DELETE | `/livros/{id}` | Remove livro por ID | 200 |

---

## 📦 Dependências

```
fastapi>=0.110.0
uvicorn>=0.29.0
```

> Instale com: `pip install fastapi uvicorn`
