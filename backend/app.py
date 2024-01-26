from dotenv import load_dotenv
import os
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain import FAISS
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from pydantic import BaseModel, Field
from typing import Annotated
from fastapi import FastAPI,File,Form, UploadFile,Body
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional,Union
# import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*","http://127.0.0.1:5500/*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()

openai_api_key = os.getenv('OPENAI_API_KEY')



def get_model():
    llm = ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0.8, openai_api_key=openai_api_key)
    return llm

llm = get_model()


embeddings = OpenAIEmbeddings(openai_api_key =openai_api_key)

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
        


#read_pdf_file = read_pdf(file)

# chain = LLMChain(
#     llm=llm,
#     prompt=PromptTemplate(template=CV_PROMPT, input_variables=["resume","jd","position","words"]),
#     verbose=True
# )

# result = chain.run({"jd": jd, "resume": read_pdf_file, "words" : "200", "position" : "Machine Learning Engineer"})



@app.get("/")
async def root():
    return {"message": "Hello World"}

# class InputVars(BaseModel):
#     pdf =  Annotated[UploadFile, File()]
#     position: Annotated[str, Form()]
#     words: Annotated[str, Form()]
#     additional_instruations: Optional[Annotated[str, Form()]]
#     jd: Annotated[str,Form()]


@app.post("/CvGen")
async def genratecv(file: UploadFile = File(), 
                    position: str = Form(), 
                    words: str = Form(), 
                    jd: str = Form(),
                    additional_instructions: Union[str, None] = Form(default=None)):
    try:
        # Your processing logic here
        print(file.filename)    
        return {'response': file.filename}
    except:
        print("not fond error")


# if __name__ == '__main__':
#     uvicorn.run(app, host='127.0.0.1', port=8000)