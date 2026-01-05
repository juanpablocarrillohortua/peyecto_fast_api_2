from fastapi import FastAPI, Response, status
import json
from futboldata import FutbolData
from models import Partido

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



@app.get("/partidos/", tags=['partidos'], status_code=status.HTTP_200_OK)
async def get_matches(skip: int=0, total: int=10):
    return await futbol.get_partidos(skip, total)


@app.get("/todospartidos/", tags=['partidos'], status_code=status.HTTP_200_OK)
async def get_matches():
    return await futbol.get_allIPartidos()

@app.get("/partidos/{match_id}", tags=['partidos'], status_code=status.HTTP_200_OK)
async def get_matches(match_id, response:Response):
    res = await futbol.get_partido(match_id)
    if res:
        return res
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"error",str(match_id)+" no encontrado"}


@app.get('/partidosequipo/', tags=['partidos'], status_code=status.HTTP_200_OK)
@app.get('/partidosequipo/{team}', tags=['partidos'], status_code=status.HTTP_200_OK)
async def get_by_team(team: str, response:Response):
    res = await futbol.get_partidosEquipo(team)
    if res:
        return res
    
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"error",str(team)+" no encontrado"}

@app.post('/partidos', tags=['partidos'])
async def write_match(partido: Partido):
    return await futbol.write_partido(partido)

@app.put('/partidos/{team_id}', tags=['partidos'])
async def update_match(team_id: int, partido:Partido, response:Response):
    res = await futbol.update_partido(team_id, partido)
    if res:
        return res
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"error",str(team_id)+" no encontrado"}