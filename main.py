# Step 1: IMPORT

from fastapi import FastAPI, HTTPException
from typing import List, Optional, Literal
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import google.generativeai as genai
import os
import sqlite3

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

# Step 3: CREATION OF DATA MODELS

class DataUsers(BaseModel):
    name: str = Field(..., min_length=3, max_length=20)
    age: int = Field(..., gt=0, lt=100)
    type_employment: Literal["Formal", "Informal", "Unemployed","Student"] = Field(...)
    type_worker: Literal["Independent", "Employee", "Entrepreneur", "Businessman"] = Field(...)
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
    age INTEGER,
    type_employment TEXT,
    type_worker TEXT,
    stratum_number INTEGER,
    income_frequency TEXT,
    monthly_income INTEGER,
    essential_expenses INTEGER, 
    test_score INTEGER DEFAULT 0,
    risk_profile TEXT DEFAULT 'waiting'
)
"""

cursor.execute(fin_table_sql)
connection.commit()
print("¡Data saved sucessfully!")
connection.close()

# STEP 5: CREATION OF ENDPOINTS 

@app.post("/users", status_code=201)
async def register_new_user(user: DataUsers):
    """
**Financial Profile Registration and Persistence**
Captures essential socioeconomic data of the citizen (income, expenses, socioeconomic stratum, and type of employment)
and stores it in a structured format in the SQLite database.
* **Validation:** Ensures that the amounts are positive and the age/stratum ranges are valid.
* **Output:** Returns the user's unique ID for future analysis queries.
"""
