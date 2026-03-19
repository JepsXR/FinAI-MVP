# Step 1: IMPORT

from fastapi import FastAPI, HTTPException
from typing import List, Optional
from pydantic import BaseModel
from dotenv import load_dotenv
import google.generativeai as genai
import os
import sqlite3

# Step 2: SERVER ACTIVATION

app = FastAPI(
    title="FinAI agent",
    description="Fin it's a agent that explain financial terms to people in a simple way ",
    version="1.0.0"
)

load_dotenv()

keymaster = os.getenv("FINAI_API_KEY")
if keymaster is None:
    print("Ups....don't find api key")
else:
    genai.configure(api_key=keymaster)
    print("Sucessfull connection")

# Step 3: DATABASE CONNECTION AND CREATION OF ITS ARCHITECTURE

connection = sqlite3.connect('fin_ai.db')
cursor = connection.cursor()

fin_table_sql = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,              
    name TEXT UNIQUE NOT NULL,
    age INTEGER
    test_score INTEGER DEFAULT 0
    risk_profile TEXT DEFAULT 'waiting'
)
"""

cursor.execute(fin_table_sql)
connection.commit()
print("¡Data saved sucessfully!")
connection.close()

# STEP 4: CREATION OF ENDPOINTS
