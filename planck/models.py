import os
from planck.constants import constants

from pydantic import BaseModel
from pydantic import create_model
from pydantic import Field


models = {"a": 1}

dirpath = os.path.dirname(__file__)
filepath = os.path.join(dirpath, "_models.py")

with open(filepath, "w") as fp:
    fp.write("from pydantic import BaseModel")


for k in constants.keys():
    if k not in ["m", "m/s"]:
        continue

    constant = constants[k]

    # print(constant)

    kwargs = {}
    for kk, v in constant.items():
        kwargs[kk] = (float, Field(default=v))

    class_name = constant.name.title().replace(" ", "")
    M = create_model(
        class_name,
        symbol=(str, constant.symbol),
        name=(str, constant.name),
        quantity=(str, constant.quantity),
        **kwargs,
    )

    attrs = ""
    for kk, (cls, f) in kwargs.items():
        attrs += f"    {kk}: float\n"
        attrs += f"        {f.default}\n"

    doc = f'''
class {class_name}(BaseModel):
    """    
    {constant.name.title()}
    
    Attributes
    ----------
    symbol: str
        {constant.symbol}
    name: str
        {constant.name}
    quantity: str
        {constant.quantity}    
{attrs}    
    """
    '''

    # print(doc)
    # with open(filepath, "a") as fp:
    #     fp.write(doc)

    models[constant.symbol] = M()

# print(models)
