from fastapi import FastAPI
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from openai import OpenAI
from fastapi.middleware.cors import CORSMiddleware
# 加载 .env
load_dotenv()

# 创建 FastAPI 实例
app = FastAPI(title="BookTok FastAPI MVP")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化 OpenAI（支持中转）
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")
)

# 请求体结构
class ScriptRequest(BaseModel):
    book_title: str

# 测试接口
@app.get("/")
def root():
    return {"message": "BookTok API is running 🚀"}

# 生成脚本接口
@app.post("/api/scripts/generate")
def generate_script(req: ScriptRequest):
    prompt = f"""
You are a viral BookTok creator.

Create 5 short TikTok video scripts for this book:
{req.book_title}

Each script must include:
- Hook
- Conflict
- Emotion
- CTA

Make it highly engaging and emotional.
"""

    response = client.responses.create(
        model=os.getenv("OPENAI_MODEL"),
        input=prompt
    )

    return {
        "book_title": req.book_title,
        "scripts": response.output_text
    }