"""
Repository of functions for examples
"""

def auth_block(rdr, cardid, key, block=0):
    """Authenticate to a sector by a given block with authenticator A.

    Returns true if authentication was successful, otherwise false.
    """
    assert len(cardid) == 5, f"Card uid has wrong length: {cardid}"
    assert len(key) == 6, f"Authenticator has wrong length:{key}"
    error = rdr.card_auth(rdr.auth_a, block, key, cardid)
    if not error:
        print("Sucessful Auth")
        return True
    return False

def auth_new_block(rdr, card, cardid, sector_trailer, block):
    """
    Check if the new block has a new sector trailer and authenticate if needed.

    Returns true if authentication was successful, otherwise false.
    """
    new_sector_trailer = card.get_sector_trailer(block)
    if new_sector_trailer != sector_trailer:
        sector_trailer = new_sector_trailer
        keya = card.get_key_a(sector_trailer)
        if not auth_block(rdr, cardid, keya, sector_trailer):
            return False
    return True
