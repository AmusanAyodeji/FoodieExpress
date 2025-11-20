from fastapi import APIRouter, Depends
from typing import Annotated
from schema.users import User
from auth import get_current_user
from schema.orders import OrderItem
from deps import init_db_connection, close_db_connection

router = APIRouter()

@router.get("/place-order")
def place_order(current_user: Annotated[User, Depends(get_current_user)],order: OrderItem):
    conn, cur = init_db_connection()
    cur.execute("SELECT price FROM food WHERE id = %s",(order.food_id,))
    price = cur.fetchone()
    price = price[0]
    cur.execute("SELECT user_id FROM food WHERE id = %s",(order.food_id,))
    vendor_id = cur.fetchone()
    cur.execute("INSERT INTO orders(food_id, quantity, user_id, price, vendor_id) VALUES(%s, %s, %s, %s)",(order.food_id, order.quantity, current_user.id, order.quantity * price, vendor_id))
    conn.commit()
    close_db_connection(conn, cur)
    return {"message":"Order placed successfully", "data": order}

@router.get("/order-history")
def order_history(current_user: Annotated[User, Depends(get_current_user)]):
    conn, cur = init_db_connection()
    cur.execute("SELECT * FROM orders WHERE user_id = %s",(current_user.id,))
    orders = cur.fetchall()
    close_db_connection(conn, cur)
    return {"message":"Order history fetched successfully", "data": orders}
    