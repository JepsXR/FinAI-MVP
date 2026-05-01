# FinAI Agent - Financial AI Assistant 🚀

## Description
FinAI is a backend agent designed to explain financial terms in a simple way. This project uses **FastAPI** to create a high-performance API and integrates **Google Gemini AI** to provide intelligent responses.

## Key Features
* **AI Integration:** Uses Google Generative AI to process financial queries.
* **Security:** Implements `.env` files to protect sensitive API keys.
* **Database:** Uses **SQLite** for lightweight data persistence.
* **Modern Stack:** Built with Python 3.10+ and FastAPI.

## Why I built this?
I have developed this project to demonstrate my skills in **Backend Development** and **API Integration**. I chose SQLite because it is perfect for this stage of development, and I prioritized security by managing credentials through environment variables.

## Tech Stack
* **Language:** Python
* **Framework:** FastAPI
* **AI:** Google Gemini API
* **Database:** SQLite

## ⚙️ How to run it locally

1. **Clone the repo:**
   `git clone https://github.com/JepsXR/FinAI-MVP

2. **Install dependencies:**
   `pip install fastapi uvicorn google-generativeai python-dotenv`

3. **Set up your environment:**
   Create a `.env` file and add your `API_KEY`.

4. **Run the server:**
   `uvicorn main:app --reload`
