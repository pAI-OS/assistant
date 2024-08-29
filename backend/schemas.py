from datetime import datetime
from pydantic import BaseModel, field_serializer
from typing import Optional


# We have *Create schemas because API clients ideally don't set the id field, it's set by the server
# Alternatively we could have made the id optional but then we would have to check if it's set by the client

# Config schemas
class ConfigBaseSchema(BaseModel):
    value: Optional[str] = None

class ConfigSchema(ConfigBaseSchema):
    key: str

# Resource schemas
class ChannelBaseSchema(BaseModel):
    name: str
    uri: str

class ChannelCreateSchema(ChannelBaseSchema):
    pass

class ChannelSchema(ChannelBaseSchema):
    id: str

# Persona schemas
class PersonaBaseSchema(BaseModel):
    name: str
    description: Optional[str] = None
    voice_id: str = None
    face_id: str = None

class PersonaCreateSchema(PersonaBaseSchema):
    pass

class PersonaSchema(PersonaBaseSchema):
    id: str

# User schemas
class UserBaseSchema(BaseModel):
    name: str
    email: str

class UserCreateSchema(UserBaseSchema):
    pass

class UserSchema(UserBaseSchema):
    id: str

# Asset schemas
class AssetBaseSchema(BaseModel):
    title: str
    user_id: Optional[str] = None
    creator: Optional[str] = None
    subject: Optional[str] = None
    description: Optional[str] = None

class AssetCreateSchema(AssetBaseSchema):
    pass

class AssetSchema(AssetBaseSchema):
    id: str

# Share schemas

class ShareBaseSchema(BaseModel):
    resource_id: str
    user_id: Optional[str] = None
    expiration_dt: Optional[datetime] = None
    is_revoked: Optional[bool] = False

    @field_serializer('expiration_dt')
    def serialize_dt(self, dt: datetime, _info):
        return dt.strftime('%Y-%m-%dT%H:%M:%SZ')


class ShareCreateSchema(ShareBaseSchema):
    pass

class ShareSchema(ShareBaseSchema):
    id: str
