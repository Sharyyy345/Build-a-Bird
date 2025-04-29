import smtplib
import torch
from abc import ABC, abstractmethod
from email.message import EmailMessage
from diffusers import AutoPipelineForText2Image

class Promptifiable(ABC):
    '''
    Object that can be converted to a text prompt for downstream processing
    '''

    @abstractmethod
    def to_prompt(self, *args, **kwargs) -> str:
        pass

class BirdOrder(Promptifiable):
    '''
    Represents an order for a bird through the app
    '''

    # TODO: revise this all

    SPECIES = set(['conure','macaw','cockatoo','parakeet'])
    SIZES = set(['small','medium','large'])
    COLORS = set(['red','green','blue'])

    def __init__(self, species:str='conure', size:str='small', primary_feather_color:str='green', secondary_feather_color:str='red'):
        self.species = species.lower()
        self.size = size.lower()
        self.primary_feather_color = primary_feather_color.lower()
        self.secondary_feather_color = secondary_feather_color.lower()

    @property
    def species(self):
        return self._species
    
    @species.setter
    def species(self, species:str):
        if species not in self.SPECIES:
            raise ValueError(f'Species must be one of {self.SPECIES}')
        self._species = species

    @property
    def size(self):
        return self._size
    
    @size.setter
    def size(self, size:str):
        if size not in self.SIZES:
            raise ValueError(f'Size must be one of {self.SIZES}')
        self._size = size

    @property
    def primary_feather_color(self):
        return self._primary_feather_color
    
    @primary_feather_color.setter
    def primary_feather_color(self, color:str):
        if color not in self.COLORS:
            raise ValueError(f'Primary feather color must be one of {self.COLORS}')
        self._primary_feather_color = color

    @property
    def secondary_feather_color(self):
        return self._secondary_feather_color
    
    @secondary_feather_color.setter
    def secondary_feather_color(self, color:str):
        if color not in self.COLORS:
            raise ValueError(f'Secondary feather color must be one of {self.COLORS}')
        self._secondary_feather_color = color

    def to_prompt(self, *args, **kwargs):
        return f'A {self.size} {self.species} with {self.primary_feather_color} and {self.secondary_feather_color} feathers in a white room'

class GmailProvider():
    '''
    Mechanism for programmatically sending emails via Gmail

    See https://stackoverflow.com/questions/10147455/how-to-send-an-email-with-gmail-as-provider-using-python
    '''

    HOST = 'smtp.gmail.com'
    PORT = 465

    def __init__(self, from_addr:str, app_password:str):
        self.from_addr = from_addr
        self.app_password = app_password

    def _connect(self):
        '''
        Establishes a connection to Gmail's SMTP server (with SSL encryption)
        '''

        conn = smtplib.SMTP_SSL(host=self.HOST, port=self.PORT)

        conn.ehlo()

        conn.login(self.from_addr, self.app_password)

        return conn
    
    def send(self, email:EmailMessage):
        '''
        Send `email` via Gmail

        Returns a dictionary, with one entry for each recipient that was refused. 
        Each entry contains a tuple of the SMTP error code and the accompanying error message sent by the server.
        '''

        smtp_conn = self._connect()
        send_errs = smtp_conn.sendmail(self.from_addr, email['To'], email.as_string())
        smtp_conn.quit()
        return send_errs

class DiffusersText2ImgProvider():
    '''
    Mechanism for converting a `Promptifiable` object into a text prompt
    suitable for processing by a text-to-image AI model
    as provided by `diffusers`
    '''

    def __init__(self, diffusers_model_id:str, torch_dtype:torch.dtype=torch.float16, use_gpu=True, seed:int=123):
        self.diffusers_model_id = diffusers_model_id
        self.torch_dtype = torch_dtype
        self.device = 'cuda' if use_gpu else 'cpu'
        self.seed = seed
        self.pipeline, self.rand = self._build_pipeline()

    def _build_pipeline(self):
        rand = torch.manual_seed(self.seed)

        pipeline = AutoPipelineForText2Image.from_pretrained(self.diffusers_model_id, torch_dtype=self.torch_dtype)
        pipeline.to(self.device)

        return pipeline, rand

    def gen_img(self, input:Promptifiable, **inference_config):
        '''
        Generate an image based on `input` text prompt
        '''

        inference_config['num_images_per_prompt'] = 1 # only ever want to generate 1 image

        imgs = self.pipeline(prompt=input.to_prompt(), **inference_config).images

        return imgs[0]
