from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import schemas, models, oauth2
from ..database import get_db


router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

@router.get('/', response_model=List[schemas.OrderOut])
async def get_all_users_orders(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    orders = db.query(models.Order).filter(models.Order.customer_id == current_user.id).all()
    return orders

@router.get('/all', response_model=List[schemas.OrderOut])
async def get_all_orders(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    if current_user.is_admin == False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Unauthorized")
    orders = db.query(models.Order).all()
    return orders

@router.get('/{id}', response_model=schemas.OrderOut)
async def get_order(id:int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    order = db.query(models.Order).filter(models.Order.customer_id == id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Order with id {id} not found")
    if order.customer_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Unauthorized")
    return order

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Order)
async def create_order(request: schemas.Order, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    product = check_product(request, db)
    new_order = create_new_order(request, db, current_user, product)
    update_product_stock(request, db)
    return new_order

def check_product(request: schemas.Order, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.product_id == request.product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id {request.product_id} not found")
    if product.product_stock < request.quantity:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Product stock is not enough")
    return product

def update_product_stock(request, db):
    product = db.query(models.Product).filter(models.Product.product_id == request.product_id).first()
    product.product_stock -= request.quantity
    db.commit()
    db.refresh(product)
    return product

def create_new_order(request, db, current_user, product):
    new_order = models.Order(
        customer_id=current_user.id,
        total_price=request.quantity*product.product_price,
        **request.model_dump()
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order

@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
async def update_order(id:int, request: schemas.Order, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    if current_user.is_admin == False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Unauthorized")
    order = db.query(models.Order).filter(models.Order.order_id == id)
    if not order.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Order with id {id} not found")
    order.update(request.model_dump())
    db.commit()
    return Response(status_code=status.HTTP_202_ACCEPTED)

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(id:int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    if current_user.is_admin == False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Unauthorized")
    order = db.query(models.Order).filter(models.Order.order_id == id)
    if not order.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Order with id {id} not found")
    order.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)