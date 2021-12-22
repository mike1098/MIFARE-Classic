"""
A libary to support MIFARE Classik RFIID cards
"""

class Classic1k:
    """
    A class to support MIFARE Classic 1k RFIID cards
    """
    def __init__(self):
        self.sector = {}
        self.block_length = 16
        self._sector_trailer_blocks = tuple([i -1 for i in range(4, 65, 4)])
        self._data_blocks = tuple([i for i in range(0, 64, 1) if i not in self._sector_trailer_blocks])
        self._sector_trailers = {sector: {'keya': [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF], 'keyb': [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF], 'access': [0xFF, 0x07, 0x80]} for sector in self._sector_trailer_blocks }
        self.DEFAULT_BLOCK_DATA= (0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00) 

    def get_key_a(self, block: int): 
        #TOTO write the function in a way that it returns the key for any given block
        """
        Returns the Key A from a sector trailer
        """
        #assert (sector is not in self._sector_trailer_blocks), "given sector is not a sector trailer. see _sector_trailer_blocks"
        return self._sector_trailers[block]['keya']
    
    def get_key_b(self, block: int): 
        #TOTO write the function in a way that it returns the key for any given block
        """
        Returns the Key B from a sector trailer
        """
        #assert (sector is not in self._sector_trailer_blocks), "given sector is not a sector trailer. see _sector_trailer_blocks"
        return self._sector_trailers[self.get_sector_trailer(block)]['keyb']

    def set_key_a(self, block: int, keya):
        """
        Set the Key A of a sector trailer
        """
        self._sector_trailers[block]['keya'] = keya
        return True

    def set_key_b(self, block, keyb):
        """
        Set the Key B of a sector trailer
        """
        self._sector_trailers[block]['keya'] = keyb
        return True
    
    def get_sector_trailer(self,block: int):
        """
        Returns the block number of the sector trailor of a given sector.
        If the block is already a sector trailor we just return it.
        """
        if block in self._sector_trailer_blocks:
            return block
        for trailer in self._sector_trailer_blocks:
            if trailer > block:
                return trailer
    
    def int2block(self,value: int) -> list:
        """converts value to a list of hex values with length 16
        and returns that list. None used elements are padded with 0x00
        if value is greater than 32 bytes it returns none

        value = int
        returns a list or none
        """
        block_data=[]
        #convert the integer to hex
        hex_value=f'{value:0>32x}'
        if len(hex_value) > 32:
            return None
        i=0
        while i< len(hex_value):
            #convert the data to a real integer with base 16 and add it to the list
            block_data.append(int(f'0x{hex_value[i:i+2]}',16))
            i+=2
        return block_data



