from fastapi import APIRouter, Depends
from typing import Annotated
from schema.users import User
from auth import get_current_user
from schema.orders import OrderItem
from deps import init_db_connection, close_db_connection
import uuid

student_router = APIRouter()

@student_router.post("/place-order")
def place_order(current_user: Annotated[User, Depends(get_current_user)], order: OrderItem):
    if not current_user.role == 'student':
        return {"message":"Only students can place orders"}
    conn, cur = init_db_connection()
    cur.execute("SELECT price FROM food WHERE id = %s",(str(order.food_id),))
    price = cur.fetchone()
    price = price[0]
    cur.execute("SELECT vendor_id FROM food WHERE id = %s",(str(order.food_id),))
    vendor_id = cur.fetchone()
    cur.execute("INSERT INTO orders(food_id, quantity, user_id, price, vendor_id) VALUES(%s, %s, %s, %s, %s)",(str(order.food_id), order.quantity, str(current_user.id), order.quantity * price, vendor_id))
    conn.commit()
    close_db_connection(conn, cur)
    return {"message":"Order placed successfully", "data": order}

@student_router.get("/order-history")
def order_history(current_user: Annotated[User, Depends(get_current_user)]):
    if not current_user.role == 'student':
        return {"message":"Only students can place orders"}
    conn, cur = init_db_connection()
    cur.execute("SELECT * FROM orders WHERE user_id = %s",(str(current_user.id),))
    orders = cur.fetchall()
    close_db_connection(conn, cur)
    return {"message":"Order history fetched successfully", "data": orders}


@student_router.get("/view-vendors")
def view_vendors(current_user: Annotated[User, Depends(get_current_user)]):
    if not current_user.role == 'student':
        return {"message":"Only students can place orders"}
    conn, cur = init_db_connection()
    cur.execute("SELECT DISTINCT users.id, users.full_name FROM users JOIN food ON users.id = food.vendor_id WHERE users.role = 'vendor'")
    vendors = cur.fetchall()
    close_db_connection(conn, cur)
    return {"message":"Vendors fetched successfully", "data": vendors}

@student_router.get("/view-menu")
def view_menu(current_user: Annotated[User, Depends(get_current_user)], vendor_id: uuid.UUID):
    if not current_user.role == 'student':
        return {"message":"Only students can place orders"}
    conn, cur = init_db_connection()
    cur.execute("SELECT * FROM food WHERE vendor_id = %s",(str(vendor_id),))
    menu = cur.fetchall()
    close_db_connection(conn, cur)
    return {"message":"Menu fetched successfully", "data": menu}

@student_router.delete("/remove-order/{order_id}")
def remove_order(current_user: Annotated[User, Depends(get_current_user)] ,order_id: uuid.UUID):
    if not current_user.role == 'student':
        return {"message":"Only students can place orders"}
    conn, cur = init_db_connection()
    cur.execute("DELETE FROM orders WHERE id = %s AND user_id = %s",(str(order_id), str(current_user.id)))
    conn.commit()
    close_db_connection(conn, cur)
    return {"message":"Order Removed Successfully"}


#add endpoint to view current order that can be paid for, like a view cart endpoint

#add endpoint to generate payment link for order to pay and update db to make the orders dat were paid for have their boolean value for paid be updated to true