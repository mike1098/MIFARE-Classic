#!/usr/bin/env python3

"""Writes text to RFID Card.

"""
import sys
from pirc522 import RFID #https://github.com/ondryaso/pi-rc522
import mifare
from functions import auth_block, auth_new_block, connect_card

def format_card(rdr, cardid, card, startblock=1):
    """Overwrites all block data with 0x00

    Returns true if successful otherwise false
    """
    assert startblock > 0, "Cannot write to Manufacturer Block 0"
    data_block_index = card.data_blocks.index(startblock)
    sector_trailer=card.get_sector_trailer(startblock)
    # Authenticate to the first sector
    keya = card.get_key_a(startblock)
    if not auth_block(rdr, cardid, keya, sector_trailer):
        print(f"could not intially authenticate block {sector_trailer}")
        return False
    while data_block_index < len(card.data_blocks):
        new_block = card.data_blocks[data_block_index]
        sector_trailer= auth_new_block(rdr, card, cardid, sector_trailer, new_block)
        if not sector_trailer:
            print(f"could not authenticate block {new_block} ")
            return None
        print(f"Write {card.default_data_blocks} to block # {card.data_blocks[data_block_index]}")
        rdr.write(card.data_blocks[data_block_index], card.default_data_blocks)
        # Next data block
        data_block_index += 1
    return True

def write_text(rdr, cardid, card, text, startblock=8):
    """
    Write UTF8 encoded text to RFID card
    """
    assert startblock > 0, "Cannot write to Manufacturer Block 0"
    idx= 0
    text_encode= list(text.encode())
    data_block_index = card.data_blocks.index(startblock)
    sector_trailer=card.get_sector_trailer(startblock)
    print(f"index:{data_block_index} trailor {sector_trailer}")
    # Authenticate to the first sector
    keya = card.get_key_a(startblock)
    if not auth_block(rdr, cardid, keya, sector_trailer):
        print(f"could not intially authenticate block {sector_trailer}")
        return False
    while idx < len(text_encode):
        new_block = card.data_blocks[data_block_index]
        sector_trailer= auth_new_block(rdr, card, cardid, sector_trailer, new_block)
        if not sector_trailer:
            print(f"could not authenticate block {new_block} ")
            return False
        block_content = text_encode[idx:idx+card.block_length]
        # If the last block is less than 16 bytes we fill the remaining bytes with 0x00
        if len(block_content) < card.block_length:
            block_content.extend([0x00 for i in range(len(block_content),card.block_length)])
        print(f"write block #:{card.data_blocks[data_block_index]:02}"
              f"byte content: {block_content}")
        rdr.write(card.data_blocks[data_block_index], block_content)
        data_block_index += 1
        idx+=card.block_length
    return True

card1k = mifare.Classic1k()
reader = RFID()
id_card = connect_card(reader)

if id_card:
    format_card(reader, id_card, card1k)
    write_text(reader, id_card, card1k,sys.argv[1])
reader.cleanup()
