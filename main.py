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
    description="Fin it's a agent that explains financial terms to people in a simple way ",
    version="1.0.0"
)

load_dotenv()

keymaster = os.getenv("FINAI_API_KEY")
if keymaster is None:
    print("Ups....don't find api key")
else:
    genai.configure(api_key=keymaster)
    print("Successful connection")

# Step 3: CONNECTION WITH A DATABASE

connection = sqlite3.connect('database')
cursor = connection.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)")
cursor.execute("INSERT INTO users (name) VALUES ('Your name')")

connection.commit()
print("¡Data saved successfully!")
connection.close()
