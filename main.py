# from fastapi import FastAPI, Query, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import JSONResponse
# from typing import Dict

# app = FastAPI()

# # Enable CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# def is_prime(n: int) -> bool:
#     if n < 2:
#         return False
#     for i in range(2, int(n ** 0.5) + 1):
#         if n % i == 0:
#             return False
#     return True

# def is_perfect(n: int) -> bool:
#     return sum([i for i in range(1, n) if n % i == 0]) == n

# def is_armstrong(n: int) -> bool:
#     return n == sum(int(digit) ** len(str(n)) for digit in str(n))

# @app.get("/api/classify-number")
# async def classify_number(number: str = Query(..., description="Number to classify")) -> Dict:
#     # Check if the number is a valid integer
#     if not number.lstrip('-').isdigit():
#         return JSONResponse(status_code=400, content={"number": number, "error": True})

#     number = int(number)
#     properties = []
    
#     if is_prime(number):
#         properties.append("prime")
#     if is_perfect(number):
#         properties.append("perfect")
#     if is_armstrong(number):
#         properties.append("armstrong")

#     properties.append("even" if number % 2 == 0 else "odd")

#     response = {
#         "number": number,
#         "is_prime": is_prime(number),
#         "is_perfect": is_perfect(number),
#         "properties": properties,
#         "digit_sum": sum(int(d) for d in str(abs(number))),
#         "fun_fact": f"{number} is an Armstrong number because {' + '.join(f'{d}^{len(str(number))}' for d in str(number))} = {number}" if is_armstrong(number) else None
#     }

#     return response

import os
import requests
import uvicorn
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def is_armstrong(n: int) -> bool:
    """Check if a number is an Armstrong number."""
    digits = [int(d) for d in str(n)]
    power = len(digits)
    return sum(d**power for d in digits) == n

def is_prime(n: int) -> bool:
    """Check if a number is prime."""
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n: int) -> bool:
    """Check if a number is a perfect number."""
    return sum(i for i in range(1, n) if n % i == 0) == n

def get_fun_fact(n: int) -> str:
    """Fetch a fun fact about the number from NumbersAPI."""
    response = requests.get(f"http://numbersapi.com/{n}/math?json")
    if response.status_code == 200:
        return response.json().get("text", "No fun fact available.")
    return "Could not retrieve a fun fact."

@app.get("/api/classify-number")
async def classify_number(number: int = Query(..., description="The number to classify")):
    """Classify the number and return its properties."""
    try:
        armstrong = is_armstrong(number)
        properties = []
        
        if armstrong:
            properties.append("armstrong")
        
        properties.append("odd" if number % 2 != 0 else "even")

        return {
            "number": number,
            "is_prime": is_prime(number),
            "is_perfect": is_perfect(number),
            "properties": properties,
            "digit_sum": sum(int(d) for d in str(number)),
            "fun_fact": get_fun_fact(number),
        }
    except Exception as e:
        return {"error": True, "message": str(e)}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))  # Use Render's PORT
    uvicorn.run(app, host="0.0.0.0", port=port)
