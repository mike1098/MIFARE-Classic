"""
A libary to support MIFARE Classik RFIID cards
"""

class Classic1k:
    """
    A class to support MIFARE Classic 1k RFIID cards
    """
    def __init__(self):
        self.sector = {}
        self.sector_length = 16
        self._sector_trailer_blocks = tuple([i -1 for i in range(4, 65, 4)])
        self._data_blocks = tuple([i for i in range(0, 48, 1) if i not in self._sector_trailer_blocks])
        self._sector_trailers = {sector: {'keya': [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF], 'keyb': [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF], 'access': '000000'} for sector in self._sector_trailer_blocks }

    def get_key_a(self, block):
        """
        Returns the Key A from a sector trailer
        """
        #assert (sector is not in self._sector_trailer_blocks), "given sector is not a sector trailer. see _sector_trailer_blocks"
        return self._sector_trailers[block]['keya']

    def set_key_a(self, block, keya):
        """
        Set the Key A of a sector trailer
        """
        self._sector_trailers[block]['keya'] = keya
        return True
    
    def get_sector_trailer(self,block):
        """
        Returns the block number of the sector trailor of a given sector.
        If the block is already a sector trailor we just return it.
        """
        if block in self._sector_trailer_blocks:
            return block
        for trailer in self._sector_trailer_blocks:
            if trailer > block:
                return trailer
        



