from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dto import PostCreateDTO, PostResponseDTO, UpdatePost
from base import get_db
from model import Post, User
from security import get_current_user

router = APIRouter(prefix="/posts", tags=["posts"])

def create_post_in_db(db: Session, post: Post) -> Post:
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

def post_create_service(db: Session, user_id: int, post_data: PostCreateDTO) -> Post:
    new_post = Post(
        title=post_data.title,
        content=post_data.content,
        user_id=user_id
    )
    return create_post_in_db(db, new_post)

@router.post("/", response_model=PostResponseDTO)
def create_post(post_data: PostCreateDTO, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        post = post_create_service(db, current_user.id, post_data)
        return post
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    post = db.query(Post).filter(Post.id == post_id, Post.user_id == current_user.id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(post)
    db.commit()
    return {"message": "Post deleted successfully!"}

@router.get("/my-posts")
def get_my_posts(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    posts = db.query(Post).filter(Post.user_id == current_user.id).all()
    return posts
@router.put("/{post_id}")
def update_post(post_id: int, post_data: UpdatePost, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    post = db.query(Post).filter(Post.id == post_id, Post.user_id == current_user.id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    post.title = post_data.title
    post.content = post_data.content
    db.commit()
    db.refresh(post)
    return {"message": "Post updated successfully!"}