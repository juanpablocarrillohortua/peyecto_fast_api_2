from fastapi import FastAPI, Response, status, Query, Path, Body, HTTPException
import json
from fastapi.responses import JSONResponse
from futboldata import FutbolData
from models import Partido
from typing import Union, Annotated
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException


futbol = FutbolData()

tags_metadata = [
    {
        "name": "partidos",
        "description": "Operaciones relacionadas con el CRUD de partidos"
    }
]

app = FastAPI(title='partidos API',
              description="ApiRestFul para la gestión de partidos",
              version="0.0.2",
              contact={
                  "name": "Juan Pablo Carrillo Hortua",
                  "url": "https://github.com/juanpablocarrillohortua"
              },
              license_info={
                  "name": "Apache 2.0",
                  "url": "https://www.apache.org/licenses/LICENSE-2.0.html"
              },
              openapi_tags=tags_metadata)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )


@app.exception_handler(RequestValidationError)
async def http_exception_handler(request, exc):
    error = exc.errors()[0]

    field = error.get("loc")[-1] 
    msg = error.get("msg")
    
    return JSONResponse(
        status_code=422,
        content={"error": f"Error en el campo '{field}': {msg}"}
    )



@app.get("/partidos/", tags=['partidos'], status_code=status.HTTP_200_OK)
async def get_matches(skip: Annotated[int, 0, Query(ge=0, description="en que posicion de la lista desea empezar")]=0, 
                      total: Annotated[int, Query(gt=0)]=10):
    return await futbol.get_partidos(skip, total)


@app.get("/todospartidos/", tags=['partidos'], status_code=status.HTTP_200_OK)
async def get_matches():
    return await futbol.get_allIPartidos()

@app.get("/partidos/{match_id}", tags=['partidos'], status_code=status.HTTP_200_OK)
async def get_matches(match_id: Annotated[int, Path(gt=0, description="identificador del partido")]
                      , response:Response):
    res = await futbol.get_partido(match_id)
    if res:
        return res
    
    raise HTTPException(status_code=404, detail="Match not found")


@app.get('/partidosequipo/', tags=['partidos'], status_code=status.HTTP_200_OK)
@app.get('/partidosequipo/{team}', tags=['partidos'], status_code=status.HTTP_200_OK)
async def get_by_team(team: str, response:Response):
    res = await futbol.get_partidosEquipo(team)
    if res:
        return res
    
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"error",str(team)+" no encontrado"}

@app.post('/partidos', tags=['partidos'])
async def write_match(partido: Annotated[Partido, Body(description="estructura de datos del partido")]):
    return await futbol.write_partido(partido)

@app.put('/partidos/{team_id}', tags=['partidos'])
async def update_match(team_id: int, partido:Partido, response:Response):
    res = await futbol.update_partido(team_id, partido)
    if res:
        return res
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"error",str(team_id)+" no encontrado"}