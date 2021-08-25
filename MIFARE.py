"""
A libary to support MIFARE Classik RFIID cards
"""

class Classic1k:
    """
    A class to support MIFARE Classic 1k RFIID cards
    """
    def __init__(self):
        self.sector = {}
        self._sector_trailer_blocks = tuple([i -1 for i in range(4, 48, 4)])
        self._data_blocks = tuple([i for i in range(0, 48, 1) if i not in self._sector_trailer_blocks])
        self._sector_trailers = {sector: {'keya': 'FFFFFFFF', 'keyb': 'FFFFFFFF', 'access': '000000'} for sector in self._sector_trailer_blocks }

    def get_key_a(self, sector):
        """
        Returns the Key A from a sector
        """
        #assert (sector is not in self._sector_trailer_blocks), "given sector is not a sector trailer. see _sector_trailer_blocks"
        return self._sector_trailers[sector]['keya']

    def set_key_a(self, sector, keya):
        """
        Set the Key A of a sector
        """
        self._sector_trailers[sector]['keya'] = keya
        return True
        



