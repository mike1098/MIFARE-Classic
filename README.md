# MIFARE-Classic
A python class to support MIFARE Classic cards

MIFARE Classic 1k has 16 sectors each 4 blocks. One block is 16bytes
Sector Trailer:
[i -1 for i in range(4, 48, 4)]
Data Blocks, 3 Blocks of 16bytes each
Sector 0 contains only 2 Blocks, first block is RO containing manufactoring data
[i for i in range(0, 48, 1) if i not in keys]

key=3
[i for i in range(key-3, key, 1) if i not in keys]

Possible Dict:
{'1':{'a':"FFFFFFFFF",'b':'FFFFFFFFF','access':'bits'},}

{x: {'a': 'keyA', 'b': 'keyB', 'access': 'bits'} for x in keys}
