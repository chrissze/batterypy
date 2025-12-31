# STANDARD LIBS
from collections import OrderedDict

from itertools import dropwhile
from typing import Any, Tuple


def insert_odict(odict: OrderedDict, item: Tuple[Any, Any], index: int=0) -> OrderedDict:
    """
    line 1, 2, 3 CANNOT be combined

    This function will not mutate the odict argument.
    """    
    od_list = list(odict.items())     # line 1
    od_list.insert(index, item)    # line 2
    new_od = OrderedDict(od_list)      # line 3
    return new_od

