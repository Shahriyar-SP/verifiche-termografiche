from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates 
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker, Session

# --- ۱. تنظیمات اتصال به دیتابیس ---
# حتماً جای YOUR_PASSWORD رمز خودت رو بنویس (مثلا postgresql://postgres:1234@localhost...)
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:1234@localhost/verifiche_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- ۲. ساختار جدولِ فرم تماس ---
class ContactRequest(Base):
    __tablename__ = "contatti"  # اسم جدول تو دیتابیس
    
    id = Column(Integer, primary_key=True, index=True)
    ragione_sociale = Column(String, index=True)
    partita_iva = Column(String, nullable=True)
    email = Column(String)
    telefono = Column(String)
    tipo_verifica = Column(String)
    messaggio = Column(Text)

# --- ۳. دستور ساخت جدول ---
Base.metadata.create_all(bind=engine)

# --- ۴. تنظیمات سایت (کدهای قبلی) ---
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# یه تابع کمکی برای باز و بسته کردن دیتابیس
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse(request, "index.html")

# --- این مسیر جدید رو برای دریافت فرم اضافه کن ---
@app.post("/submit", response_class=HTMLResponse)
def submit_form(
    ragione_sociale: str = Form(...),
    partita_iva: str = Form(None),
    email: str = Form(...),
    telefono: str = Form(...),
    tipo_verifica: str = Form(...),
    messaggio: str = Form(...),
    db: Session = Depends(get_db)
):
    # ۱. ساخت یک رکورد جدید با اطلاعات فرم
    nuovo_contatto = ContactRequest(
        ragione_sociale=ragione_sociale,
        partita_iva=partita_iva,
        email=email,
        telefono=telefono,
        tipo_verifica=tipo_verifica,
        messaggio=messaggio
    )
    
    # ۲. ذخیره در دیتابیس
    db.add(nuovo_contatto)
    db.commit()
    
    # ۳. ارسال یه کد HTML ساده برای نمایش پیام موفقیت به جای فرم
    return """
    <div style="background-color: #dcfce7; border: 2px solid #22c55e; padding: 30px; border-radius: 8px; text-align: center;">
        <h3 style="color: #166534; margin-bottom: 10px;">✅ Richiesta Inviata con Successo!</h3>
        <p style="color: #15803d; font-size: 1.1rem;">Grazie. Il nostro team ti contatterà al più presto.</p>
    </div>
    """