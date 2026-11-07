from main import generate_explanation
from unittest.mock import patch, Mock 
import pytest 



@patch('main.client.models.generate_content')
def test_generate_explanation(mock_gemini): 
    mock_response = Mock() 
    mock_response.text = 'Amex Gold is the best points card.'
    mock_gemini.return_value = mock_response

    amount = 40 
    category = 'dining'
    result = { 
        'recommended_points_card': ['AmexGold'],
        'recommended_cashback_card': ['RobinhoodGold','CitiCostco'],
        'points_earned': 160,  
        'cashback_earned': 1.20,
        'other_cashback_cards': [
             {'card': 'BlueCashEveryday', 'cashback': 0.40},
             {'card': 'CitiCostco', 'cashback': 1.20},
             {'card': 'AmazonPrimeVisa', 'cashback': 0.80},
             {'card': 'RobinhoodGold', 'cashback': 1.20}
        ],
        'other_points_cards': [
             {'card': 'ChaseSapphirePreferred', 'points': 120},
             {'card': 'AmexGold', 'points': 160},
             {'card': 'AmexBlueBusinessPlus', 'points': 80}
        ]
    }
    actual_result = generate_explanation(result, amount, category)
    
    assert actual_result == 'Amex Gold is the best points card.'
    assert mock_gemini.call_count == 1
    actual_prompt = mock_gemini.call_args.kwargs['contents']
    mock_gemini.assert_called_once_with(
            model = 'gemini-3.5-flash', 
            contents = actual_prompt,
        )
    assert 'dining' in actual_prompt
    assert '$40' in actual_prompt
    assert 'AmexGold' in actual_prompt
    assert 'ChaseSapphirePreferred' in actual_prompt
    assert 'RobinhoodGold' in actual_prompt        
        

@patch('main.client.models.generate_content')
def test_generate_explanation_empty_response(mock_gemini): 
    mock_response = Mock() 
    mock_response.text = ''
    mock_gemini.return_value = mock_response


    amount = 40 
    category = 'dining'
    result = { 
        'recommended_points_card': ['AmexGold'],
        'recommended_cashback_card': ['RobinhoodGold','CitiCostco'],
        'points_earned': 160,  
        'cashback_earned': 1.20,
        'other_cashback_cards': [
             {'card': 'BlueCashEveryday', 'cashback': 0.40},
             {'card': 'CitiCostco', 'cashback': 1.20},
             {'card': 'AmazonPrimeVisa', 'cashback': 0.80},
             {'card': 'RobinhoodGold', 'cashback': 1.20}
        ],
        'other_points_cards': [
             {'card': 'ChaseSapphirePreferred', 'points': 120},
             {'card': 'AmexGold', 'points': 160},
             {'card': 'AmexBlueBusinessPlus', 'points': 80}
        ]
    }
    actual_result = generate_explanation(result, amount, category)    
    assert actual_result is None



@patch('main.client.models.generate_content')
def test_generate_explanation_error(mock_gemini): 
    mock_gemini.side_effect = Exception("Gemini API failed")

    

    amount = 40 
    category = 'dining'
    result = { 
        'recommended_points_card': ['AmexGold'],
        'recommended_cashback_card': ['RobinhoodGold','CitiCostco'],
        'points_earned': 160,  
        'cashback_earned': 1.20,
        'other_cashback_cards': [
             {'card': 'BlueCashEveryday', 'cashback': 0.40},
             {'card': 'CitiCostco', 'cashback': 1.20},
             {'card': 'AmazonPrimeVisa', 'cashback': 0.80},
             {'card': 'RobinhoodGold', 'cashback': 1.20}
        ],
        'other_points_cards': [
             {'card': 'ChaseSapphirePreferred', 'points': 120},
             {'card': 'AmexGold', 'points': 160},
             {'card': 'AmexBlueBusinessPlus', 'points': 80}
        ]
    }
    with pytest.raises(Exception): 
        generate_explanation(result, amount, category)   
    assert mock_gemini.call_count == 3  

