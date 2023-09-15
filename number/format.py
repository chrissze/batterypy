"""

"""

from typing import Any



def round0(x) -> Any:
    return round(x) if isinstance(x, (int, float)) else x

def round1(x) -> Any:
    return round(x, 1) if isinstance(x, (int, float)) else x

def round2(x) -> Any:
    return round(x, 2) if isinstance(x, (int, float)) else x
    
def round3(x) -> Any:
    return round(x, 3) if isinstance(x, (int, float)) else x

def round4(x) -> Any:
    return round(x, 4) if isinstance(x, (int, float)) else x


