class AternosParsingError(Exception):
    """Exception raised for error in parsing the Aternos webpages or similar"""

    def __init(self, reason):
        self.reason = reason
