from fastapi import FastAPI, Depends, HTTPException
from auth import AuthHandler
from pydantic import BaseModel


class AuthDetails(BaseModel):
    useremail: str
    password: str

app = FastAPI()

auth_handler = AuthHandler()
users = [

]

# @app.post('/register', status_code=201)
# def register(auth_details: AuthDetails):
#     if any(x['useremail'] == auth_details.useremail for x in users):
#         raise HTTPException(status_code=400, detail='Username is taken')
#     # hashed_password = auth_handler.get_password_hash(auth_details.password)
#     users.append({
#         'useremail': auth_details.useremail,
#         'password': auth_details.password   
#     })
#     return


@app.post('/login')
def login(auth_details: AuthDetails):
    user = None
    for x in users:
        if x['useremail'] == auth_details.useremail:
            user = x
            break
    
    if (user is None) or (not auth_handler.verify_password(auth_details.password, auth_handler.get_password_hash(user['password']))):
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    token = auth_handler.encode_token(user['useremail'])
    return { 'token': token }


@app.get('/unprotected')
def unprotected():
    return { 'hello': 'world','users':users }


@app.get('/protected')
def protected(useremail=Depends(auth_handler.auth_wrapper)):
    return { 'name': useremail }