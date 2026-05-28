# =============================================================================
# API REST Assíncrona com FastAPI — CRUD de Livros
# =============================================================================
# Conceito central: FastAPI é um framework ASGI (Asynchronous Server Gateway
# Interface). Isso significa que ele foi construído do zero para suportar
# código assíncrono. Quando usamos `async def`, estamos dizendo ao Python:
# "esta função pode pausar e deixar outras tarefas rodarem enquanto espera".
# O `await` marca exatamente onde essa pausa pode ocorrer.
# =============================================================================

# --- Importações ---
# FastAPI: o framework principal
# HTTPException: para retornar erros HTTP padronizados (ex: 404 Not Found)
# status: constantes com códigos HTTP legíveis (status.HTTP_404_NOT_FOUND)
from fastapi import FastAPI, HTTPException, status

# BaseModel do Pydantic: serve para validar e tipar os dados que entram e saem
# da API. É como um "contrato" que garante que os dados têm o formato correto.
# NOTA: Execute "pip install pydantic fastapi uvicorn" no terminal para instalar as dependências
from pydantic import BaseModel

# Optional: permite que um campo possa ser None (útil no PUT, onde nem
# todos os campos precisam ser enviados)
from typing import Optional

# asyncio.sleep simula uma operação I/O assíncrona (ex: consulta a banco de dados)
import asyncio


# =============================================================================
# INSTÂNCIA DA APLICAÇÃO
# =============================================================================
# Criamos a aplicação FastAPI. O título e a versão aparecem na documentação
# automática em /docs (Swagger UI).
app = FastAPI(
    title="API de Livros",
    description="Exemplo de API REST assíncrona com FastAPI",
    version="1.0.0",
)


# =============================================================================
# MODELOS DE DADOS (Pydantic)
# =============================================================================
# Por que usar Pydantic?
# Sem Pydantic, teríamos que validar manualmente cada campo recebido.
# Com Pydantic, definimos a estrutura uma vez e ele cuida de:
#   - Validar tipos automaticamente
#   - Retornar erros claros se algo estiver errado
#   - Gerar documentação automática no Swagger
#
# Pensando como senior: separamos em dois modelos propositalmente.
# LivroBase: campos que o USUÁRIO envia (sem o id, que é gerado pelo sistema)
# Livro: representa o livro COMPLETO já armazenado (inclui o id)
# Livro herda de LivroBase, evitando repetição de código (DRY principle)

class LivroBase(BaseModel):
    """Dados que o cliente envia ao criar ou atualizar um livro."""
    titulo: str
    autor: str
    ano: int
    disponivel: bool = True  # valor padrão: True


class Livro(LivroBase):
    """Representa um livro completo, já com ID atribuído pelo sistema."""
    id: int


class LivroAtualizacao(BaseModel):
    """
    Modelo para atualizações parciais (PUT).
    Todos os campos são opcionais: o cliente pode enviar apenas
    o que deseja alterar, sem precisar repetir tudo.
    Esse padrão é chamado de "partial update".
    """
    titulo: Optional[str] = None
    autor: Optional[str] = None
    ano: Optional[int] = None
    disponivel: Optional[bool] = None


# =============================================================================
# "BANCO DE DADOS" EM MEMÓRIA
# =============================================================================
# Em produção, isso seria uma chamada assíncrona a um banco de dados
# (ex: await db.query(...) com SQLAlchemy async ou Motor para MongoDB).
# Aqui usamos uma lista Python para simplificar e focar no aprendizado
# dos padrões async/await.
#
# db_livros: lista que armazena os livros enquanto a aplicação está rodando
# proximo_id: contador simples para gerar IDs únicos e crescentes
db_livros: list[Livro] = [
    Livro(id=1, titulo="Clean Code", autor="Robert C. Martin", ano=2008),
    Livro(id=2, titulo="O Programador Pragmático", autor="Andrew Hunt", ano=1999),
    Livro(id=3, titulo="Domain-Driven Design", autor="Eric Evans", ano=2003),
]
proximo_id: int = 4


