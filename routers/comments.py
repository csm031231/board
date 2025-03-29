from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dto import CommentCreateDTO, CommentResponseDTO, CommentUpdateDTO
from base import get_db
from model import Comment, Post, User
from security import get_current_user

router = APIRouter(prefix="/comments", tags=["comments"])

def create_comment_in_db(db: Session, comment: Comment) -> Comment:
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment

def comment_create_service(db: Session, user_id: int, comment_data: CommentCreateDTO) -> Comment:
    post = db.query(Post).filter(Post.id == comment_data.post_id).first()
    if not post:
        raise Exception("Post not found")
    new_comment = Comment(
        content=comment_data.content,
        user_id=user_id,
        post_id=comment_data.post_id
    )
    return create_comment_in_db(db, new_comment)

@router.post("/", response_model=CommentResponseDTO)
def create_comment(comment_data: CommentCreateDTO, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        comment = comment_create_service(db, current_user.id, comment_data)
        return comment
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.put("/{comment_id}")
def update_comment(comment_id: int, comment_data: CommentUpdateDTO, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    comment = db.query(Comment).filter(Comment.id == comment_id, Comment.user_id == current_user.id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    comment.content = comment_data.content
    db.commit()
    db.refresh(comment)
    return {"message": "Comment updated successfully!"}


@router.delete("/{comment_id}")
def delete_comment(comment_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    comment = db.query(Comment).filter(Comment.id == comment_id, Comment.user_id == current_user.id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    db.delete(comment)
    db.commit()
    return {"message": "Comment deleted successfully!"}