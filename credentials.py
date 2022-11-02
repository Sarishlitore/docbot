"""
Credentials
"""
import os
from os.path import join, dirname

from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), 'credentials.env')
load_dotenv(dotenv_path)
bot_token = os.environ.get('BOT_TOKEN')
