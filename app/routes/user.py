from fastapi import APIRouter
from app.config.db import client
from app.schemas.user import User, Order
from bson import ObjectId
# from app.schemas.user import Order, ItemInOrder
from app.schemas.restaurant import Item
from app.schemas.user import ItemRequest
from app.schemas.user import Reviews
from app.schemas.user import Blocked
from app.schemas.user import Reported
from app.auth.provider import oauth2_scheme, get_password_hash, verify_password, create_access_token, return_user


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
        items.append({"item_name": item["item_name"], "item_id":str(item["_id"]) , "item_price": item["item_price"],
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

    user_table = client["SEProject"]["User"]
    # find the number of the user in the user_table
    user = user_table.find_one({"email": order.order_email})
    user_number = user["number"]

    order_table.insert_one({"items": order_items, "gender_preference": order.gender_preference,
                            "partial_order": order.partial_order, "total_price": total_price, "accepted": 0, "order_location": order_items[0]["item_location"] , "order_email": order.order_email , "order_number" : user_number})

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

    blocked_table = client["SEProject"]["Blocked"]
    me_blocked_users = blocked_table.find({"blockee_email": my_email})
    my_blocked_users  = blocked_table.find({"blocker_email": my_email})
    me_blocked_users = [user["blocker_email"] for user in me_blocked_users]
    my_blocked_users = [user["blockee_email"] for user in my_blocked_users]

    me_blocked_users.extend(my_blocked_users)
    print(me_blocked_users)


    orders_list = [dict(ordr) for ordr in orders_of_my_gender]
    orders_list2 = [dict(ordr) for ordr in orders_of_none_gender]
    orders_list.extend(orders_list2)
    returning_list = []
    for order in orders_list:
        if order["order_email"] not in me_blocked_users:
            returning_list.append({"items": order["items"], "gender_preference": order["gender_preference"],
                            "partial_order": order["partial_order"], "total_price": order["total_price"], "accepted": 0, "order_location": order["order_location"] , "order_id" : str(order["_id"]) , "order_number" : order["order_number"]})
            
    print(returning_list)

    return {
        "orders": returning_list
    }


@router.put('/accept-order')
async def accept_order(order_id: str):
    order_table = client["SEProject"]["Order"]
    order_table.update_one({"_id": ObjectId(order_id)}, {"$set": {"accepted": 1}})
    return {"message": "Order Accepted"}


@router.post('/request-item')
async def request_item(item: ItemRequest):
    request_table = client["SEProject"]["ItemRequest"]
    request_table.insert_one({"item_name": item.item_name, "item_location": item.item_location, "accepted": 0 , "requester_email" : item.requester_email})
    
    return {"message": "Item Requested"}

@router.post('/user-review/{my_email}')
async def user_review(review: Reviews):
    review_table = client["SEProject"]["Review"]
    review_table.insert_one({"reviewer_email": review.reviewer_email, "reviewee_email": review.reviewee_email, "review": review.review, "rating": review.rating})
    return {"message": "Review Added"}

@router.get('/my-reviews/{my_email}')
async def my_reviews(my_email: str):
    review_table = client["SEProject"]["Review"]
    reviews = review_table.find({"reviewee_email": my_email})
    # reviews_list = [dict(review) for review in reviews]
    reviews_list = []
    for rev in reviews:
        rev["_id"] = str(rev["_id"])
        reviews_list.append(rev)
    return {"reviews": reviews_list}

@router.post('/block-user')
async def block_user(block: Blocked):
    block_table = client["SEProject"]["Blocked"]
    block_table.insert_one({"blocker_email": block.blocker_email, "blockee_email": block.blockee_email})
    return {"message": "User Blocked"}
   
@router.post('/report-user')
async def report_user(report: Reported):
    report_table = client["SEProject"]["Reported"]
    report_table.insert_one({"reporter_email": report.reporter_email, "reportee_email": report.reportee_email , "situation": report.situation , "additional_comments" : report.additional_comments, "approved_by_admin": 0})
    return {"message": "User Reported"}



@router.get('/my-orders/{email}')
async def my_orders(email: str):
    order_table = client["SEProject"]["Order"]
    orders = order_table.find({"order_email": email})
    # orders_list = [dict(order) for order in orders]
    order_list = []
    for order in orders:
        order["_id"] = str(order["_id"])
        order_list.append(order)

    return {"orders": order_list}

