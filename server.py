from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from package import main

_some_state = {"Sample": "state", "ipsum": "Lorem"}

app = FastAPI()


class StateEntry(BaseModel):
    key: str
    value: str


@app.get("/error404")
async def error_404():
    raise HTTPException(status_code=404, detail="Item not found")


@app.get("/package")
async def package_call():
    return f"{main.desc()}"


@app.get("/states")
async def complete_state():
    return dict(_some_state)


@app.get("/state/{key}")
async def state(key):
    return {"key": key, "value": _some_state.get(key, "")}


@app.post("/state/")
async def set_state(state_entry: StateEntry):
    prev = {"key": state_entry.key, "value": _some_state.get(state_entry.key, "")}
    _some_state[state_entry.key] = state_entry.value
    return prev
