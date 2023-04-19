from fastapi import APIRouter
from app.config.db import client
from app.schemas.user import User, Order
from bson import ObjectId
# from app.schemas.user import Order, ItemInOrder
from app.schemas.restaurant import Item

router = APIRouter()


@router.get('/')
async def path1():
    return {"message": "User Endpoint"}


@router.get('/locations')
async def location():

    rest_table = client["SEProject"]["Restaurant"]
    locations = rest_table.find({})
    locations_list = []
    for location in locations:
        for rest in rest_table:
            locations_list.append(
                {"restaurantLocation": rest["location"], "restaurantName": rest["location"]})

    return {
        "location": "Location Endpoint"
    }


@router.get('/all-locations')
async def all_locations():
    location_table = client["SEProject"]["Location"]
    locations = location_table.find({})
    locations_list = []
    for location in locations:
        locations_list.append({"location_name": location["location_name"]})

    return {
        "all-locations": locations_list
    }


@router.get('/displayitems/{location_name}')
# this funtion is for the khareedar landing screen where all the restaurants are being displayed
async def displayitems(location_name: str):
    items_table = client["SEProject"]["Item"]
    items_data = items_table.find({"item_location": location_name})

    # Construct the list of items to return
    items = []
    for item in items_data:
        items.append({"item_name": item["item_name"], "item_id": item["item_id"], "item_price": item["item_price"],
                     "item_location": item["item_location"], "item_desription": item["item_description"]})

    return {
        "displayItems": items
    }


@router.post('/place-order')
async def place_order(order: Order):
    order_table = client["SEProject"]["Order"]
    total_price = 0
    # Convert list of ItemInCart to list of dicts
    order_items = [dict(item) for item in order.items]
    for item in order.items:
        total_price += item.item_price * item.quantity

    order_table.insert_one({"items": order_items, "gender_preference": order.gender_preference,
                            "partial_order": order.partial_order, "total_price": total_price, "accepted": 0, "order_location": order_items[0]["item_location"]})

    return {"message": "Order Placed"}

# .................................. DOST ..................................

# dispay all orders


@router.get('/display-orders/{my_email}')
async def display_orders(my_email: str):
    order_table = client['SEProject']["Order"]
    user_table = client["SEProject"]["User"]
    me_user = user_table.find_one({"email": my_email})
    my_gender = me_user["gender"]
    orders_of_my_gender = order_table.find(
        {"accepted": 0, "gender_preference": my_gender})
    
    orders_of_none_gender = order_table.find(
        {"accepted": 0, "gender_preference": "None"})
    
    orders_list = []

    
    orders_list = [dict(ordr) for ordr in orders_of_my_gender]
    orders_list2 = [dict(ordr) for ordr in orders_of_none_gender]
    orders_list.extend(orders_list2)
    returning_list = []
    for order in orders_list:
        returning_list.append({"items": order["items"], "gender_preference": order["gender_preference"],
                            "partial_order": order["partial_order"], "total_price": order["total_price"], "accepted": 0, "order_location": order["order_location"] , "order_id" : str(order["_id"])})
    print(returning_list)

    return {
        "orders": returning_list
    }


@router.put('/accept-order')
async def accept_order(order_id: str):
    order_table = client["SEProject"]["Order"]
    order_table.update_one({"_id": ObjectId(order_id)}, {"$set": {"accepted": 1}})
    return {"message": "Order Accepted"}