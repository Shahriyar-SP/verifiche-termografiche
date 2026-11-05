Verifiche Termografiche - Landing Page & Backend

Questo progetto è stato sviluppato durante il mio tirocinio come Software Engineer presso V.B.R Group. Si tratta di una landing page interattiva con un backend strutturato per la raccolta e gestione dei dati degli utenti, 
sviluppata con particolare attenzione alle performance e alla validazione dei form.


🚀 Tecnologie Utilizzate


Python & FastAPI: Backend asincrono ad alte prestazioni per la gestione delle API REST e della business logic.
SQLite: Database relazionale leggero impiegato come storage di sviluppo e fallback locale.
HTML5 & CSS3: Struttura semantica e styling moderno, reattivo e ottimizzato.
Alpine.js: Micro-framework per la reattività del client e la gestione dinamica dell'interfaccia.
Architettura & Validazione Robusta: Validazione coerente sia client-side che server-side tramite modelli Pydantic.
Honeypot Anti-Spam: Meccanismo di sicurezza invisibile per la prevenzione di bot e invii automatizzati.


🛠️ Scelte Tecniche

Adozione di FastAPI
FastAPI è stato selezionato per garantire massima efficienza computazionale e supporto nativo alla programmazione asincrona. La documentazione interattiva OpenAPI generata automaticamente e 
la validazione rigorosa dei payload tramite Pydantic riducono al minimo i tempi di sviluppo e gli errori a runtime.

Alpine.js per la reattività frontend
Invece di sovraccaricare il frontend con framework monolitici (come React o Vue), si è optato per Alpine.js. Questa scelta permette di implementare validazione in tempo reale e manipolazioni DOM reattive mantenendo 
un bundle ridottissimo e tempi di caricamento istantanei per la landing page.

SQLite in locale e separazione degli ambienti
L'utilizzo di SQLite funge da fallback agile per il testing locale senza dipendenze infrastrutturali esterne, mentre l'architettura di produzione è configurata per PostgreSQL. Questa separazione evidenzia 
una chiara adozione delle buone pratiche di configuration management e isolamento tra ambienti di sviluppo, collaudo e produzione.

Protezione Anti-Spam con tecnica Honeypot
Al fine di bloccare bot e crawler che compilano automaticamente i form senza degradare l'esperienza utente con CAPTCHA invasivi, è stato introdotto un campo honeypot nascosto tramite CSS. 
I bot tendono a compilare tutti i campi esposti nel DOM; il backend scarta silenziosamente qualsiasi richiesta in cui tale campo risulti valorizzato.


💡 Come eseguire il progetto localmente

1. Clonare il repository di progetto:
    git clone https://github.com/Shahriyar-SP/verifiche-termografiche.git
    cd verifiche-termografiche

2. Creare e attivare un virtual environment:
    python -m venv venv
    source venv/bin/activate  # Su Windows: venv\Scripts\activate

3. Installare le dipendenze:
    pip install -r requirements.txt

4. Avviare il server di sviluppo con Uvicorn:
    uvicorn main:app --reload

L'applicazione sarà raggiungibile su http://127.0.0.1:8000 e la documentazione Swagger interattiva sarà consultabile su http://127.0.0.1:8000/docs.
