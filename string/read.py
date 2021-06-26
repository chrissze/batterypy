from typing import Any, List ,Optional, Union
import re



def formatlarge(n: Union[int,float]) -> str:
    if n >= 10000000000000000.0:  # 10^16
        nstring: List[str] = str(float(n)).split('+')
        #print('nstring: ', nstring)
        power: int = int(nstring[1])
        num_part = round(n / 10**power, 2)
        power_str: str = ' x 10^' + nstring[1]
        result: str = str(num_part) + power_str

    elif n >= 1000000000000000.0: # 10^15
        nstring: List[str] = str(float(n)).split('.')
        power: int = len(nstring[0]) - 1
        num_part = round(n / 10**power, 2)
        power_str: str = ' x 10^' + str(power)
        result: str = str(num_part) + power_str
    else:
        divider, letter = (1000000000000000.0, 'Quad') if n >= 1000000000000000.0 else \
                          (1000000000000.0, 'T') if n >= 1000000000000.0 else \
                          (1000000000.0, 'B') if n >= 1000000000.0 else \
                          (1000000.0, 'M') if n >= 1000000.0 else \
                          (1000.0, 'K') if n >= 1000.0 else (1.0, '')
        result: str = str(round(n / divider, 2)) + ' ' + letter

    return result


def is_floatable(s: Any) -> bool:
    s0: str = str(s)
    s1: str = s0.strip() # remove all leading and trailing spaces
    is_neg_str: bool = s1[:1] == '-'
    s2: str = s1[1:] if is_neg_str else s1
    s3: str = s2.replace('.', '', 1) # get rid of one dot
    return s3.isdecimal()

def readfloat(s: Any) -> Optional[float]:
    return float(s) if is_floatable(s) else None


def readf(s: Any) -> Optional[float]:
    s0: str = s[:-1] if len(s) > 0 and s[-1] == '.' else s
    x = re.sub('[,+%$¢£¥€]', '', str(s0))
    return float(x) if is_floatable(x) else None


def float0(s: Any) -> float:
    x = re.sub('[,+%$¢£¥€]', '', str(s))
    return float(x) if is_floatable(x) else 0.0


def readlarge(s: str) -> Optional[float]:
    s1: str = s.strip()
    s2: str = re.sub('[,+$£¥€]', '', s1)
    if is_floatable(s2):
        return float(s2)
    else:
        lastchar: str = s2[-1:].upper()
        s3: str = re.sub('[mbtMBT]', '', s2)
        valid: bool = is_floatable(s3)
        base_num: float = float(s3) if valid else 0.0
        result: Optional[float] = base_num * 1000000.0 if valid and lastchar == 'M' else \
                                  base_num * 1000000000.0 if valid and lastchar == 'B' else \
                                  base_num * 1000000000000.0 if valid and lastchar == 'T' else None
        return result



def is_intable(s: Any) -> bool:
    s0 = str(s)
    s1: str = s0.strip() # remove all leading and trailing spaces
    is_neg_str: bool = s1[:1] == '-'
    s2: str = s1[1:] if is_neg_str else s1
    return s2.isdecimal()

def readint(s: str) -> Optional[int]:
    return int(s) if is_intable(s) else None

def readi(s: str) -> Optional[int]:
    x = re.sub('[,+%$¢£¥€]', '', s)
    return int(x) if is_intable(x) else None


def int0(s: str) -> int:
    x = re.sub('[,+%$¢£¥€]', '', s)
    return int(x) if is_intable(x) else 0




if __name__ == '__main__':
    xxx = ''
    y = readf(xxx)
    print(y)







