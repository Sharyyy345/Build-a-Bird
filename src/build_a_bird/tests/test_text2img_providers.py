import os
from dotenv import load_dotenv
from build_a_bird.app import utils, entities

load_dotenv()

class TestDiffusersText2ImgProvider():
    '''
    Units tests for `DiffusersText2ImgProvider` image generation provider
    '''

    def test_gen_img(self):
        order = entities.BirdOrder(
            species='conure', 
            size='small', 
            primary_feather_color='green', 
            secondary_feather_color='red',
            )
        
        img_provider = utils.DiffusersText2ImgProvider(
            os.getenv('DIFFUSERS_MODEL_ID'),
            use_gpu=True,
            seed=777,
            )
        
        img = img_provider.gen_img(order)
                