from pydantic import BaseModel
from pydantic import Field
from planck._scipy import sp_constants


class Metre(BaseModel):
    in_: float = Field(1. / sp_constants.inch, alias="in")
    ft: float = Field(1. / sp_constants.foot)
    mi: float = Field(1. / sp_constants.mile)
    NM: float = Field(1. / sp_constants.nautical_mile)
    mm: float = Field(None)
    cm: float = Field(None)
    m: float = Field(None)
    km: float = Field(None)


metre = Metre()

print(metre)