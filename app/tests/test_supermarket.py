from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

#Test Supermarket APIs
def test_add_item():
    response = client.post("/api/supermarket/add-item", json={
        "item_name": "A",
        "unit_price": 50,
        "special_price": {"quantity": 3, "price": 130}
    })
    assert response.status_code == 200
    assert response.json()["item_name"] == "A"
    assert response.json()["unit_price"] == 50
    assert response.json()["special_price"] == {"quantity": 3, "price": 130}

def test_add_item_invalid_payload():
    response = client.post("/api/supermarket/add-item", json={
        "item_name": "B"
    })
    assert response.status_code == 422

def test_fetch_all_items():
    response = client.get("/api/supermarket/")
    assert response.status_code == 200
    items = response.json()
    assert "A" in items

    item = items["A"]
    assert item["item_name"] == "A"
    assert item["unit_price"] == 50
    assert item["special_price"]["quantity"] == 3
    assert item["special_price"]["price"] == 130
    

def test_get_pricing():
    response = client.get("/api/supermarket/A/pricing")
    assert response.status_code == 200
    pricing = response.json()
    assert pricing["item_name"] == "A"
    assert pricing["unit_price"] == 50
    assert pricing["special_price"]["quantity"] == 3
    assert pricing["special_price"]["price"] == 130

def test_get_pricing_nonexistent_item():
    response = client.get("/api/supermarket/Z/pricing")
    assert response.status_code == 200
    assert response.json()["error"] == "Item not found."

def test_delete_item():
    response = client.delete("/api/supermarket/A")
    assert response.status_code == 200
    assert response.json()["message"] == "Item A deleted."

def test_delete_nonexistent_item():
    response = client.delete("/api/supermarket/Z")
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found."










# Test Cart APIs
def test_get_empty_cart():
    response = client.get("/api/cart/")
    assert response.status_code == 200
    assert response.json() == {}

def test_get_cart_items():
    client.post("/api/supermarket/add-item", json={
        "item_name": "A",
        "unit_price": 50,
        "special_price": {"quantity": 3, "price": 130}
    })
    client.post("/api/supermarket/add-item", json={
        "item_name": "B",
        "unit_price": 30,
        "special_price": {"quantity": 2, "price": 45}
    })
    client.post("/api/cart/add?items=AAB")

    response = client.get("/api/cart/")
    assert response.status_code == 200
    cart = response.json()

    assert "A" in cart
    assert "B" in cart
    assert cart["A"] == 2
    assert cart["B"] == 1

def test_reset_cart():
    client.post("/api/cart/add?items=AAB")

    response = client.post("/api/cart/reset")
    assert response.status_code == 200
    assert response.json()["message"] == "Cart has been reset."

    response = client.get("/api/cart/")
    assert response.status_code == 200
    assert response.json() == {}

def test_reset_empty_cart():
    response = client.get("/api/cart/")
    assert response.status_code == 200
    assert response.json() == {}

    response = client.post("/api/cart/reset")
    assert response.status_code == 200
    assert response.json()["message"] == "Cart has been reset."

    response = client.get("/api/cart/")
    assert response.status_code == 200
    assert response.json() == {}

def test_add_to_cart():
    response = client.post("/api/cart/add?items=AAB")

    assert response.status_code == 200
    assert response.json()["message"] == "Items added to cart."
    cart = response.json()["cart"]
    assert cart["A"] == 2
    assert cart["B"] == 1
    client.post("/api/cart/reset")

def test_add_mixed_case_items_to_cart():
    response = client.post("/api/cart/add?items=aaB")

    assert response.status_code == 200
    assert response.json()["message"] == "Items added to cart."
    assert response.json()["cart"]["A"] == 2
    assert response.json()["cart"]["B"] == 1
    client.post("/api/cart/reset")

def test_add_invalid_item_to_cart():
    response = client.post("/api/cart/add?items=Zz")
    assert response.status_code == 400
    assert response.json()["detail"] == "Bad input. One or more items are invalid."

def test_add_empty_string_to_cart():
    response = client.post("/api/cart/add?items=")

    assert response.status_code == 200
    assert response.json()["message"] == "Items added to cart."
    assert response.json()["cart"] == {}

def test_remove_from_cart():
    response = client.post("/api/cart/add?items=ABBA")

    response = client.post("/api/cart/remove?items=A")
    assert response.status_code == 200
    assert response.json()["message"] == "Items removed from cart."
    assert response.json()["cart"]["A"] == 1
    client.post("/api/cart/reset")

def test_remove_more_than_in_cart():
    client.post("/api/cart/add?items=AAB")

    response = client.post("/api/cart/remove?items=BB")
    assert response.status_code == 400
    assert response.json()["detail"] == "Cannot remove more than 1 of B."
    client.post("/api/cart/reset")

def test_remove_item_not_in_cart():
    client.post("/api/cart/add?items=AAB")
    response = client.post("/api/cart/remove?items=C")

    assert response.status_code == 400
    assert response.json()["detail"] == "Bad input. One or more items are not in the cart."
    client.post("/api/cart/reset")

def test_remove_empty_string_from_cart():
    response = client.post("/api/cart/remove?items=")
    print("Error Response:", response.json())
    assert response.status_code == 200
    assert response.json()["message"] == "Items removed from cart."
    assert response.json()["cart"] == {}

def test_calculate_total_price():
    client.post("/api/cart/add?items=AABB")

    response = client.get("/api/cart/total-price")
    assert response.status_code == 200
    total_price = response.json()["total_price"]
    assert total_price == 145

def test_calculate_total_price_empty_cart():
    client.post("/api/cart/reset")

    response = client.get("/api/cart/total-price")
    assert response.status_code == 200
    assert response.json()["total_price"] == 0