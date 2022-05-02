from asyncio import FastChildWatcher
import re

def is_valid_email(email):
    #Expresion regular de email
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    # pass the regular expression
    # and the string into the fullmatch() method
    if(re.fullmatch(regex, email)): return True
    else: return False