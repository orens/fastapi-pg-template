from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select


class RowBase(SQLModel):
    name: str = Field(index=True)
    category: int | None = Field(default=None, index=True)


class Row(RowBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    secret_category: int | None = Field(default=None, index=True)


class RowPublic(RowBase):
    id: int


class RowCreate(RowBase):
    secret_category: int


class RowUpdate(RowBase):
    name: str | None = None
    category: int | None = None
    secret_category: int | None = None


_SQLITE_FILE_NAME = "database/main.sqlite.db"
_sqlite_params = (f"sqlite:///{_SQLITE_FILE_NAME}", {"check_same_thread": False})

_postgres_params = ("postgresql://admin:root@localhost:5432/app", {})

_db_params = _postgres_params # change this to use sqlite

def _create_engine():
    return create_engine(_db_params[0], connect_args=_db_params[1])


_engine = _create_engine()


def create_db_and_tables():
    SQLModel.metadata.create_all(_engine)


def get_session():
    with Session(_engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/rows/", response_model=RowPublic)
async def create_row(row: RowCreate, session: SessionDep):
    db_row = Row.model_validate(row)
    session.add(db_row)
    session.commit()
    session.refresh(db_row)
    return db_row


@app.get("/rows/", response_model=list[RowPublic])
async def read_rows(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    rows = session.exec(select(Row).offset(offset).limit(limit)).all()
    return rows


@app.get("/rows/{row_id}", response_model=RowPublic)
async def read_row(row_id: int, session: SessionDep):
    row = session.get(Row, row_id)
    if not row:
        raise HTTPException(status_code=404, detail="Row not found")
    return row


@app.patch("/rows/{row_id}", response_model=RowPublic)
async def update_row(row_id: int, row: RowUpdate, session: SessionDep):
    row_db = session.get(Row, row_id)
    if not row_db:
        raise HTTPException(status_code=404, detail="Row not found")
    row_data = row.model_dump(exclude_unset=True)
    row_db.sqlmodel_update(row_data)
    session.add(row_db)
    session.commit()
    session.refresh(row_db)
    return row_db


@app.delete("/rows/{row_id}")
async def delete_row(row_id: int, session: SessionDep):
    row = session.get(Row, row_id)
    if not row:
        raise HTTPException(status_code=404, detail="Row not found")
    session.delete(row)
    session.commit()
    return {"ok": True}
