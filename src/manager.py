from enum import Enum
from uuid import UUID, uuid4

from fastapi import FastAPI, status
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
        "descrição": "comprar leite e ovos",
        "estado": "não finalizado",
    },
    {
        "id": "2",
        "titulo": "levar o cachorro para tosar",
        "descrição": "está muito peludo",
        "estado": "não finalizado",
    },
    {
        "id": "3",
        "titulo": "lavar roupas",
        "descrição": "estão sujas",
        "estado": "não finalizado",
    },
]


@app.get("/tarefas")
def listar_tarefas():
    return TAREFAS


@app.post(
    "/tarefas", response_model=Tarefa, status_code=status.HTTP_201_CREATED
)
def criar(tarefa: TarefaEntrada):
    nova_tarefa = tarefa.dict()
    nova_tarefa.update({"id": uuid4()})
    TAREFAS.append(nova_tarefa)
    return nova_tarefa
