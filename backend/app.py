import logging
import asyncio
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain,create_extraction_chain
from langchain.prompts import PromptTemplate
from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from typing import Union, AsyncIterable
from langchain.callbacks import AsyncIteratorCallbackHandler
from langchain.document_loaders import AsyncHtmlLoader
from langchain.document_transformers import Html2TextTransformer
import uvicorn
from config import CONFIG
from prompt.prompts import CV_PROMPT, JD_RAW  # Fix incorrect import path
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*", "http://127.0.0.1:5500"],  # Removed the wildcard from the URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

openai_api_key = CONFIG.get_openai_api_key()


async def send_response(pdf_content: str,
                        jd: str,
                        words: str,
                        position: str,
                        additional_instructions: str) -> AsyncIterable[str]:
    callback = AsyncIteratorCallbackHandler()
    llm = ChatOpenAI(
        model="gpt-3.5-turbo-1106",
        temperature=0.8,
        openai_api_key=openai_api_key,
        streaming=True,
        callbacks=[callback],
        verbose=True
    )
    chain = LLMChain(
        llm=llm,
        prompt=PromptTemplate(template=CV_PROMPT, 
                              input_variables=["resume", 
                                               "jd", 
                                               "position", 
                                               "words",
                                                "additional_instructions"]))
    task = asyncio.create_task(
        chain.ainvoke({"jd": jd, 
                       "resume": pdf_content, 
                       "words": words, 
                       "position": position,
                       "additional_instructions": additional_instructions}))

    data_yielded = False
    try:
        async for token in callback.aiter():
            yield token
            data_yielded = True
            await asyncio.sleep(0)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Error Streaming Tokens")
    finally:
        callback.done.set()
    
    await task

    if not data_yielded:
        raise HTTPException(status_code=204, detail="No content")
    
schema = {
     "properties":{
        "job_description":{"type": "string"},
     },
        "required": ["job_description"]
 }
    
async def getJDfromUrl(url):
    start_time = time.time()
    loader = AsyncHtmlLoader([url])
    raw = loader.load()
    print("time took to load html", time.time() - start_time)
    transfomer = Html2TextTransformer()
    print("time took to load transform", time.time() - start_time)
    raw_text = transfomer.transform_documents(raw)[0].page_content
    print("time took to extract raw text", time.time() - start_time)
    llm=ChatOpenAI(model="gpt-3.5-turbo-1106", #gpt-3.5-turbo-1106 , gpt-3.5-turbo-16k
                   openai_api_key=openai_api_key, 
                    temperature=0.9)
    prompt = PromptTemplate(template=JD_RAW, 
                            input_variables=["raw_text"])
    chain = create_extraction_chain(llm=llm, prompt=prompt, schema=schema)
    print("time took to create chain", time.time() - start_time)
    response = chain.invoke({raw_text})
    print("time took to extract job description", time.time() - start_time)
    return response['text'][0]['job_description']
    
@app.post("/CvGen/")
async def generate_cv(resume: str = Form(),
                      position: str = Form(),
                      words: str = Form(),
                      option:str = Form(),
                      jd: str = Form(),
                      additional_instructions: Union[str, None] = Form(default=None)):
    try:
        if (option == 'detectByUrl'):
            description = await getJDfromUrl(jd)
        else:
            description = jd  
        print("Extracted description, generating CV...")
        response = send_response(resume, description, words, position, additional_instructions)
        return StreamingResponse(response, media_type="text/html")
    except Exception as e:
        print("Error occurred while generating CV", e)
        raise HTTPException(status_code=500, detail=f"Error occurred while generating CV: {e}")


if __name__ == '__main__':
    uvicorn.run("app:app", host='127.0.0.1', port=8000, reload=False)