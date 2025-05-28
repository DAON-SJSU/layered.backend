from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware

import service
from model import Playlist

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 오리진 허용
    allow_credentials=True,  # 크리덴셜(쿠키, 인증 헤더 등) 허용
    allow_methods=["*"],  # 모든 HTTP 메서드 허용 (GET, POST, PUT, DELETE 등)
    allow_headers=["*"],  # 모든 헤더 허용
)
@app.post("/")
async def root(dto: Playlist = Body(...)):
    return service.get_playlist(dto)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run('main:app', host="0.0.0.0", port=8000, reload=True)