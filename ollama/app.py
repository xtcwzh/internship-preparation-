import uuid

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from llm_chain import stream_chat, chat_histories

app = FastAPI(title="算法题解析助手")
templates = Jinja2Templates(directory="templates") # 模板引擎


class ChatRequest(BaseModel): #定义请求的样子
    message: str
    session_id: str | None = None


@app.get("/", response_class=HTMLResponse)#表示返回的是html页面而不是json
async def index(request: Request): #async表示异步，request: Request表示请求的类型
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/chat")
async def chat(req: ChatRequest):
    session_id = req.session_id or str(uuid.uuid4())

    async def event_generator():
        async for token in stream_chat(session_id, req.message):
            # SSE 格式: data: ...\n\n
            yield f"data: {token}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Session-Id": session_id,
        },
    )


@app.post("/clear")
async def clear_history(req: ChatRequest):
    session_id = req.session_id
    if session_id and session_id in chat_histories:
        del chat_histories[session_id]
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
