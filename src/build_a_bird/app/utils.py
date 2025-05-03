import smtplib
import torch
from PIL.Image import Image
from email.message import EmailMessage
from diffusers import AutoPipelineForText2Image
from typing import Any
from build_a_bird.app import entities

class ApiResponse():
    '''
    Represents a response from the Flask app's API endpoints
    '''

    def __init__(self, success:bool=True, data:Any='', errors:list[Exception|str]=[], status_code:int=200):
        self.success = success
        self.data = data
        self.errors = errors
        self.status_code = status_code

    def to_json(self):
        return {'success': self.success, 'data': self.data, 'errors': [str(e) for e in self.errors]}

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
    Mechanism for converting an `Entity` into a text prompt
    suitable for processing by a text-to-image AI model
    as provided by `diffusers`
    '''

    def __init__(self, diffusers_model_id:str, img_size:int=128, torch_dtype:torch.dtype=torch.float16, use_gpu=True, seed:int|None=None):
        self.diffusers_model_id = diffusers_model_id
        self.img_size = img_size
        self.torch_dtype = torch_dtype
        self.device = 'cuda' if use_gpu else 'cpu'
        self.seed = seed
        self.pipeline, self.rand = self._build_pipeline()

    def _build_pipeline(self):
        rand = None
        if self.seed is not None:
            rand = torch.manual_seed(self.seed)

        pipeline = AutoPipelineForText2Image.from_pretrained(self.diffusers_model_id, torch_dtype=self.torch_dtype)
        pipeline.to(self.device)

        return pipeline, rand

    def gen_img(self, input:entities.Entity, **inference_config) -> Image:
        '''
        Generate an image based on `input` text prompt
        '''

        inference_config['num_images_per_prompt'] = 1 # only ever want to generate 1 image
        inference_config['generator'] = self.rand # use our own random generator

        imgs = self.pipeline(prompt=input.to_prompt(), **inference_config).images

        return imgs[0].resize((self.img_size,self.img_size))
