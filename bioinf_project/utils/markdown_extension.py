
def build_url(label, base, end):
    """ Build a url from the label, a base, and an end. """
    clean_label = re.sub(r'([ ]+_)|(_[ ]+)|([ ]+)', '_', label)
    return '%s%s%s'% (base, clean_label, end)

