import re
import numpy as np

class Clean:
    """Methods for cleaning data"""
    
    def remove_non_ascii(string):
        """Returns the string without non ASCII characters"""
        stripped = (c for c in string if 0 < ord(c) < 127)
        string = ''.join(stripped)
        return string

    def pounds_and_pence(string):
        """Finds pounds or pounds and pence and returns as a float"""
        pence = re.search(r'(\d+[.]\d{2})', string)
        if pence:
            x, y = pence.span()
            digits = string[x:y]
        else:
            digits = re.sub(r'(\D+)', '', string)
        return float(digits)

    def outlier_limits(col):
        """Calculates upper and lower limit of Interquartile range"""
        Q1, Q3 = np.nanpercentile(col, [25, 75])
        IQR = Q3 - Q1
        LL = Q1 - 1.5*IQR
        UL = Q3 + 1.5*IQR
        return LL, UL