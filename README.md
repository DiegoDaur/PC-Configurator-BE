Backend del progetto DaurisComputer, un'applicazione per configurare PC su misura. È un'API REST scritta in Python con Flask, che gestisce utenti, componenti, build e regole di compatibilità tra componenti.

Tecnologie usate:
- Python con Flask
- SQLAlchemy per l'accesso al database
- PostgreSQL come database
- JWT (PyJWT) per l'autenticazione
- bcrypt per l'hashing delle password
- flask-cors per permettere le richieste dal frontend

Architettura
Il progetto è organizzato a livelli:
- controller/ - le rotte Flask, ricevono le richieste e restituiscono le risposte
- service/ - logica applicativa (validazioni, regole di business)
- repository/ - query verso il database
- model/ - rappresentazione delle entità (User, Component, Build, CompatibilityRule)
- exception/ - eccezione custom per gestire gli errori in modo uniforme
- persistence/ - configurazione della connessione al database
- docs/ - script SQL per creare le tabelle (DDL) e popolarle con dati di esempio (DML)