# =============================================================================
# FUNÇÕES AUXILIARES ASSÍNCRONAS
# =============================================================================
# Por que criar funções auxiliares?
# Elas simulam a camada de "repositório" (repository pattern), separando
# a lógica de acesso a dados dos endpoints. Em produção, essas funções
# fariam chamadas reais ao banco de dados com `await`.

async def buscar_livro_por_id(livro_id: int) -> Optional[Livro]:
    """
    Busca um livro pelo ID na lista em memória.
    O `await asyncio.sleep(0)` simula uma operação I/O assíncrona,
    como uma consulta a banco de dados. Em produção seria:
        return await db.execute(select(Livro).where(Livro.id == livro_id))
    """
    await asyncio.sleep(0)  # simula latência de I/O (ex: consulta ao banco)
    for livro in db_livros:
        if livro.id == livro_id:
            return livro
    return None


async def salvar_livros() -> None:
    """
    Simula persistência assíncrona (ex: commit no banco de dados).
    Em produção: await db.commit()
    """
    await asyncio.sleep(0)  # simula I/O de escrita


# =============================================================================
# ENDPOINTS
# =============================================================================

# -----------------------------------------------------------------------------
# GET /livros — Listar todos os livros
# -----------------------------------------------------------------------------
# Por que `async def`?
# Mesmo que aqui não tenhamos um await "real" bloqueante, declarar async def
# prepara o endpoint para escalar. Se amanhã adicionarmos uma query ao banco,
# não precisamos refatorar a assinatura da função.
#
# `response_model=list[Livro]` garante que a resposta sempre siga o formato
# do modelo Livro, filtrando campos extras e documentando a resposta no Swagger.

@app.get(
    "/livros",
    response_model=list[Livro],
    summary="Lista todos os livros",
    status_code=status.HTTP_200_OK,
)
async def listar_livros():
    """
    Retorna a lista completa de livros cadastrados.

    - **Retorna**: lista de objetos Livro
    - **Status de sucesso**: 200 OK
    """
    await asyncio.sleep(0)  # simula busca assíncrona no banco
    return db_livros


# -----------------------------------------------------------------------------
# GET /livros/{id} — Buscar um livro específico
# -----------------------------------------------------------------------------
# `{livro_id}` na rota é um "path parameter". FastAPI automaticamente converte
# para int e injeta como argumento da função.

@app.get(
    "/livros/{livro_id}",
    response_model=Livro,
    summary="Busca um livro pelo ID",
    status_code=status.HTTP_200_OK,
)
async def buscar_livro(livro_id: int):
    """
    Retorna um livro específico pelo seu ID.

    - **livro_id**: ID inteiro do livro
    - **Retorna**: objeto Livro
    - **Erro 404**: se o livro não for encontrado
    """
    # `await` aqui libera o event loop enquanto a busca ocorre
    livro = await buscar_livro_por_id(livro_id)

    if livro is None:
        # HTTPException interrompe a execução e retorna o erro ao cliente
        # Usar constantes de status (HTTP_404_NOT_FOUND) é melhor do que
        # números mágicos (404) — mais legível e menos propenso a erros
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Livro com ID {livro_id} não encontrado.",
        )

    return livro


# -----------------------------------------------------------------------------
# POST /livros — Criar um novo livro
# -----------------------------------------------------------------------------
# O corpo da requisição (body) é recebido automaticamente pelo FastAPI
# quando o parâmetro é do tipo de um BaseModel do Pydantic.
# FastAPI faz a desserialização (JSON → objeto Python) e validação sozinho.
#
# status_code=201: convenção REST — "201 Created" indica que um recurso
# foi criado com sucesso, diferente de "200 OK" que apenas retorna dados.

