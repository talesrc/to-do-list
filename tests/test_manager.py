import operator

from fastapi import status
from fastapi.testclient import TestClient

from src.manager import TAREFAS, app


def test_quando_listar_tarefas_devo_ter_como_retorno_codigo_de_status_200():
    cliente = TestClient(app)
    resposta = cliente.get("/tarefas")
    assert resposta.status_code == status.HTTP_200_OK


def test_quando_listar_tarefas_formato_de_retorno_deve_ser_json():
    cliente = TestClient(app)
    resposta = cliente.get("/tarefas")
    assert resposta.headers["Content-Type"] == "application/json"


def test_quando_listar_tarefas_retorno_deve_ser_uma_lista():
    cliente = TestClient(app)
    resposta = cliente.get("/tarefas")
    assert isinstance(resposta.json(), list)


def test_quando_listar_tarefas_a_tarefa_retornada_deve_possuir_id():
    TAREFAS.append(
        {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "titulo": "titulo 1",
            "descricao": "descricao 1",
            "estado": "finalizado",
        }
    )
    cliente = TestClient(app)
    resposta = cliente.get("/tarefas")
    assert "id" in resposta.json().pop()
    TAREFAS.clear()


def test_quando_listar_tarefas_a_tarefa_retornada_deve_possuir_titulo():
    TAREFAS.append(
        {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "titulo": "titulo 1",
            "descricao": "descricao 1",
            "estado": "finalizado",
        }
    )
    cliente = TestClient(app)
    resposta = cliente.get("/tarefas")
    assert "titulo" in resposta.json().pop()
    TAREFAS.clear()


def test_quando_listar_tarefas_a_tarefa_retornada_deve_possuir_descricao():
    TAREFAS.append(
        {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "titulo": "titulo 1",
            "descricao": "descricao 1",
            "estado": "finalizado",
        }
    )
    cliente = TestClient(app)
    resposta = cliente.get("/tarefas")
    assert "descricao" in resposta.json().pop()
    TAREFAS.clear()


def test_quando_listar_tarefas_a_tarefa_retornada_deve_possuir_um_estado():
    TAREFAS.append(
        {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "titulo": "titulo 1",
            "descricao": "descricao 1",
            "estado": "finalizado",
        }
    )
    cliente = TestClient(app)
    resposta = cliente.get("/tarefas")
    assert "estado" in resposta.json().pop()
    TAREFAS.clear()


def test_recurso_tarefas_deve_aceitar_o_verbo_post():
    cliente = TestClient(app)
    resposta = cliente.post("/tarefas")
    assert resposta.status_code != status.HTTP_405_METHOD_NOT_ALLOWED


def test_quando_uma_tarefa_e_submetida_deve_possuir_um_titulo():
    cliente = TestClient(app)
    resposta = cliente.post("/tarefas", json={})
    assert resposta.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_titulo_da_tarefa_deve_conter_entre_3_e_50_caracteres():
    cliente = TestClient(app)
    resposta = cliente.post("/tarefas", json={"titulo": 2 * "*"})
    assert resposta.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    resposta = cliente.post("/tarefas", json={"titulo": 51 * "*"})
    assert resposta.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_quando_uma_tarefa_e_submetida_deve_possuir_uma_descricao():
    cliente = TestClient(app)
    resposta = cliente.post("/tarefas", json={"titulo": "titulo"})
    assert resposta.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_descricao_da_tarefa_pode_conter_no_maximo_140_caracteres():
    cliente = TestClient(app)
    resposta = cliente.post(
        "/tarefas", json={"titulo": "titulo", "descricao": "*" * 141}
    )
    assert resposta.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_quando_criar_uma_tarefa_a_mesma_deve_ser_retornada():
    cliente = TestClient(app)
    tarefa_esperada = {"titulo": "titulo", "descricao": "descricao"}
    resposta = cliente.post("/tarefas", json=tarefa_esperada)
    tarefa_criada = resposta.json()
    assert tarefa_criada["titulo"] == tarefa_esperada["titulo"]
    assert tarefa_criada["descricao"] == tarefa_esperada["descricao"]
    TAREFAS.clear()


