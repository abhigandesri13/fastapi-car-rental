# ----------- IMPORTS & APP INITIALIZATION ---------------
from fastapi import FastAPI, Query, Response, HTTPException
from pydantic import BaseModel, Field
import math

app = FastAPI()


# ------------------- Question 1: HOME ROUTE -------------------
@app.get("/")
def home():
    return {"message": "Welcome to SpeedRide Car Rentals"}


# ----------------------- CARS DATA (Q2) -----------------------
cars = [
    {"id": 1, "model": "i20", "brand": "Hyundai", "type": "Hatchback", "price_per_day": 2000, "fuel_type": "Petrol", "is_available": True},
    {"id": 2, "model": "City", "brand": "Honda", "type": "Sedan", "price_per_day": 3000, "fuel_type": "Petrol", "is_available": True},
    {"id": 3, "model": "Fortuner", "brand": "Toyota", "type": "SUV", "price_per_day": 5000, "fuel_type": "Diesel", "is_available": False},
    {"id": 4, "model": "Swift", "brand": "Maruti", "type": "Hatchback", "price_per_day": 1800, "fuel_type": "Petrol", "is_available": True},
    {"id": 5, "model": "Thar", "brand": "Mahindra", "type": "SUV", "price_per_day": 4500, "fuel_type": "Diesel", "is_available": True},
    {"id": 6, "model": "Nexon", "brand": "Tata", "type": "SUV", "price_per_day": 2500, "fuel_type": "Electric", "is_available": True}
]



# -------------- RENTALS DATA (Q4) ----------------
rentals = []
rental_counter = 1


# ------------- Question 2: GET ALL CARS ----------------
@app.get("/cars")
def get_cars():
    available_count = len([c for c in cars if c["is_available"]])

    return {
        "total": len(cars),
        "available_count": available_count,
        "cars": cars
    }


# ------------- Question 5: CARS SUMMARY ----------------
@app.get("/cars/summary")
def cars_summary():
    total = len(cars)
    available = len([c for c in cars if c["is_available"]])

    type_count = {}
    fuel_count = {}

    for car in cars:
        type_count[car["type"]] = type_count.get(car["type"], 0) + 1
        fuel_count[car["fuel_type"]] = fuel_count.get(car["fuel_type"], 0) + 1

    cheapest = min(cars, key=lambda x: x["price_per_day"])
    expensive = max(cars, key=lambda x: x["price_per_day"])

    return {
        "total_cars": total,
        "available_count": available,
        "type_breakdown": type_count,
        "fuel_type_breakdown": fuel_count,
        "cheapest_car": cheapest,
        "most_expensive_car": expensive
    }

# -------------- FILTER CARS (Q10) ----------------
def filter_cars_logic(type=None, brand=None, fuel_type=None, max_price=None, is_available=None):
    result = cars

    if type is not None:
        result = [c for c in result if c["type"].lower() == type.lower()]

    if brand is not None:
        result = [c for c in result if c["brand"].lower() == brand.lower()]

    if fuel_type is not None:
        result = [c for c in result if c["fuel_type"].lower() == fuel_type.lower()]

    if max_price is not None:
        result = [c for c in result if c["price_per_day"] <= max_price]

    if is_available is not None:
        result = [c for c in result if c["is_available"] == is_available]

    return result

@app.get("/cars/filter")
def filter_cars(
    type: str = None,
    brand: str = None,
    fuel_type: str = None,
    max_price: int = None,
    is_available: bool = None
):
    filtered = filter_cars_logic(type, brand, fuel_type, max_price, is_available)

    return {
        "total": len(filtered),
        "cars": filtered
    }

# ------------------  Question 16: SEARCH -----------------------
@app.get("/cars/search")
def search(keyword: str):
    res = [
        c for c in cars
        if keyword.lower() in c["model"].lower()
        or keyword.lower() in c["brand"].lower()
        or keyword.lower() in c["type"].lower()
    ]
    return {"total_found": len(res), "cars": res}


