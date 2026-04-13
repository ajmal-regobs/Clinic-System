from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from app.db import get_connection, init_db
from app.models import PatientCreate, Patient


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Clinic System API", lifespan=lifespan)


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/patients", response_model=Patient, status_code=201)
def add_patient(patient: PatientCreate):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO patients (name, age, gender, phone)
                VALUES (%s, %s, %s, %s)
                RETURNING id, name, age, gender, phone, created_at
                """,
                (patient.name, patient.age, patient.gender, patient.phone),
            )
            row = cur.fetchone()
        conn.commit()
        return row
    finally:
        conn.close()


@app.get("/patients", response_model=list[Patient])
def list_patients():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name, age, gender, phone, created_at FROM patients ORDER BY id")
            return cur.fetchall()
    finally:
        conn.close()


@app.delete("/patients/{patient_id}", status_code=204)
def remove_patient(patient_id: int):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM patients WHERE id = %s RETURNING id", (patient_id,))
            if cur.fetchone() is None:
                raise HTTPException(status_code=404, detail="Patient not found")
        conn.commit()
    finally:
        conn.close()
