from enum import Enum
from uuid import UUID, uuid4
import operator

from fastapi import FastAPI, status, Response
from pydantic import BaseModel, constr


class EstadosPossiveis(str, Enum):
    finalizado = "finalizado"
    nao_finalizado = "não finalizado"


class TarefaEntrada(BaseModel):
    titulo: constr(min_length=3, max_length=50)
    descricao: constr(max_length=140)
    estado: EstadosPossiveis = EstadosPossiveis.nao_finalizado


class Tarefa(TarefaEntrada):
    id: UUID


app = FastAPI()

TAREFAS = [
    {
        "id": "1",
        "titulo": "fazer compras",
        "descricao": "comprar leite e ovos",
        "estado": "não finalizado",
    },
    {
        "id": "2",
        "titulo": "levar o cachorro para tosar",
        "descricao": "está muito peludo",
        "estado": "não finalizado",
    },
    {
        "id": "3",
        "titulo": "lavar roupas",
        "descricao": "estão sujas",
        "estado": "finalizado",
    },
]


@app.get("/tarefas")
def listar_tarefas():
    return sorted(TAREFAS, key=operator.itemgetter('estado'), reverse=True)


@app.post(
    "/tarefas", response_model=Tarefa, status_code=status.HTTP_201_CREATED
)
def criar(tarefa: TarefaEntrada):
    nova_tarefa = tarefa.dict()
    nova_tarefa.update({"id": uuid4()})
    TAREFAS.append(nova_tarefa)
    return nova_tarefa

@app.delete('/tarefas/{id}')
def remover_tarefa(id):
    for i in range(0, len(TAREFAS)):
        if TAREFAS[i]['id'] == id:
            TAREFAS.pop(i)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    return Response(status_code=status.HTTP_404_NOT_FOUND)

@app.put('/tarefas/{id}', status_code=202)
def finalizar_tarefa(id):
    for i in range(0, len(TAREFAS)):
        if TAREFAS[i]['id'] == id:
            TAREFAS[i]['estado'] = 'finalizado'
            return TAREFAS[i]
    return Response(status_code=status.HTTP_404_NOT_FOUND)

@app.get('/tarefas/{id}', status_code=202)
def listar_tarefa(id):
    for i in range(0, len(TAREFAS)):
        if TAREFAS[i]['id'] == id:
            return TAREFAS[i]
    return Response(status_code=status.HTTP_404_NOT_FOUND)
