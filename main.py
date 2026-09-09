from dotenv import load_dotenv
import os
import json
import logging
from datetime import datetime

from google import genai
import gspread
from google.oauth2.service_account import Credentials
from telegram import Update
from telegram.ext import Application, ContextTypes, MessageHandler, filters

load_dotenv()

TELEGRAM_BOT_KEY = os.environ.get("TELGRAM_BOT_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GOOGLE_SHEET_NAME = "Jimmy's Financial logs"
SERVICE_ACCOUNT_FILE = "service_account.json"  

logging.basicConfig(
    level=logging.INFO,
    filename='app.log',
    filemode='a',
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

client = genai.Client(api_key=GEMINI_API_KEY)
MODEL_NAME = "gemini-3.1-flash-lite"

SYSTEM_PROMPT = """Kamu parser pencatat keuangan. Ubah pesan berikut menjadi JSON
dengan format persis: {{"kategori": string, "nominal": number, "deskripsi": string}}.
Balas HANYA JSON, tanpa penjelasan apapun, tanpa markdown code block.

Pesan: {message_text}"""