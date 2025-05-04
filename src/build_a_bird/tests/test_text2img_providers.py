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
        
        model = os.getenv('DIFFUSERS_MODEL_ID')
        img_size = int(os.getenv('IMG_SIZE', 128))
        model_dtype = utils.TORCH_DTYPES[os.getenv('MODEL_DTYPE', 'bfloat16').lower()]
        device = os.getenv('MODEL_DEVICE', 'cpu').lower()
        print(f'Generating {img_size}x{img_size} image using {model} of data type {model_dtype} on {device}')

        img_provider = utils.DiffusersText2ImgProvider(
            model,
            img_size=img_size,
            torch_dtype=model_dtype,
            device=device,
            )
        
        img = img_provider.gen_img(order)
        img.save('bird.jpg')
                