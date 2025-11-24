from fastapi import APIRouter, Depends
from typing import Annotated
from schema.vendors import FoodItem
from schema.users import User
from auth import get_current_user
from deps import init_db_connection, close_db_connection
import uuid

router = APIRouter()

@router.post("/add-food-item")
def add_food_item(current_user: Annotated[User, Depends(get_current_user)] ,food_item: FoodItem):
    if not current_user.role == 'vendor':
        return {"message":"Only vendors can add food items"}
    conn, cur = init_db_connection()
    cur.execute("INSERT INTO food(name, quantity, price, vendor_id) VALUES(%s, %s, %s, %s)",(food_item.name, food_item.quantity, food_item.price, str(current_user.id)))
    conn.commit()
    close_db_connection(conn, cur)
    return {"message":"Food successfully Added", "data": food_item}

@router.delete("/remove/{food_id}")
def delete_food_item(current_user: Annotated[User, Depends(get_current_user)] ,food_id: uuid.UUID):
    if not current_user.role == 'vendor':
        return {"message":"Only vendors can add food items"}
    conn, cur = init_db_connection()
    cur.execute("DELETE FROM food WHERE id = %s",(str(food_id),))
    conn.commit()
    close_db_connection(conn, cur)
    return {"message":"Food Deleted Successfully"}

@router.get("/get-orders")
def get_orders(current_user: Annotated[User, Depends(get_current_user)]):
    if not current_user.role == 'vendor':
        return {"message":"Only vendors can add food items"}
    conn, cur = init_db_connection()
    cur.execute("SELECT * FROM orders WHERE vendor_id = %s",(str(current_user.id),))
    orders = cur.fetchall()
    close_db_connection(conn, cur)
    return {"message":"Orders fetched successfully", "data": orders}