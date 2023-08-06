# __init__.py
# Copyright (C) 2019 (gnyontu39@gmail.com) and contributors
#

import inspect
import os
import sys
from pklmng import pkdump
from pklmng import pkload
__version__ = '0.0.3'

real_path = os.path.dirname(os.path.abspath(__file__)).replace("\\","/")
sys.path.append(real_path)


__all__ = [name for name, obj in locals().items()
           if not (name.startswith('_') or inspect.ismodule(obj))]

print("__all__"  ,locals().items())