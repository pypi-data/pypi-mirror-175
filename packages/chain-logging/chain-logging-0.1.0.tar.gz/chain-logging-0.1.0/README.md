# Distinct Logger
Distinct every request with an `ID` on your logger

# How to use?
Very easy to initialize

## FastAPI
```
from fastapi import FastAPI, Request
from chain_logging.fastapi import ChainLoggerMiddleware, get_chained_logger

app = FastAPI()

app.add_middleware(ChainLoggerMiddleware, on_receive=True, on_done=True)

@app.get("/home")
async def home(request: Request):
    logger = await get_chained_logger(request)
    logger.info("this is a trial 1")
    logger.error("this is a trial 2")
    logger.warning("this is a trial 3")
    logger.critical("this is a trial 3")
    return {"status": "welcome home!"}
```

Output
```
[2022-11-09 03:11:31,835][ID:1667963491835419699][fastapi.py:225][INFO] - Received GET /home
[2022-11-09 03:11:31,836][ID:1667963491835419699][__init__.py:14][INFO] - this is a trial 1
[2022-11-09 03:11:31,836][ID:1667963491835419699][__init__.py:15][ERROR] - this is a trial 2
[2022-11-09 03:11:31,836][ID:1667963491835419699][__init__.py:16][WARNING] - this is a trial 3
[2022-11-09 03:11:31,836][ID:1667963491835419699][__init__.py:17][CRITICAL] - this is a trial 3
[2022-11-09 03:11:31,836][ID:1667963491835419699][fastapi.py:236][INFO] - Request done in 1.17ms
[2022-11-09 03:12:19,152][ID:1667963539151928302][fastapi.py:225][INFO] - Received GET /home
[2022-11-09 03:12:19,152][ID:1667963539151928302][__init__.py:14][INFO] - this is a trial 1
[2022-11-09 03:12:19,152][ID:1667963539151928302][__init__.py:15][ERROR] - this is a trial 2
[2022-11-09 03:12:19,152][ID:1667963539151928302][__init__.py:16][WARNING] - this is a trial 3
[2022-11-09 03:12:19,152][ID:1667963539151928302][__init__.py:17][CRITICAL] - this is a trial 3
[2022-11-09 03:12:19,153][ID:1667963539151928302][fastapi.py:236][INFO] - Request done in 1.37ms
[2022-11-09 03:12:21,892][ID:1667963541892393491][fastapi.py:225][INFO] - Received GET /home
[2022-11-09 03:12:21,893][ID:1667963541892393491][__init__.py:14][INFO] - this is a trial 1
[2022-11-09 03:12:21,893][ID:1667963541892393491][__init__.py:15][ERROR] - this is a trial 2
[2022-11-09 03:12:21,893][ID:1667963541892393491][__init__.py:16][WARNING] - this is a trial 3
[2022-11-09 03:12:21,893][ID:1667963541892393491][__init__.py:17][CRITICAL] - this is a trial 3
[2022-11-09 03:12:21,894][ID:1667963541892393491][fastapi.py:236][INFO] - Request done in 1.62ms

```

## Flask
```
from flask import Flask
from chain_logging.flask import setup_chained_logger, logger

app = Flask(__name__)

setup_chained_logger(app)

@app.get("/home")
def home():
    logger.info("this is a trial 1")
    logger.error("this is a trial 2")
    logger.warning("this is a trial 3")
    logger.critical("this is a trial 3")
    return {"status": "welcome home!"}
```

Output
```
[2022-11-09 10:23:29,769][ID:1667964209768871143][main.py:252][INFO] - Received GET /home
[2022-11-09 10:23:29,769][ID:1667964209768871143][main.py:328][INFO] - this is a trial 1
[2022-11-09 10:23:29,770][ID:1667964209768871143][main.py:329][ERROR] - this is a trial 2
[2022-11-09 10:23:29,770][ID:1667964209768871143][main.py:330][WARNING] - this is a trial 3
[2022-11-09 10:23:29,770][ID:1667964209768871143][main.py:331][CRITICAL] - this is a trial 3
[2022-11-09 10:23:29,771][ID:1667964209768871143][main.py:259][INFO] - Request done in 2.53ms
[2022-11-09 10:23:30,407][ID:1667964210407508175][main.py:252][INFO] - Received GET /home
[2022-11-09 10:23:30,408][ID:1667964210407508175][main.py:328][INFO] - this is a trial 1
[2022-11-09 10:23:30,408][ID:1667964210407508175][main.py:329][ERROR] - this is a trial 2
[2022-11-09 10:23:30,408][ID:1667964210407508175][main.py:330][WARNING] - this is a trial 3
[2022-11-09 10:23:30,409][ID:1667964210407508175][main.py:331][CRITICAL] - this is a trial 3
[2022-11-09 10:23:30,410][ID:1667964210407508175][main.py:259][INFO] - Request done in 2.41ms
[2022-11-09 10:23:30,831][ID:1667964210831595163][main.py:252][INFO] - Received GET /home
[2022-11-09 10:23:30,832][ID:1667964210831595163][main.py:328][INFO] - this is a trial 1
[2022-11-09 10:23:30,832][ID:1667964210831595163][main.py:329][ERROR] - this is a trial 2
[2022-11-09 10:23:30,832][ID:1667964210831595163][main.py:330][WARNING] - this is a trial 3
[2022-11-09 10:23:30,833][ID:1667964210831595163][main.py:331][CRITICAL] - this is a trial 3
[2022-11-09 10:23:30,833][ID:1667964210831595163][main.py:259][INFO] - Request done in 2.07ms
```