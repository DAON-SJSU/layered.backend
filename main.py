from fastapi import FastAPI, Body

import service
from model import Playlist

app = FastAPI()
@app.post("/")
async def root(dto: Playlist = Body(...)):
    return service.get_playlist(dto)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run('main:app', host="0.0.0.0", port=8000, reload=True)