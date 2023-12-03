from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import schemas, models, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

@router.get('/', response_model=List[schemas.Product])
def get_all_products(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return products

@router.get('/{id}', response_model=schemas.Product)
def get_product(id:int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.product_id == id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id {id} not found")
    return product

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Product)
def create_product(request: schemas.Product, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    if current_user.is_admin == False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Unauthorized")
    new_product = models.Product(**request.model_dump())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
async def update_product(id:int, request: schemas.Product, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    if current_user.is_admin == False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Unauthorized")
    product = db.query(models.Product).filter(models.Product.product_id == id)
    if not product.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id {id} not found")
    product.update(request.model_dump())
    db.commit()
    return Response(status_code=status.HTTP_202_ACCEPTED)

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(id:int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    if current_user.is_admin == False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Unauthorized")
    product = db.query(models.Product).filter(models.Product.product_id == id)
    if not product.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id {id} not found")
    product.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)