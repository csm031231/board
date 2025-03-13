from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from dto import AddUserDTO, UpdateUserDTO, UserResponseDTO, TokenDTO
from base import get_db
from model import User
from security import hash_password, create_access_token, authenticate_user, get_current_user

router = APIRouter(prefix="/user", tags=["user"])

@router.post("/signup", response_model=UserResponseDTO)
def signup(user_data: AddUserDTO, db: Session = Depends(get_db)):
    try:
        if db.query(User).filter(User.username == user_data.username).first():
            raise HTTPException(status_code=400, detail="Username already exists")
        hashed_password = hash_password(user_data.password)
        new_user = User(
            username=user_data.username,
            password_hash=hashed_password,
            nickname=user_data.nickname
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error adding user: {str(e)}")

@router.post("/login", response_model=TokenDTO)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if user:
        token_data = {"sub": user.username, "type": "access"}
        token = create_access_token(token_data)
        return {"access_token": token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=401, detail="아이디 또는 비밀번호가 잘못되었습니다")

@router.delete("/{username}/del")
def delete_user(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        user_to_delete = db.query(User).filter(User.username == current_user.username).first()
        if not user_to_delete:
            raise HTTPException(status_code=404, detail=f"User {current_user.username} not found")
        db.delete(user_to_delete)
        db.commit()
        return {"message": f"User {current_user.username} deleted successfully!"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error deleting user: {str(e)}")

@router.put("/{username}/change")
def update_user(user_data: UpdateUserDTO, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        user_obj = db.query(User).filter(User.username == current_user.username).first()
        if not user_obj:
            raise HTTPException(status_code=404, detail="User not found")
        user_obj.username = user_data.username
        user_obj.nickname = user_data.nickname
        if user_data.password:
            user_obj.password_hash = hash_password(user_data.password)
        db.add(user_obj)
        db.commit()
        db.refresh(user_obj)
        return {"message": f"User {current_user.username} updated successfully!"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error updating user: {str(e)}")
