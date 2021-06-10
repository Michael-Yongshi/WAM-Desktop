import os

from pynfc.class_nfc import NFCconnection

    # FOR 2 SCANNERS: READER CENTRIC APPROACH. FOR 1 SCANNER THE NORMAL CARD CENTRIC APPROACH
    # FIRST CHECK IF THERE ARE 2 SCANNERS (LEN(READERS) == 2), IF IT DOES SWITCH TO READER CENTRIC

class NFC_Stuff(object):
    """Use NFC tag to save an id or get an id
    """

    def __init__(self):
        super().__init__()
     
        # try:
        self.nfcconnect = NFCconnection.initialize()

        # except:
            # print(f"Failed to connect to nfc card")

    def get_nfc_tag_uid(self):

        nfc_tag_uid = self.nfcconnect.metadata["UID"]

        return nfc_tag_uid

    def read_card(self):

        unique_id = self.nfcconnect.read_card()

        return unique_id

    def write_card(self, unique_id):
        """
        """

        # make sure the card is clean
        self.nfcconnect.wipe_card()

        # write to nfc tag
        self.nfcconnect.write_card(unique_id)