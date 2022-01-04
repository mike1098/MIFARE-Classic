#!/usr/bin/env python3
""" Reads text from RFID Card.

Returns text
"""
from pirc522 import RFID #https://github.com/ondryaso/pi-rc522
import mifare

def connect_card(rdr,retries=3):
    """Opens the connection to a RFID card for reading or writing.

    Returns the NUID/UID as a list
    """
    while retries > 0:
        (error, _) = rdr.request()
        if not error:
            (error, uid) = rdr.anticoll()
            if not error:
                if not rdr.select_tag(uid):
                    return uid
        retries -= 1
    return None

def auth_block(rdr, cardid, key, block=0):
    """Authenticate to a sector by a given block with authenticator A.
    
    Returns true if athentication was successful, otherwise false.
    """
    assert len(cardid) == 5, f"Card uid has wrong length: {cardid}"
    assert len(key) == 6, f"Authenticator has wrong length:{key}"
    error = rdr.card_auth(rdr.auth_a, block, key, cardid)
    if not error:
        print("Sucessful Auth")
        return True
    return False

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
        return ""
    while block_not_zero:
        error, block_content = rdr.read(card.data_blocks[data_block_index])
        if not error:
            print(f"read block #:{card.data_blocks[data_block_index]:02} byte content: {block_content}")
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
                new_sector_trailer = card.get_sector_trailer(card.data_blocks[data_block_index])
                if new_sector_trailer != sector_trailer:
                    sector_trailer = new_sector_trailer
                    print(f"New Sector Trailer: {sector_trailer}")
                    keya = card.get_key_a(sector_trailer)
                    if not auth_block(rdr, cardid, keya, sector_trailer):
                        print(f"could not authenticate block {sector_trailer}")
                        rdr.stop_crypto()
                        return None
        else:
            #TODO Find out where we handle card access
            rdr.stop_crypto()
            return ""
    #TODO Find out where we handle card access
    rdr.stop_crypto()
    return bytes(raw_content).decode()

reader = RFID()
card = mifare.Classic1k()
id_card = connect_card(reader)

print(f'Card NUID: {card.block2int(id_card)}')
TEXT=read_text(reader, id_card)
print(f"Text: {TEXT}")
# Calls GPIO cleanup
reader.cleanup()
