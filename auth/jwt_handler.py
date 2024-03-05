# This file is responsible for signing, enconding, decoding and retutrning JWTs
import time # limit the token, expire time
import jwt 
from dotenv import load_dotenv
import os

load_dotenv(".env")

JWT_SECRET = os.environ.get("SECRET_KEY")
JWT_ALGORITHM = os.environ.get("ALGORITHM")

# Function returns the generated Tokens (JWTs)
def token_response(token:str):
    return {
        "access_token": token
    }

# Fuction used for signIn the JWT string   
def signJWT(userId:str):
    payload = {
        "userId": userId,
        "expiry": time.time() + 600
    }
    token = jwt.encode(payload, JWT_SECRET, algorith=JWT_ALGORITHM)
    return token_response(token)

def decodeJWT(token:str):
    decode_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    return decode_token if decode_token['exp'] >= time.time() else None
    