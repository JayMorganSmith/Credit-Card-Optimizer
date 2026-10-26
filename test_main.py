from main import calculate_points
from main import recommend_card
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_calculate_points(): 
    actual_result = calculate_points(30,4)
    expected_result = 120 
    assert actual_result == expected_result

def test_calculate_points2(): 
    actual_result = calculate_points(50,3)
    expected_result = 150 
    assert actual_result == expected_result


def test_recommend_card(): 
    result = recommend_card(40,'dining')

    actual_rewards_result = result['points_earned']
    actual_card_result = result['recommended_points_card']
    expected_reward_result = 160
    expected_card_result = 'AmexGold'
    assert actual_rewards_result == expected_reward_result
    assert expected_card_result in actual_card_result


    actual_cashback_result = result['cashback_earned']
    actual_card_result = result['recommended_cashback_card']
    expected_cashback_result = 1.2
    expected_card_result = sorted(['RobinhoodGold','CitiCostco'])
    assert actual_cashback_result == expected_cashback_result
    assert actual_card_result == expected_card_result 

def test_recommend_card_zero_amount():
    result = recommend_card(0, 'dining') 

    assert result['points_earned'] == 0 
    assert result['cashback_earned'] == 0 
    assert result['recommended_points_card'] == ['No suitable points card found']
    assert result['recommended_cashback_card'] == ['No suitable cashback card found']


def test_recommend_endpoint():
    response = client.post("/recommend", json={
        "merchant": "Restaurant",
        "amount": 40,
        "category": "dining",
        "booking_method": ""
    })

    assert response.status_code == 200
    assert response.json()["recommended_points_card"] == ["AmexGold"]
    assert sorted(response.json()["recommended_cashback_card"]) == sorted(["RobinhoodGold","CitiCostco"])
    assert response.json()["points_earned"] == 160
    assert response.json()["cashback_earned"] == 1.2

def test_recommend_endpoint_dining():
    response = client.post("/recommend", json={
            "merchant": "Airline",
            "amount": 400,
            "category": "flights",
            "booking_method": "direct"
        })
    
    assert response.status_code == 200
    assert response.json()["recommended_points_card"] == ["AmexGold"]
    assert sorted(response.json()["recommended_cashback_card"]) == sorted(["RobinhoodGold",'CitiCostco'])
    assert response.json()["points_earned"] == 1200
    assert response.json()["cashback_earned"] == 12

def test_missing_category():
    response = client.post("/recommend", json={
        "merchant": "Restaurant",
        "amount": 40,
        "booking_method": ""
    })

    assert response.status_code == 422 

def test_invalid_amount():
    response = client.post("/recommend", json={
        "merchant": "Restaurant",
        "amount": 'forty',
        "category":'dining',
        "booking_method": ""
    })

    assert response.status_code == 422 
   