"""
A module to support  MIFARE Classic EV1 contactless IC
according to ISO/IEC 14443 Type A.


"""

class Classic1k():
    """
    A module to support  MIFARE Classic EV1 contactless IC
    MF1S50yyX/V1 according to ISO/IEC 14443 Type A.

    The card has 1k memory, organized in 16 sectors of 4 blocks.
    One block consists of 16 bytes. The last block of each sector
    is called "trailer", which contains two secret keys and
    programmable access conditions for each block in this sector.

    """
    def __init__(self):
        self._sector = {}
        self.block_length = 16
        self.sector_trailers_blocks =tuple(i -1 for i in range(4, 65, 4))
        self.data_blocks = tuple(i for i in range(0, 64,1 )
                                 if i not in self.sector_trailers_blocks)
        self.sector_trailers = {_sector: {'keya': [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF],
                                          'keyb': [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF],
                                          'access': [0xFF, 0x07, 0x80]}
                                          for _sector in self.sector_trailers_blocks}
        self.default_data_blocks = (0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
                                   0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00)

    def get_key_a(self, block: int):
        #TODO write the function in a way that it returns the key for any given block
        """
        Returns the Key A from a sector trailer.

        Returns a list of 16 hex codes
        """
        return self.sector_trailers[block]['keya']

    def get_key_b(self, block: int):
        #TODO write the function in a way that it returns the key for any given block
        """
        Returns the Key B from a sector trailer.

        Returns a list of 16 hex codes.
        """
        #assert (sector is not in self.sector_trailers_blocks),
        # "given sector is not a sector trailer. see sector_trailers_blocks"
        return self.sector_trailers[self.get_sector_trailer(block)]['keyb']

    def set_key_a(self, block: int, keya):
        """
        Set the Key A of a sector trailer.

        Returns true in case of success.
        """
        self.sector_trailers[block]['keya'] = keya
        return True

    def set_key_b(self, block, keyb):
        """
        Set the Key B of a sector trailer.

        Returns true in case of success.
        """
        self.sector_trailers[block]['keya'] = keyb
        return True

    def get_sector_trailer(self,block: int):
        """
        Returns the block number of the sector trailor of a given block.

        If the block is already a sector trailor we just return it.
        Returns an integer or none if no sector trailor found.
        """
        if block in self.sector_trailers_blocks:
            return block
        for trailer in self.sector_trailers_blocks:
            if trailer > block:
                return trailer
        return None

    @staticmethod
    def int2block(value: int) -> list:
        """Converts an integer to block data.

        Converts value to a list of hex values with length 16
        and returns that list. None used elements are padded with 0x00
        if value is greater than 32 bytes it returns none

        Keyword arguments:
        value -- an integer with max lenght of 32bytes

        returns a list or none
        """
        block_data=[]
        #convert the integer to hex
        hex_value=f'{value:0>32x}'
        if len(hex_value) > 32:
            return None
        pos=0
        while pos< len(hex_value):
            #convert the data to a real integer with base 16 and add it to the list
            block_data.append(int(f'0x{hex_value[pos:pos+2]}',16))
            pos+=2
        return block_data

    @staticmethod
    def block2int(block_data: list) -> int:
        """Converts block data to an integer.

        This function converts a block, which is a list of hex numbers,
        to an integer.
        returns an integer

        Keyword arguments:
        block_data --  a list of hex numbers.

        Returns an integer
        """
        exponent = 0
        number = 0
        for item in reversed(block_data):
            number += item * 256 ** exponent
            exponent += 1
        return number
