import re
class Clean:
    """Methods for cleaning data"""
    
    def remove_non_ascii(string):
        """Returns the string without non ASCII characters"""
        stripped = (c for c in string if 0 < ord(c) < 127)
        string = ''.join(stripped)
        return string

    def only_digits(string):
        """Returns sting with non digits removed"""
        if string:
            digits = re.sub(r'(\D+)', '', string)
        return digits