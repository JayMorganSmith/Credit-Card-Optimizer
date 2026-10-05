from fastapi import FastAPI 

app = FastAPI() 

from pydantic import BaseModel

class RecommendationRequest(BaseModel): 
    merchant: str 
    amount: float 
    category: str

@app.get("/")
def home(): 
    return {"message": " Hello from my first FastAPI app!"} 

@app.get("/about") 
def about(): 
    return {"message": " About endpoint placeholder"} 

@app.get("/cards") 
def cards(): 
    return {"message": " Cards endpoint placeholder"} 

@app.get("/rewards") 
def rewards(): 
    return {"message": " Rewards endpount placeholder"} 

@app.post("/recommend") 
def recommend(request: RecommendationRequest): 
    return {
        "merchant": request.merchant, 
        "amount": request.amount ,
        "category": request.category

        } 

@app.get("/transactions") 
def transactions(): 
    return {"message": " Transactions endpount placeholder"} 

@app.get("/cards/{card_name}")
def get_card(card_name: str): 
    return {"card": card_name}
