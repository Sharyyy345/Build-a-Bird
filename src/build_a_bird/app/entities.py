from abc import ABC, abstractmethod
from marshmallow import Schema, fields, validate, ValidationError

class Entity(ABC):
    '''
    Represents a domain-related object
    '''

    @abstractmethod
    def from_json(self, json:dict) -> tuple[bool,Exception|None]:
        '''
        Populates object's fields from JSON data

        Returns tuple of form `(success,error)`
        '''
        pass

    @abstractmethod
    def to_prompt(self, *args, **kwargs) -> str:
        '''
        Converts object to a text prompt for downstream processing
        '''
        pass

class BirdOrder(Entity):
    '''
    Represents an order for a bird through the app
    '''

    SEXES = {
        'male': 25.0,
        'female': 25.0,
    }

    SPECIES = {
        'parakeet': 100.0,
        'conure': 1000.0,
        'macaw': 3500.0,
        'cockatoo': 4000.0,
    }

    SIZES = {
        'small': 50.0,
        'medium': 75.0,
        'large': 100.0,
    }

    COLORS = {
        'red': 10.0,
        'blue': 10.0,
        'green': 10.0,
    }

    def __init__(
            self, 
            user_name:str='Guest', 
            user_email:str='',
            sex:str='male',
            species:str='conure', 
            size:str='small', 
            primary_feather_color:str='red', 
            secondary_feather_color:str='red',
            ):
        # user info
        self.user_name = user_name
        self.user_email = user_email

        # bird info
        self.sex = sex
        self.species = species.lower()
        self.size = size.lower()
        self.primary_feather_color = primary_feather_color.lower()
        self.secondary_feather_color = secondary_feather_color.lower()

    @property
    def user_name(self):
        return self._user_name
    
    @user_name.setter
    def user_name(self, name:str):
        self._user_name = name

    @property
    def user_email(self):
        return self._user_email
    
    @user_email.setter
    def user_email(self, email_addr:str):
        self._user_email = email_addr

    @property
    def sex(self):
        return self._sex
    
    @sex.setter
    def sex(self, sex:str):
        if sex not in self.SEXES:
            raise ValueError(f'Sex must be one of {self.SEXES}')
        self._sex = sex

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

    def from_json(self, json):
        try:
            data = BirdOrderSchema(unknown='exclude').load(json)
            for attr, val in data.items():
                setattr(self, attr, val)
            return (True,None)
        except ValidationError as ve:
            return (False,ve)

    def to_prompt(self, *args, **kwargs):
        return f'A highly detailed realistic {self.size} {self.sex} {self.species} with {self.primary_feather_color} and {self.secondary_feather_color} feathers in a white room with studio lighting'
    
    def __str__(self):
        res = f'Order Details:\n'

        cost = self.SEXES[self.sex]
        res += f'Sex: {self.sex} (+${self.SEXES[self.sex]:,.2f})\n'

        cost += self.SPECIES[self.species]
        res += f'Species: {self.species} (+${self.SPECIES[self.species]:,.2f})\n'

        cost += self.SIZES[self.size]
        res += f'Size: {self.size} (+${self.SIZES[self.size]:,.2f})\n'

        cost += self.COLORS[self.primary_feather_color]
        res += f'Primary Feather Color: {self.primary_feather_color} (+{self.COLORS[self.primary_feather_color]:,.2f})\n'

        cost += 0.0 if self.secondary_feather_color == self.primary_feather_color else self.COLORS[self.secondary_feather_color]
        res += f'Secondary Feather Color: {self.secondary_feather_color} (+{0.00 if self.secondary_feather_color == self.primary_feather_color else self.COLORS[self.secondary_feather_color]:,.2f})\n'
    
        res += f'Total: ${cost:,.2f}'
        
        return res
    
class BirdOrderSchema(Schema):
    user_name = fields.Str(required=False, load_default='Guest', dump_default='Guest')
    user_email = fields.Str(required=True)

    sex = fields.Str(validate=validate.OneOf(BirdOrder.SEXES), required=True)
    species = fields.Str(validate=validate.OneOf(BirdOrder.SPECIES), required=True)
    size = fields.Str(validate=validate.OneOf(BirdOrder.SIZES), required=True)
    primary_feather_color = fields.Str(validate=validate.OneOf(BirdOrder.COLORS), required=True)
    secondary_feather_color = fields.Str(validate=validate.OneOf(BirdOrder.COLORS), required=True)
    