from http.client import HTTPException
from pathlib import Path
from typing import Any, List
from fastapi import FastAPI
from fastapi import Depends
from fastapi import status
from fastapi import HTTPException
from fastapi import Response

from models import Curso
from models import cursos
from utils.find import find, findID

app = FastAPI(
    title="Api de Cursos da Geek University",
    version="0.0.1",
    description="Uma API para estudo do FastApi"
)


@app.get("/cursos",
         description="Retorna todos os cursos ou uma lista vazia.",
         summary="Retorna todos os cursos",
         response_model=List[Curso],
         response_description="Cursos encontrados com sucesso.")
async def get_curses():
    return cursos


@app.get("/cursos/{curso_id}")
async def get_curse(curso_id: int = Path(default=None, title="Id do curso", description="Deve ser entre 1 e 2", gt=0, lt=3)):
    try:
        curso = find(cursos, curso_id)
        return curso
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Curso não encontrado."
        )


@app.post("/cursos", status_code=status.HTTP_201_CREATED, response_model=Curso)
async def post_curse(curso: Curso):
    next_id: int = len(cursos) + 1
    curso.id = next_id
    cursos.append(curso)

    return curso


@app.put("/cursos/{curso_id}")
async def put_curse(course_id: int, curse: Curso):
    itemExist = any(item.id == course_id for item in cursos)
    if itemExist:
        idCurse = findID(cursos, course_id)
        curse.id = idCurse
        cursos[course_id - 1] = curse
        return curse
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Não existe um curso com id: {course_id}")


@app.delete("/cursos/{curso_id}")
async def delete_curse(course_id: int):
    itemExist = any(item.id == course_id for item in cursos)
    if itemExist:
        print(course_id)
        del cursos[course_id - 1]
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Não existe um curso com id: {course_id}")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, debug=True, reload=True)
