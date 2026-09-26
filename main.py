from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
import uvicorn
from models import User, CreateUser, UserResponse, UserLogIn, UserUpdate, ChangePassword
from security import *
from db import get_db

app = FastAPI()


@app.get('/')
def home():
    return {'messagge':'Welcome!'}

#Tutti gli utenti registrati
@app.get('/users/', response_model=list[UserResponse])
def all_users(db:Session = Depends(get_db)):
    users = db.query(User).all()
    return users

#Registra utente nel database
@app.post('/registration/', response_model=UserResponse) 
def registration(user:CreateUser, db:Session = Depends(get_db)):

    email_check = db.query(User).filter(User.email == user.email).one_or_none()

    if email_check:
        raise HTTPException(status_code=404, detail=f'Utente con {user.email} già esistente!')

    new_user = User(first_name = user.first_name, last_name = user.last_name, email = user.email, password = get_password_hash(user.password))

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

#LogIn
@app.post('/login/')
def login(user:UserLogIn, db:Session = Depends(get_db)):

    user_exists = db.query(User).filter(User.email == user.email).one_or_none()

    if not user_exists:
        raise HTTPException(status_code=404, detail=f'User inesistente!')

    if not verify_password(user.password, user_exists.password):
        raise HTTPException(status_code= 404, detail=f'Credenziali non valide')

    else:
        return f'LogIn...'

#Dati utente con email
@app.get('/users/{user_email}', response_model=UserResponse)
def get_user(user_email, db:Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_email).one_or_none()

    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail=f'{user_email} non esiste')

#Elimina Utente
@app.delete('/users/{user_email}')
def delete_user(user_email, db:Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_email).one_or_none()

    if user:
        db.delete(user)
        db.commit()
        return f'{user_email} eliminato'
    else:
        raise HTTPException(status_code=404, detail=f'{user_email} non esiste')

#Aggiorna dati utente
@app.put('/users/{email}', response_model=UserResponse)
def aggiorna_dati(email, user:UserUpdate, db:Session = Depends(get_db)):

    user_exists = db.query(User).filter(User.email == email).one_or_none()

    if user_exists:

        for key, value in user.dict().items():
            setattr(user_exists, key, value)

        db.commit()
        db.refresh(user_exists)
        return user_exists

    else:
        raise HTTPException(status_code=404, detail=f'{email} non esiste')

#Change password
@app.put('/users/changepass/{email}')
def change_password(email, user:ChangePassword, db:Session = Depends(get_db)):

    user_exists = db.query(User).filter(User.email == email).one_or_none()

    if user_exists:

        if verify_password(user.old_password, user_exists.password):

            if verify_password(user.new_password, user_exists.password):
                return f'Non puoi utilizzare la stessa password'

            else:
                user_exists.password = get_password_hash(user.new_password)
                db.commit()
                db.refresh(user_exists)
                return f'Password aggiornata con successo!'            
            
        else:
            return f'Password Errata!'

    else:
        raise HTTPException(status_code= 404, detail=f'{email} non esiste')



if __name__ == '__main__':
    uvicorn.run(app, port=5000)