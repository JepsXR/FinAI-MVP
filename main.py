# Step 1: IMPORT

from fastapi import FastAPI, HTTPException
from typing import List, Optional, Literal
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import google.generativeai as genai
import os
import sqlite3
import logging
import json

# Step 2: SERVER ACTIVATION

app = FastAPI(
    title="FinAI agent",
    description="Fin is an agent that explain financial terms to people in a simple way ",
    version="1.0.0"
)

load_dotenv()

keymaster = os.getenv("FINAI_API_KEY")
if not keymaster:
    print("CRITICAL ERROR: FINAI_API_KEY not found. Server aborted.")
else:
    genai.configure(api_key=keymaster)
    print("Sucessfull connection")

logging.basicConfig(level=logging.INFO)

# Step 3: CREATION OF DATA MODELS

class DataUsers(BaseModel):
    name: str = Field(..., min_length=3, max_length=20)
    age: int = Field(..., gt=0, lt=100)
    type_employment: Literal["Formal", "Informal", "Unemployed","Student"] = Field(...)
    type_worker: Literal["Independent", "Employee", "Entrepreneur", "Businessman", "Student"] = Field(...)
    stratum_number: int = Field(..., ge=0, le=6)
    monthly_income: int = Field(
        ..., 
        ge=0,
        description="Total monthly income in Colombian pesos (COP)",
        example=1200000)
    essential_expenses: int = Field(
        ..., 
        ge=0,
        description="Total monthly expenses in Colombian pesos (COP)")
    income_frequency: Literal["Fixed", "Variable"] = Field(...)

# Step 4: DATABASE CONNECTION AND CREATION OF ITS ARCHITECTURE

connection = sqlite3.connect('fin_ai.db')
cursor = connection.cursor()

fin_table_sql = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,              
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    type_employment TEXT NOT NULL,
    type_worker TEXT NOT NULL,
    stratum_number INTEGER NOT NULL,
    income_frequency TEXT NOT NULL,
    monthly_income INTEGER NOT NULL,
    essential_expenses INTEGER NOT NULL, 
    test_score INTEGER NOT NULL DEFAULT 0,
    risk_profile TEXT NOT NULL DEFAULT 'waiting'
)
"""

cursor.execute(fin_table_sql)
connection.commit()
print("¡Data saved sucessfully!")
connection.close()

# STEP 5: LOG ENDPOINT CREATION

@app.post("/users", status_code=201)
async def register_new_user(user: DataUsers):
    """
**Financial Profile Registration and Persistence**
Captures essential socioeconomic data of the citizen (income, expenses, socioeconomic stratum, and type of employment)
and stores it in a structured format in the SQLite database.
* **Validation:** Ensures that the amounts are positive and the age/stratum ranges are valid.
* **Output:** Returns the user's unique ID for future analysis queries.
"""

    try:
        conn = sqlite3.connect('fin_ai.db')
        cursor = conn.cursor()
        
        query = """
        INSERT INTO users (
            name, age, type_employment, type_worker, stratum_number,
            income_frequency, monthly_income, essential_expenses
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        values = (
            user.name, 
            user.age, 
            user.type_employment, 
            user.type_worker, 
            user.stratum_number,
            user.income_frequency, 
            user.monthly_income, 
            user.essential_expenses
        )
        
        cursor.execute(query, values)
        conn.commit()
        
        new_id = cursor.lastrowid
        conn.close()
        
        return {"message": "User Created", "id": new_id}

    except Exception as e:
        
        raise HTTPException(
            status_code=500, 
            detail="Error interno del servidor al crear el usuario."
        )

# STEP 6: FINAI ANALYSIS ENGINE

@app.get("/users/{user_id}/advice")
async def generate_financial_advice(user_id: int):
    """
    **FinAI Core Engine**
    Fetches user data, sends it to Gemini with strict socioeconomic context rules,
    updates the database with the generated score/profile, and returns the advice.
    """
    try:
        conn = sqlite3.connect('fin_ai.db')
        cursor = conn.cursor()
        
        # 1. Buscar el expediente del usuario en el archivero
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user_data = cursor.fetchone()
        
        if not user_data:
            conn.close()
            raise HTTPException(status_code=404, detail="Usuario no encontrado en la base de datos.")

        column_names = [description[0] for description in cursor.description]
        user_dict = dict(zip(column_names, user_data))
