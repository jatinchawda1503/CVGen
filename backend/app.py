import sys
import logging
import asyncio
from PyPDF2 import PdfReader
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from typing import Union, AsyncIterable
from langchain.callbacks import AsyncIteratorCallbackHandler
import uvicorn
from config import CONFIG
from prompts.prompts import CV_PROMPT  # Fix incorrect import path

sys.path.append(CONFIG.get_root_path())
logger = logging.getLogger("uvicorn")
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*", "http://127.0.0.1:5500"],  # Removed the wildcard from the URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

openai_api_key = CONFIG.get_openai_api_key()
callback = AsyncIteratorCallbackHandler()


def get_model():
    return ChatOpenAI(
        model="gpt-3.5-turbo-1106",
        temperature=0.8,
        openai_api_key=openai_api_key,
        streaming=True,
        callbacks=[callback]
    )


def read_pdf(file):
    if file is not None:
        try:
            pdf = PdfReader(file)
            text = ""
            for page in pdf.pages:
                text += page.extract_text()
            processed_text = text
        except Exception as e:
            processed_text = None
            print(f"Error reading PDF: {e}")
    else:
        print("Cannot read the file")
        processed_text = None

    return processed_text


async def send_response(pdf_content: str,
                        jd: str,
                        words: str,
                        position: str,
                        additional_instructions: str) -> AsyncIterable[str]:
    llm = get_model()
    chain = LLMChain(
        llm=llm,
        prompt=PromptTemplate(template=CV_PROMPT, input_variables=["resume", "jd", "position", "words",
                                                                   "additional_instructions"]),
    )
    task = asyncio.create_task(
        chain.ainvoke({"jd": jd, "resume": pdf_content, "words": words, "position": position,
                       "additional_instructions": additional_instructions}))

    try:
        async for token in callback.aiter():
            yield token
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Error Streaming Tokens")
    finally:
        callback.done.set()
    await task


llm = get_model()


@app.post("/CvGen/")
async def generate_cv(resume: str = Form(),
                      position: str = Form(),
                      words: str = Form(),
                      jd: str = Form(),
                      additional_instructions: Union[str, None] = Form(default=None)):
    try:
        response = send_response(resume, jd, words, position, additional_instructions)
        return StreamingResponse(response, media_type="text/html")
    except Exception as e:
        print("Error occurred while generating CV", e)
        raise HTTPException(status_code=500, detail=f"Error occurred while generating CV: {e}")


if __name__ == '__main__':
    uvicorn.run("app:app", host='127.0.0.1', port=8000, reload=True)
