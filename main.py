from fastapi import FastAPI 

app = FastAPI()  

from pydantic import BaseModel

class RecommendationRequest(BaseModel): 
    merchant: str 
    amount: float 
    category: str
    booking_method: str = ''

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

def calculate_points(amount,rate): 
    points = amount * rate 
    return points 

reward_types = {
    'ChaseSapphirePreferred': 'points',
    'AmexGold': 'points',
    'BlueCashEveryday': 'cashback',
    'CitiCostco': 'cashback',
    'AmexBlueBusinessPlus': 'points',
    'AmazonPrimeVisa': 'cashback',
    'RobinhoodGold': 'cashback'
}

sample_cards = {

    'ChaseSapphirePreferred': {
        'flights_direct': 2,
        'flights_through_portal': 5,
        'hotels_direct': 2,
        'hotels_through_portal': 5,
        'dining': 3,
        'gas': 3,
        'groceries': 3,
        'streaming': 3,
        'other': 1
    },

    'AmexGold': {
        'dining': 4,
        'groceries': 4,
        'flights_direct': 3,
        'flights_through_portal': 3,
        'hotels_through_portal': 5,
        'car_rentals_through_portal': 2,
        'other': 1
    },

    'BlueCashEveryday': {
        'groceries': 3,
        'gas': 3,
        'online_retail': 3,
        'other': 1
    },

    'CitiCostco': {
        'gas': 4,
        'gas_costco': 5,
        'ev_charging': 4,
        'dining': 3,
        'flights_direct': 3,
        'hotels_direct': 3,
        'other': 1
    },

    'AmexBlueBusinessPlus': {
        'other': 2
    },

    'AmazonPrimeVisa': {
        'amazon': 5,
        'whole_foods': 5,
        'flights_through_portal': 5,
        'hotels_through_portal': 5,
        'gas': 2,
        'dining': 2,
        'transit': 2,
        'other': 1
    },

    'RobinhoodGold': {
        'other': 3
    }
}

def recommend_card(amount, category):
    best_points_card = []
    best_points = 0 
    best_cashback_card = []
    best_cashback = 0

    for card_name, rewards in sample_cards.items():
        rate = rewards.get(category, rewards.get('other', 0))
        reward_type = reward_types[card_name]

        if reward_type == 'points':
            points = calculate_points(amount, rate)

            if points > best_points:
                best_points = points
                best_points_card = [card_name]
            elif points == best_points and points > 0: 
                best_points_card.append(card_name)
        
                
              

        elif reward_type == 'cashback':
            cashback = amount * (rate / 100)

            if cashback > best_cashback:
                best_cashback = cashback
                best_cashback_card = [card_name]
            elif cashback == best_cashback and cashback > 0: 
                best_cashback_card.append(card_name)
            


    if best_points_card == []:
        best_points_card = ['No suitable points card found']

    if best_cashback_card == []:
        best_cashback_card = ['No suitable cashback card found']

    return {
        'recommended_cashback_card': best_cashback_card,
        'cashback_earned': best_cashback,
        'recommended_points_card': best_points_card,
        'points_earned': best_points
    }

@app.post("/recommend") 
def recommend(request: RecommendationRequest): 

    category = request.category.lower()
    booking_method = request.booking_method.lower()

    if booking_method: 
         reward_category = category + '_' + booking_method 
    else: 
        reward_category = category
    

    result = recommend_card(
        request.amount, 
        reward_category
    )

    
    return {
        "merchant": request.merchant, 
        "amount": request.amount ,
        "category": request.category, 
        'recommended_cashback_card': result['recommended_cashback_card'],
        'cashback_earned': result['cashback_earned'],
        'recommended_points_card': result['recommended_points_card'],
        'points_earned': result['points_earned']
    

        } 

@app.get("/transactions") 
def transactions(): 
    return {"message": " Transactions endpount placeholder"} 

@app.get("/cards/{card_name}")
def get_card(card_name: str): 
    return {"card": card_name}
