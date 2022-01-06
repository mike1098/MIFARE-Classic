#!/usr/bin/env python3
""" Reads text from RFID Card.

Returns text
"""
from pirc522 import RFID #https://github.com/ondryaso/pi-rc522
import mifare
from functions import auth_block, auth_new_block, connect_card

def read_text(rdr, cardid, startblock=8):
    """Reads text from the RFID card.

    The TEXT must be UTF8 encoded and terminated with at least one 0x00 otherwise it
    returns none. If a sector could not be authenticated it returns None

    returns a byte object otherwise None
    """
    block_not_zero = True
    data_block_index = card.data_blocks.index(startblock)
    raw_content=[]
    sector_trailer=card.get_sector_trailer(startblock)
    keya = card.get_key_a(startblock)
    if not auth_block(rdr, cardid, keya, startblock):
        print(f"could not intially authenticate block {sector_trailer}")
        return None
    while block_not_zero:
        error, block_content = rdr.read(card.data_blocks[data_block_index])
        if not error:
            print(f"read block #:{card.data_blocks[data_block_index]:02}"
                  f" byte content: {block_content}")
            raw_content.extend(block_content)
            if 0x00 in raw_content:
                print("Found 0x00 in content -> end of text. Stop reading.")
                block_not_zero = False
            else:
                data_block_index += 1
                if data_block_index == len(card.data_blocks):
                    print("reached end of card")
                    rdr.stop_crypto()
                    return None
                new_block = card.data_blocks[data_block_index]
                sector_trailer= auth_new_block(rdr, card, cardid, sector_trailer, new_block)
                if not sector_trailer:
                    print(f"could not authenticate block {new_block} ")
                    return None
        else:
            return None
    return bytes(raw_content).decode()

reader = RFID()
card = mifare.Classic1k()
id_card = connect_card(reader)
if id_card:
    print(f'Card NUID: {card.block2int(id_card)}')
    TEXT=read_text(reader, id_card)
    print(f"Text: {TEXT}")

else:
    print('No card found!')
# Calls GPIO cleanup and stop crypto
reader.cleanup()