#--------------------- Question 17: SORT ------------------------
@app.get("/cars/sort")
def sort(sort_by: str = "price_per_day", order: str = "asc"):
    allowed = ["price_per_day", "brand", "type"]
    if sort_by not in allowed:
        return {"error": "Invalid sort_by"}

    reverse = True if order == "desc" else False
    return {"cars": sorted(cars, key=lambda x: x[sort_by], reverse=reverse)}


# ------------------- Question 18: PAGINATION --------------------
@app.get("/cars/page")
def page(page: int = 1, limit: int = 3):
    start = (page - 1) * limit
    data = cars[start:start + limit]
    return {
        "page": page,
        "total_pages": math.ceil(len(cars) / limit),
        "cars": data
    }


# ----------------- Question 19: RENTAL SEARCH/SORT/PAGE --------------------
@app.get("/rentals/search")
def r_search(customer_name: str):
    return {"rentals": [r for r in rentals if customer_name.lower() in r["customer_name"].lower()]}


@app.get("/rentals/sort")
def r_sort(sort_by: str = "total_cost"):
    return {"rentals": sorted(rentals, key=lambda x: x[sort_by])}


@app.get("/rentals/page")
def r_page(page: int = 1, limit: int = 3):
    start = (page - 1) * limit
    return {"rentals": rentals[start:start + limit]}


#  ----------------------- Question 20: BROWSE ----------------------
@app.get("/cars/browse")
def browse(
    keyword: str = None,
    type: str = None,
    fuel_type: str = None,
    max_price: int = None,
    is_available: bool = None,
    sort_by: str = "price_per_day",
    order: str = "asc",
    page: int = 1,
    limit: int = 3
):
    result = cars

    if keyword:
        result = [c for c in result if keyword.lower() in c["model"].lower()]

    if type:
        result = [c for c in result if c["type"].lower() == type.lower()]

    if fuel_type:
        result = [c for c in result if c["fuel_type"].lower() == fuel_type.lower()]

    if max_price:
        result = [c for c in result if c["price_per_day"] <= max_price]

    if is_available is not None:
        result = [c for c in result if c["is_available"] == is_available]

    reverse = True if order == "desc" else False
    result = sorted(result, key=lambda x: x[sort_by], reverse=reverse)

    start = (page - 1) * limit
    paginated = result[start:start + limit]

    return {
        "total": len(result),
        "page": page,
        "total_pages": math.ceil(len(result) / limit),
        "cars": paginated
    }



# -------------- UNAVAILABLE CARS (15) ----------------
@app.get("/cars/unavailable")
def unavailable_cars():
    result = [c for c in cars if not c["is_available"]]
    return {"total": len(result), "cars": result}


# -------------- Question 3: GET CAR BY ID ----------------
@app.get("/cars/{car_id}")
def get_car(car_id: int):
    for car in cars:
        if car["id"] == car_id:
            return car
    return {"error": "Car not found"}


# ------------- Question 4: GET ALL RENTALS ----------------
@app.get("/rentals")
def get_rentals():
    return {
        "rentals": rentals,
        "total": len(rentals)
    }


# ----------------  ACTIVE RENTALS (Q15) -----------------------
@app.get("/rentals/active")
def active_rentals():
    active = [r for r in rentals if r["status"] == "active"]
    return {"total": len(active), "rentals": active}


# ------------------ RENTALS BY CAR (Q15) ----------------------
@app.get("/rentals/by-car/{car_id}")
def rentals_by_car(car_id: int):
    car = next((c for c in cars if c["id"] == car_id), None)
    if not car:
        return {"error": "Car not found"}

    result = [r for r in rentals if r["car_model"] == car["model"]]
    return {"total": len(result), "rentals": result}


# ---------------  Question 14: GET RENTAL BY ID -------------------
@app.get("/rentals/{rental_id}")
def get_rental_by_id(rental_id: int):
    for r in rentals:
        if r["rental_id"] == rental_id:
            return r
    return {"error": "Rental not found"}


# -------------- PYDANTIC MODEL (Q6) ----------------
class RentalRequest(BaseModel):
    customer_name: str = Field(..., min_length=2)
    car_id: int = Field(..., gt=0)
    days: int = Field(..., gt=0, le=30)
    license_number: str = Field(..., min_length=8)
    insurance: bool = False
    driver_required: bool = False


