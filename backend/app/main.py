from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import auth, empresas, profissionais, documentos, auditoria
from app.api.routes import auth

app.include_router(auth.router)

app = FastAPI(title="ImportDoc API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(empresas.router, prefix="/empresas", tags=["Empresas"])
app.include_router(profissionais.router, prefix="/profissionais", tags=["Profissionais"])
app.include_router(documentos.router, prefix="/documentos", tags=["Documentos"])
app.include_router(auditoria.router, prefix="/auditoria", tags=["Auditoria"])

@app.get("/")
def home():
    return {"app": "ImportDoc API", "status": "ok"}
