import os
import sys
from dotenv import load_dotenv
load_dotenv()

class CONFIG:
    @staticmethod
    def get_openai_api_key():
        return os.getenv('OPENAI_API_KEY')
    
    @staticmethod
    def get_root_path():
        return os.path.dirname(os.path.abspath(__file__))