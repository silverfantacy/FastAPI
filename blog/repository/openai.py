import os
from fastapi import HTTPException, status
from openai import OpenAI
from .. import schemas


client = OpenAI(
    # this is also the default, it can be omitted
    api_key=os.getenv("OPENAI_API_KEY", ""),
)


def chat(request: schemas.Chat, system: schemas.message):
    messages_json = [message.model_dump() for message in request.messages]
    messages_json.insert(0, system)
    completion = client.chat.completions.create(
        model=request.model,
        messages=messages_json
    )
    choices = completion.choices
    if not choices:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"NO RESPONSE")
    return choices[0].message.content
