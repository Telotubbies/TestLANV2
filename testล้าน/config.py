import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost:5432/testlan")
    UPLOAD_DIR   = os.getenv("UPLOAD_DIR", "./uploads")
    PUBLIC_BASE  = os.getenv("PUBLIC_BASE_URL", "http://localhost:8000")
    PORT         = int(os.getenv("PORT", "8000"))
