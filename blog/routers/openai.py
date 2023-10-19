from fastapi import APIRouter, Depends, status
from .. import schemas
from ..repository import openai

router = APIRouter(
    prefix="/openai",
    tags=["OpenAI"]
)


@router.post("/chat", status_code=status.HTTP_200_OK)
async def chat(request: schemas.Chat):
    system = {'role': "system", 'content': '#zh-tw As a system, my role is to provide direct and concise answers in a contextual and conversational style. My responses should be casual and avoid opposition, warning, or summarization. I should not provide abstract or detailed explanations or trace the origins of a question.'}
    return openai.chat(request, system)
