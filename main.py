import os
from pathlib import Path
from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates 
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from dotenv import load_dotenv

#Loading environment variables from a .env file
load_dotenv()

# Making the absolute path to the project directory
BASE_DIR = Path(__file__).resolve().parent

# Reading the database URL without exposing it in the code
DATABASE_URL = os.getenv("DATABASE_URL")

# If the DATABASE_URL is not set in the environment, use a temporary SQLite database
if not DATABASE_URL:
    DATABASE_URL = "sqlite:///:memory:"  # Use an temporary SQLite database for testing

if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Contact form table structure
class ContactRequest(Base):
    __tablename__ = "contatti"  # Name of the table in the database
    
    id = Column(Integer, primary_key=True, index=True)
    ragione_sociale = Column(String(100), index=True)
    partita_iva = Column(String(11), nullable=True)
    email = Column(String(100))
    telefono = Column(String(20))
    tipo_verifica = Column(String(50))
    messaggio = Column(Text)

# Table creation command
Base.metadata.create_all(bind=engine)

# Landing page handling
app = FastAPI()

# Using absolute paths for static files and templates to avoid issues with relative paths
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# helping function to open and close the database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(request, "index.html")

# form submission handling
@app.post("/submit", response_class=HTMLResponse)
async def submit_form(
    request: Request,
    ragione_sociale: str = Form(..., max_length=100),
    partita_iva: str = Form(None, pattern="^[0-9]{11}$"),
    email: str = Form(..., max_length=100),
    telefono: str = Form(..., max_length=20),
    tipo_verifica: str = Form(..., max_length=50),
    messaggio: str = Form(..., max_length=1000),
    fax_number: str = Form(None),  # trap for bots
    db: Session = Depends(get_db)
):
    if fax_number:
        return templates.TemplateResponse(request, "success.html")
    
    # making a new record with the form information
    nuovo_contatto = ContactRequest(
        ragione_sociale=ragione_sociale,
        partita_iva=partita_iva,
        email=email,
        telefono=telefono,
        tipo_verifica=tipo_verifica,
        messaggio=messaggio
    )
    
    # saving in the database
    db.add(nuovo_contatto)
    db.commit()
    
    return templates.TemplateResponse(request, "success.html")