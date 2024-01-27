from config import CONFIG
import sys
sys.path.append(CONFIG.get_root_path())
from prompt.prompts import CV_PROMPT


import asyncio
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings

from langchain import FAISS
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from pydantic import BaseModel, Field
from typing import Annotated
from fastapi import FastAPI,File,Form, UploadFile,Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse 
from typing import Optional,Union,AsyncIterable

from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.callbacks import AsyncIteratorCallbackHandler

import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*","http://127.0.0.1:5500/*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

openai_api_key = CONFIG.get_openai_api_key()
callback = AsyncIteratorCallbackHandler()

def get_model():
    llm = ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0.8, openai_api_key=openai_api_key, streaming=True, callbacks = [callback])
    return llm


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
        
        
async def send_response(pdf_content:str,
                        jd:str,
                        words:str,
                        position:str,
                        additional_instructions:str) -> AsyncIterable[str]:
    llm = get_model()
    chain = LLMChain(
            llm=llm,
            prompt=PromptTemplate(template=CV_PROMPT, input_variables=["resume","jd","position","words","additional_instructions"])
        )
    task = asyncio.create_task(chain.ainvoke({"jd": jd, "resume": pdf_content, "words" : words, "position" : position,"additional_instructions":additional_instructions}))
    
    try:
       async for token in callback.aiter():
              yield token
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Error Steaming Tokens")
    finally:
        callback.done.set()
    await task

llm = get_model()

@app.post("/CvGen/")
async def genratecv(resume: str = Form(), 
                    position: str = Form(), 
                    words: str = Form(), 
                    jd: str = Form(),
                    additional_instructions: Union[str, None] = Form(default=None)):
    try:
        # if file.content_type == "application/pdf":
        #     read_pdf_file = read_pdf(file.file) 
        # else:
        #     raise HTTPException(status_code=400, detail="Only accepts pdf file")
        # read_pdf_file = read_pdf(file.file) 
        # print(read_pdf_file)
        # return {"response": {
        #     "file": resume,
        # }}
        response = send_response(resume,jd,words,position,additional_instructions)
        return StreamingResponse(response,  media_type="text/event-stream")
    except Exception as e:
        print("Error occured while generating CV",e)
        raise HTTPException(status_code=500,detail="Error occured while generating CV, {e}")
        

if __name__ == '__main__':
    uvicorn.run("app:app", host='127.0.0.1', port=8000, reload=True)