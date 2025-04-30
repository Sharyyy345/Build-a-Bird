from dotenv import load_dotenv
from build_a_bird.app import entities

load_dotenv() # load configuration environment variables

class TestBirdOrderEntity():
    '''
    Unit tests for `BirdOrder` entity
    '''

    def test_from_valid_json(self):
        order_json = {
            'user_email': 'foo@bar.com',
            'species': 'conure', 
            'size': 'small', 
            'primary_feather_color': 'red', 
            'secondary_feather_color': 'green', 
            'foo': 'bar', # non-existent property - shouldn't cause errors and should be ignored
            }
        
        order = entities.BirdOrder() # initialize order
        res = order.from_json(order_json) # res[0] indicates success, res[1] indicates errors encountered

        assert res[0] == True and res[1] is None
        assert order.species == order_json['species']

    def test_from_json_missing_required(self):
        order_json = {
            # missing user email address
            'species': 'conure',
            'size': 'small', 
            'primary_feather_color': 'red', 
            'secondary_feather_color': 'green', 
            }
        
        order = entities.BirdOrder()
        res = order.from_json(order_json)

        assert res[0] == False and res[1] is not None

        print(res[1])

    def test_from_json_invalid_val(self):
        order_json = {
            'user_email': 'foo@bar.com',
            'species': 'dog',
            'size': 'small', 
            'primary_feather_color': 'red', 
            'secondary_feather_color': 'green', 
            }
        
        order = entities.BirdOrder()
        res = order.from_json(order_json)

        assert res[0] == False and res[1] is not None

        print(res[1])
