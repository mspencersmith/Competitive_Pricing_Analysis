import re
class Clean:
    """Methods for cleaning data"""
    
    def remove_non_ascii(string):
        """Returns the string without non ASCII characters"""
        stripped = (c for c in string if 0 < ord(c) < 127)
        string = ''.join(stripped)
        return string

    def pounds_and_pence(string):
        """Returns string of pounds or pounds and pence"""
        pence = re.search(r'(\d+[.]\d{2})', string)
        if pence:
            x, y = pence.span()
            digits = string[x:y]
        else:
            digits = re.sub(r'(\D+)', '', string)
        return digits