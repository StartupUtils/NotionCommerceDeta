from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from CommerceApi.utils.database import DetaBase as DB
from CommerceApi.models.store import Cart, CuratedCart, CartItem, Product, ModCommand
from CommerceApi.utils.stripe import StripeManager
from CommerceApi.config import Config

stripe = StripeManager(Config.stripe_key)

router = APIRouter(
    prefix="/api",
    tags=["product"],
    responses={404: {"description": "Not found"}},
)

product_client = DB("products")
curated_cart = DB("curated_cart")

@router.get("/product/{target}", status_code=201)
async def get_product(target: str):
    """Find a product and return data"""
    if ":" in target:
        product_id = target.split(":")[0]
        product = await product_client.get(product_id)
        # Check if product has data
        if product is None:
            return JSONResponse(
                status_code=400,
                content={"message": f"No product with id {product_id}.", "ok": False, "issue_type": "not_found"},
            )
        
        if product.get("display") == True:
            return JSONResponse(status_code=200, content=product)
        return JSONResponse(status_code=400, content={"message": f"Product is not enabeld for display", "ok": False, "issue_type": "not_displayed"})
    return JSONResponse(status_code=400, content={"message": f"Could not parse {target}", "ok": False, "issue_type": "id_parse"})

@router.post("/cart", status_code=200)
async def cart(cart: Cart):
    total = 0
    listings = []
    pricing = []

    for item in cart.data:
        product_info = await product_client.get(item.id)
        display = product_info.get("display")
        price = product_info.get("price")
        images = product_info.get("images")
        title = product_info.get("title")
        data = {
            "id": item.id,
        }
        if display and price and item.quant > 0:
            total += (price * item.quant)
            data["price"] = price
            data["quant"] = item.quant
            image = None
            if len(images) > 0:
                image = images[0]
            data["image"] = image
            data["title"] = title
            listings.append(data)
    
    return {
        "pricing": [{"subject": "Subtotal", "price": f"${round(total, 2)}"}, {"subject": "Shipping", "price": "$5"},{"subject": "Tax", "price": None}],
        "listings": listings
    }

@router.post("/createorder", status_code=200)
async def createorder(cart: CuratedCart):
    data = cart.dict()
    try:
        await curated_cart.insert(data)
        return data
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e), "ok": False})

@router.get("/removeitem/{order_key}/{item_key}", status_code=200)
async def removeitem(order_key: str, item_key: str):
    try:
        order = await curated_cart.get(order_key)
        order_obj = CuratedCart(**order)
        order_obj.removeitem(item_key)
        await curated_cart.update({"data": order_obj.data}, order_key)
        return order_obj.dict()
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e), "ok": False})

@router.post("/updateorder/{order_key}", status_code=200)
async def updateorder(order_key: str, item: CartItem):
    try:
        order = await curated_cart.get(order_key)
        order_obj = CuratedCart(**order)
        order_obj.updatecart(item)
        updated_data = order_obj.dict()
        await curated_cart.update({"data": updated_data.get("data")}, order_key)
        return updated_data
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e), "ok": False})

@router.get("/products", status_code=200)
async def allproducts():
    try:
        products = await product_client.find_many({"display": True})
        res = []
        for data in products:
            image = None
            if len(data.get("images")) > 0:
                image = data.get("images")[0]
            pack = {
                "image": image,
                "price": data.get("price"),
                "key": data.get("key"),
                "title": data.get("title")
            }
            res.append(pack)
        return res
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e), "ok": False})

@router.get("/removeitem/{order_key}/{item_key}", status_code=200)
async def removeitem(order_key: str, item_key: str):
    try:
        order = await curated_cart.get(order_key)
        order_obj = CuratedCart(**order)
        order_obj.removeitem(item_key)
        await curated_cart.update({"data": order_obj.data}, order_key)
        return order_obj.dict()
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e), "ok": False})

@router.post("/updateorder/{order_key}", status_code=200)
async def updateorder(order_key: str, item: CartItem):
    try:
        order = await curated_cart.get(order_key)
        order_obj = CuratedCart(**order)
        order_obj.updatecart(item)
        updated_data = order_obj.dict()
        await curated_cart.update({"data": updated_data.get("data")}, order_key)
        return updated_data
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e), "ok": False})

@router.get("/customcart/{order_key}", status_code=200)
async def getorder(order_key: str):
    try:
        listings = []
        subtotal = 0
        order = await curated_cart.get(order_key)
        order_obj = CuratedCart(**order)
        for item in order_obj.data:
            product_info = await product_client.get(item.id)
            product = Product(**product_info)
            if product.display:
                subtotal += product.total_price(item.quant)
                data = product.prep(item)
                listings.append(data)
        si = "$"
        price = f"{si}%.2f" % round(subtotal, 2)
        res = order_obj.dict()
        res['data'] = listings
        res["pricing"] = [
            {
                "subject": "Subtotal",
                "price": price
            },
            {
                "subject": "Shipping",
                "price": "$5.00"
            },
            {
                "subject": "Tax",
                "price": None
            },
        ]
        return res
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e), "ok": False})

@router.get("/checkout/{order_key}", status_code=200)
async def checkout(order_key: str):
    try:
        listings = []
        order = await curated_cart.get(order_key)
        order_obj = CuratedCart(**order)
        for item in order_obj.data:
            product_info = await product_client.get(item.id)
            product = Product(**product_info)
            if product.display:
                listings.append({"price": product.price_id, "quantity": item.quant})

        YOUR_DOMAIN = "https://matthewlsession.com"
        checkout_session = stripe.create_link(listings)
        return {"url": checkout_session.url}
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e), "ok": False})

@router.post("/modcart", status_code=200)
async def modcart(command: ModCommand):
    try:
        order = await curated_cart.get(command.order_key)
        order_obj = CuratedCart(**order)
        if command.command == "remove":
            order_obj.removeitem(command.product_key)
        elif command.command == "add":
            order_obj.add(command.product_key)
        elif command.command == "neg":
            order_obj.neg(command.product_key)
        data = order_obj.dict()
        await curated_cart.update({"data": data.get("data")}, command.order_key)
        return data
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e), "ok": False})