# -------------- HELPER FUNCTION (Q7) ----------------
def find_car(car_id: int):
    for car in cars:
        if car["id"] == car_id:
            return car
    return None

def calculate_rental_cost(price_per_day, days, insurance, driver_required):
    base_cost = price_per_day * days

    discount = 0
    if days >= 15:
        discount = 0.25 * base_cost
    elif days >= 7:
        discount = 0.15 * base_cost  

    insurance_cost = 500 * days if insurance else 0
    driver_cost = 800 * days if driver_required else 0

    total = base_cost - discount + insurance_cost + driver_cost

    return {
        "base_cost": base_cost,
        "discount": discount,
        "insurance_cost": insurance_cost,
        "driver_cost": driver_cost,
        "total_cost": total
    }


# -------------- Question 8 + 9: CREATE RENTAL ----------------
@app.post("/rentals")
def create_rental(request: RentalRequest):
    global rental_counter

    car = find_car(request.car_id)

    if not car:
        return {"error": "Car not found"}

    if not car["is_available"]:
        return {"error": "Car not available"}

    # mark unavailable
    car["is_available"] = False

    cost = calculate_rental_cost(
        car["price_per_day"],
        request.days,
        request.insurance,
        request.driver_required
    )

    rental = {
        "rental_id": rental_counter,
        "customer_name": request.customer_name,
        "car_model": car["model"],
        "car_brand": car["brand"],
        "days": request.days,
        "insurance": request.insurance,
        "driver_required": request.driver_required,
        "base_cost": cost["base_cost"],
        "discount": cost["discount"],
        "insurance_cost": cost["insurance_cost"],
        "driver_cost": cost["driver_cost"],
        "total_cost": cost["total_cost"],
        "status": "active"
    }

    rentals.append(rental)
    rental_counter += 1

    return rental


# -------------- RETURN CAR (Q14) ----------------
@app.post("/return/{rental_id}")
def return_car(rental_id: int):
    rental = next((r for r in rentals if r["rental_id"] == rental_id), None)

    if not rental:
        return {"error": "Rental not found"}

    if rental["status"] == "returned":
        return {"message": "Already returned"}

    rental["status"] = "returned"

    for car in cars:
        if car["model"] == rental["car_model"]:
            car["is_available"] = True

    return rental


# --------------------- NEW CAR MODEL (Q11) -----------------------
class NewCar(BaseModel):
    model: str = Field(..., min_length=2)
    brand: str = Field(..., min_length=2)
    type: str = Field(..., min_length=2)
    price_per_day: int = Field(..., gt=0)
    fuel_type: str = Field(..., min_length=2)
    is_available: bool = True


# --------------------- Question 11: ADD CAR ----------------------
@app.post("/cars")
def add_car(car: NewCar, response: Response):
    for c in cars:
        if c["model"].lower() == car.model.lower() and c["brand"].lower() == car.brand.lower():
            return {"error": "Car already exists"}

    new_car = {
        "id": len(cars) + 1,
        "model": car.model,
        "brand": car.brand,
        "type": car.type,
        "price_per_day": car.price_per_day,
        "fuel_type": car.fuel_type,
        "is_available": car.is_available
    }

    cars.append(new_car)
    response.status_code = 201

    return new_car


# --------------------- Question 12: UPDATE CAR ----------------------
@app.put("/cars/{car_id}")
def update_car(car_id: int, price_per_day: int = None, is_available: bool = None):
    car = find_car(car_id)

    if not car:
        raise HTTPException(status_code=404, detail="Car not found")

    if price_per_day is not None:
        car["price_per_day"] = price_per_day

    if is_available is not None:
        car["is_available"] = is_available

    return car


# ---------------- Question 13: DELETE CAR --------------------
@app.delete("/cars/{car_id}")
def delete_car(car_id: int):
    car = find_car(car_id)

    if not car:
       raise HTTPException(status_code=404, detail="Car not found")

    for r in rentals:
        if r["car_model"] == car["model"] and r["status"] == "active":
            return {"error": "Car has active rental"}

    cars.remove(car)

    return {"message": "Car deleted successfully"}