def test_quando_criar_uma_tarefa_seu_id_deve_ser_unico():
    cliente = TestClient(app)
    tarefa1 = {"titulo": "titulo1", "descricao": "descricao1"}
    tarefa2 = {"titulo": "titulo2", "descricao": "descricao1"}
    resposta1 = cliente.post("/tarefas", json=tarefa1)
    resposta2 = cliente.post("/tarefas", json=tarefa2)
    assert resposta1.json()["id"] != resposta2.json()["id"]
    TAREFAS.clear()


def test_quando_criar_uma_tarefa_seu_estado_padrao_e_nao_finalizado():
    cliente = TestClient(app)
    tarefa = {"titulo": "titulo", "descricao": "descricao"}
    resposta = cliente.post("/tarefas", json=tarefa)
    assert resposta.json()["estado"] == "não finalizado"
    TAREFAS.clear()


def test_quando_criar_uma_tarefa_codigo_de_status_retornado_deve_ser_201():
    cliente = TestClient(app)
    tarefa = {"titulo": "titulo", "descricao": "descricao"}
    resposta = cliente.post("/tarefas", json=tarefa)
    assert resposta.status_code == status.HTTP_201_CREATED
    TAREFAS.clear()


def test_quando_criar_uma_tarefa_esta_deve_ser_persistida():
    cliente = TestClient(app)
    tarefa = {"titulo": "titulo", "descricao": "descricao"}
    cliente.post("/tarefas", json=tarefa)
    assert len(TAREFAS) == 1
    TAREFAS.clear()


def test_quando_remover_uma_tarefa_deve_retornar_status_204():
    client = TestClient(app)
    response = client.delete("/tarefas/1")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_quando_nao_achar_a_tarefa_a_ser_removida_deve_retornar_status_404():
    client = TestClient(app)
    response = client.delete("/tarefas/aaaaaaaaaa")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_quando_solicitar_as_tarefas_a_nao_finalizada_tem_que_aparecer_antes_da_finalizada():
    TAREFAS.append(
        {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "titulo": "titulo 1",
            "descricao": "descricao 1",
            "estado": "não finalizado",
        }
    )
    TAREFAS.append(
        {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa7",
            "titulo": "titulo 1",
            "descricao": "descricao 1",
            "estado": "finalizado",
        }
    )
    client = TestClient(app)
    indexNotFinished = indexFinished = 0
    for index, item in enumerate(TAREFAS):
        if item["id"] == "3fa85f64-5717-4562-b3fc-2c963f66afa6":
            indexNotFinished = index
        elif item["id"] == "3fa85f64-5717-4562-b3fc-2c963f66afa7":
            indexFinished = index
    assert indexNotFinished < indexFinished
    TAREFAS.clear()


def test_quando_solicitar_a_finalizacao_da_atividade_o_estado_fica_finalizado():
    TAREFAS.append(
        {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa7",
            "titulo": "titulo 1",
            "descricao": "descricao 1",
            "estado": "não finalizado",
        }
    )
    client = TestClient(app)
    response = client.put("/tarefas/3fa85f64-5717-4562-b3fc-2c963f66afa7")
    assert response.json()["estado"] == "finalizado"
    TAREFAS.clear()


def test_quando_solicitar_a_finalizacao_da_atividade_o_status_da_resposta_202():
    TAREFAS.append(
        {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa7",
            "titulo": "titulo 1",
            "descricao": "descricao 1",
            "estado": "não finalizado",
        }
    )
    client = TestClient(app)
    response = client.put("/tarefas/3fa85f64-5717-4562-b3fc-2c963f66afa7")
    assert response.status_code == status.HTTP_202_ACCEPTED
    TAREFAS.clear()


def test_quando_nao_achar_item_informado_para_finalizacao_deve_retornar_status_404():
    client = TestClient(app)
    response = client.put("/tarefas/9000")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_quando_nao_achar_item_informado_deve_retornar_status_404():
    client = TestClient(app)
    response = client.get("/tarefas/9000")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_quando_retornar_item_solicitado_ter_status_da_resposta_202():
    TAREFAS.append(
        {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa7",
            "titulo": "titulo 1",
            "descricao": "descricao 1",
            "estado": "não finalizado",
        }
    )
    client = TestClient(app)
    response = client.put("/tarefas/3fa85f64-5717-4562-b3fc-2c963f66afa7")
    assert response.status_code == status.HTTP_202_ACCEPTED
    TAREFAS.clear()
