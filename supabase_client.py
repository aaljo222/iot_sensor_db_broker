import os
from dotenv import load_dotenv
from supabase import create_client

# 🔥 .env 로드 (가장 중요)
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("❌ Supabase 환경변수가 설정되지 않았습니다.")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