@app.post(
    "/livros",
    response_model=Livro,
    summary="Cria um novo livro",
    status_code=status.HTTP_201_CREATED,
)
async def criar_livro(livro_data: LivroBase):
    """
    Cria um novo livro com os dados fornecidos.

    - **livro_data**: título, autor, ano e disponibilidade
    - **Retorna**: o livro criado com o ID gerado
    - **Status de sucesso**: 201 Created
    """
    global proximo_id  # acessa o contador global para gerar o próximo ID

    # Criamos o objeto Livro combinando o ID gerado com os dados recebidos.
    # `**livro_data.model_dump()` desempacota o modelo Pydantic em um dicionário
    # para passarmos como kwargs ao construtor de Livro.
    novo_livro = Livro(id=proximo_id, **livro_data.model_dump())
    proximo_id += 1

    db_livros.append(novo_livro)
    await salvar_livros()  # simula persistência assíncrona

    return novo_livro


# -----------------------------------------------------------------------------
# PUT /livros/{id} — Atualizar um livro existente
# -----------------------------------------------------------------------------
# Aqui usamos LivroAtualizacao (com campos opcionais) para permitir
# "partial updates" — o cliente pode enviar só os campos que quer mudar.
#
# Padrão usado: criamos um novo objeto Livro mesclando os dados existentes
# com os dados novos. `exclude_unset=True` é crucial: faz o Pydantic ignorar
# campos que NÃO foram enviados (diferente de campos enviados como None).

@app.put(
    "/livros/{livro_id}",
    response_model=Livro,
    summary="Atualiza um livro existente",
    status_code=status.HTTP_200_OK,
)
async def atualizar_livro(livro_id: int, dados_atualizados: LivroAtualizacao):
    """
    Atualiza parcial ou totalmente um livro existente.

    - **livro_id**: ID do livro a ser atualizado
    - **dados_atualizados**: campos a atualizar (todos opcionais)
    - **Retorna**: o livro atualizado
    - **Erro 404**: se o livro não for encontrado
    """
    livro_existente = await buscar_livro_por_id(livro_id)

    if livro_existente is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Livro com ID {livro_id} não encontrado.",
        )

    # `model_dump(exclude_unset=True)` retorna apenas os campos que foram
    # explicitamente enviados na requisição, ignorando os que têm valor padrão None.
    # Exemplo: se o cliente enviou só {"titulo": "Novo Título"}, o dict terá
    # apenas {"titulo": "Novo Título"}, sem "autor", "ano" ou "disponivel".
    campos_para_atualizar = dados_atualizados.model_dump(exclude_unset=True)

    # `model_dump()` converte o livro existente em dicionário
    dados_livro_atual = livro_existente.model_dump()

    # Mescla: sobrescreve apenas os campos enviados, mantém o resto
    dados_livro_atual.update(campos_para_atualizar)

    # Cria um novo objeto Livro com os dados mesclados
    livro_atualizado = Livro(**dados_livro_atual)

    # Substitui o livro na lista pelo índice
    indice = db_livros.index(livro_existente)
    db_livros[indice] = livro_atualizado

    await salvar_livros()  # simula persistência assíncrona

    return livro_atualizado


# -----------------------------------------------------------------------------
# DELETE /livros/{id} — Remover um livro
# -----------------------------------------------------------------------------
# Convenção REST: DELETE bem-sucedido pode retornar:
#   - 204 No Content (sem body) — mais comum
#   - 200 OK com uma mensagem de confirmação — mais amigável para APIs públicas
# Aqui optamos por 200 com mensagem para facilitar o entendimento.

@app.delete(
    "/livros/{livro_id}",
    summary="Remove um livro",
    status_code=status.HTTP_200_OK,
)
async def deletar_livro(livro_id: int):
    """
    Remove um livro da lista pelo seu ID.

    - **livro_id**: ID do livro a ser removido
    - **Retorna**: mensagem de confirmação
    - **Erro 404**: se o livro não for encontrado
    """
    livro = await buscar_livro_por_id(livro_id)

    if livro is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Livro com ID {livro_id} não encontrado.",
        )

    db_livros.remove(livro)
    await salvar_livros()  # simula persistência assíncrona

    # Retornamos um dicionário simples como confirmação.
    # Em uma API de produção, poderia ser um modelo de resposta padronizado.
    return {"mensagem": f"Livro '{livro.titulo}' (ID {livro_id}) removido com sucesso."}
