from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_listar_todos_os_livros():
    response = client.get("/livros")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 3

def test_buscar_livro_por_id_existente():
    response = client.get("/livros/1")
    assert response.status_code == 200
    assert response.json()["titulo"] == "Clean Code"

def test_buscar_livro_nao_existente():
    response = client.get("/livros/999")
    assert response.status_code == 404