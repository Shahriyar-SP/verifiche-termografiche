import os
from pathlib import Path
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

BASE_DIR = Path(__file__).resolve().parent

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    DATABASE_URL = "sqlite:///:memory:"

SQLALCHEMY_DATABASE_URL = DATABASE_URL

Base = declarative_base()

if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class ContactRequest(Base):
    __tablename__ = "requests"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100))
    email = Column(String(100))
    telefono = Column(String(20))
    messaggio = Column(Text)

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    # Sintassi aggiornata per Starlette/FastAPI recenti: 'request' va come primo argomento
    return templates.TemplateResponse(request, "index.html")

@app.post("/submit", response_class=HTMLResponse)
async def handle_submit(
    request: Request,
    nome: str = Form(...),
    email: str = Form(...),
    telefono: str = Form(None),
    messaggio: str = Form(...),
    honeypot: str = Form("")
):
    if honeypot:
        return HTMLResponse("<p style='color:red;'>Spam detected.</p>", status_code=400)
        
    db = SessionLocal()
    try:
        new_request = ContactRequest(nome=nome, email=email, telefono=telefono, messaggio=messaggio)
        db.add(new_request)
        db.commit()
    finally:
        db.close()
        
    # Sintassi aggiornata anche qui per il frammento di successo
    return templates.TemplateResponse(request, "success.html", {"nome": nome})
