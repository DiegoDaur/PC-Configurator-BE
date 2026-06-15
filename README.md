# DaurisComputer — Backend

Backend dell'applicazione **DaurisComputer**, un configuratore di PC con verifica automatica della compatibilità tra componenti hardware.

Progetto realizzato per il corso *Full Stack Developer 2025/2026*, secondo la traccia **Alternativa 2 – Configuratore PC + Compatibilità Hardware**.

## Stack tecnologico

- **Linguaggio**: Python
- **Framework**: Flask
- **Database**: PostgreSQL
- **ORM/Query**: SQLAlchemy (query SQL dirette tramite `text()`)
- **Autenticazione**: JWT (PyJWT)
- **Hashing password**: bcrypt
- **CORS**: flask-cors

## Architettura

Il backend è organizzato a livelli (layered architecture), per separare le responsabilità:

```
controller/   → rotte Flask, gestione richieste/risposte HTTP
service/      → logica applicativa, validazioni, regole di business
repository/   → accesso al database (query SQL via SQLAlchemy)
model/        → entità del dominio (User, Component, Build, CompatibilityRule)
exception/    → gestione centralizzata degli errori
persistence/  → configurazione connessione al database
docs/         → script SQL (DDL e DML) per creare e popolare il database
```

Flusso di una richiesta: **Controller → Service → Repository → Database**, e ritorno a ritroso fino alla risposta JSON.

## Funzionalità principali

- Registrazione e login utenti con autenticazione JWT
- Hashing sicuro delle password (bcrypt)
- Gestione ruoli: utente standard e amministratore
- CRUD completo per il catalogo componenti (CPU, GPU, RAM, Motherboard, PSU, Storage, Case, Cooler)
- Verifica automatica della compatibilità tra componenti selezionati
- Gestione delle regole di compatibilità (CRUD, riservato agli admin)
- Filtro componenti compatibili dato un set di componenti già selezionati
- Creazione, lettura, modifica ed eliminazione delle build (configurazioni PC)
- Calcolo automatico di prezzo totale e consumo energetico (wattaggio) di una build
- Confronto tra build diverse
- Gestione utenti (CRUD, riservato agli admin)
- Gestione centralizzata degli errori con codici di stato HTTP coerenti

## Autenticazione e autorizzazione

L'autenticazione è basata su **JWT**:

1. Al login viene generato un token contenente `user_id`, `email` e `role`, valido 24 ore
2. Il token va inviato nelle richieste protette tramite header:
   ```
   Authorization: Bearer <token>
   ```
3. Due decoratori proteggono le rotte:
   - `@require_auth` → richiede un token valido
   - `@require_admin` → richiede inoltre il ruolo `admin`

## Endpoint principali

### Autenticazione
| Metodo | Endpoint | Descrizione |
|--------|----------|-------------|
| POST | `/api/auth/register` | Registrazione nuovo utente |
| POST | `/api/auth/login` | Login, restituisce JWT |

### Componenti
| Metodo | Endpoint | Descrizione | Accesso |
|--------|----------|-------------|---------|
| GET | `/api/components` | Lista componenti (filtro per categoria con `?category=`) | Pubblico |
| GET | `/api/components/<id>` | Dettaglio componente | Pubblico |
| POST | `/api/components` | Crea componente | Admin |
| PATCH | `/api/components/<id>` | Modifica componente | Admin |
| DELETE | `/api/components/<id>` | Elimina componente | Admin |

### Compatibilità
| Metodo | Endpoint | Descrizione | Accesso |
|--------|----------|-------------|---------|
| GET | `/api/compatibility-rules` | Lista regole di compatibilità | Admin |
| POST | `/api/compatibility-rules` | Crea regola | Admin |
| PATCH | `/api/compatibility-rules/<id>` | Modifica regola | Admin |
| DELETE | `/api/compatibility-rules/<id>` | Elimina regola | Admin |
| POST | `/api/compatibility-check` | Verifica compatibilità tra componenti selezionati | Autenticato |
| GET | `/api/compatible-components` | Componenti compatibili con una selezione | Autenticato |

### Build (configurazioni)
| Metodo | Endpoint | Descrizione | Accesso |
|--------|----------|-------------|---------|
| GET | `/api/builds` | Lista build | Autenticato |
| GET | `/api/builds/compare` | Confronto tra build | Autenticato |
| GET | `/api/builds/<id>` | Dettaglio build | Autenticato |
| POST | `/api/builds` | Crea build | Autenticato |
| PATCH | `/api/builds/<id>` | Modifica build | Autenticato |
| DELETE | `/api/builds/<id>` | Elimina build | Autenticato |

### Utenti
| Metodo | Endpoint | Descrizione | Accesso |
|--------|----------|-------------|---------|
| GET | `/api/users/me` | Profilo utente corrente | Autenticato |
| GET | `/api/users` | Lista utenti | Admin |
| GET | `/api/users/<id>` | Dettaglio utente | Admin |
| PATCH | `/api/users/<id>` | Modifica utente (es. ruolo) | Admin |
| DELETE | `/api/users/<id>` | Elimina utente | Admin |

## Modello dati (sintesi)

- **User**: id, username, email, password (hash bcrypt), role (`user` / `admin`)
- **Component**: id, name, brand, category, price, wattage, stock, in_stock, image_url, description, specs
- **Build**: id, user_id, name, notes, created_at, lista componenti collegati (tabella `build_component`)
- **CompatibilityRule**: id, component_a_id, component_b_id, is_compatible, reason

## Setup e avvio

### Prerequisiti
- Python 3.x
- PostgreSQL

### Passi

1. Crea un database PostgreSQL:
   ```sql
   CREATE DATABASE pc_configurator;
   ```

2. Esegui gli script SQL presenti in `docs/DDL/` (creazione tabelle) e `docs/DML/` (dati di esempio)

3. Configura la connessione al database in `persistence/db_config.py`

4. Installa le dipendenze:
   ```bash
   pip install -r requirements.txt
   ```

5. Avvia il server:
   ```bash
   python app.py
   ```

Il backend sarà disponibile su `http://localhost:5000`.

## Gestione errori

Tutti gli errori applicativi vengono gestiti tramite la classe `AppException`, che restituisce risposte JSON uniformi nel formato:

```json
{
  "error": "Messaggio descrittivo",
  "status": 404
}
```

## Note

Questo backend è pensato per essere usato insieme al frontend **DaurisComputer**, sviluppato in JavaScript/Vite, che consuma queste API REST.
