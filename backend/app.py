import logging
import asyncio
from PyPDF2 import PdfReader
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.chains.openai_functions.base import create_structured_output_runnable
from langchain.prompts import PromptTemplate
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from typing import Union, AsyncIterable
from langchain.callbacks import AsyncIteratorCallbackHandler
import uvicorn
from config import CONFIG
from prompt.prompts import CV_PROMPT  # Fix incorrect import path
from pydantic import BaseModel, Field

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
        callbacks=[callback],
        verbose=True
    )

class OutputStrucutre(BaseModel):
    answer: str = Field(description= "Answer in markdown format")

async def send_response(pdf_content: str,
                        jd: str,
                        words: str,
                        position: str,
                        additional_instructions: str) -> AsyncIterable[str]:
    llm = get_model()
    markdown_schema = ResponseSchema(name="Answer", description="Return response in markdown format")
    struct_parser = JsonOutputFunctionsParser()
    chain = LLMChain(
        llm=llm,
        prompt=PromptTemplate(template=CV_PROMPT, 
                              input_variables=["resume", "jd", "position", "words",
                                                                   "additional_instructions"], 
                              #partial_variables={"format_instructions": struct_parser.get_format_instructions()}
                              ),
            #output_parser=struct_parser,
    )
    task = asyncio.create_task(
        chain.ainvoke({"jd": jd, 
                       "resume": pdf_content, 
                       "words": words, 
                       "position": position,
                       "additional_instructions": additional_instructions}))

    try:
        async for token in callback.aiter():
            print(token)
            yield token
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Error Streaming Tokens")
    finally:
        callback.done.set()
    await task


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
