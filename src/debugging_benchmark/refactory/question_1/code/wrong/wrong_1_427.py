def search(x,seq):
    for i,elem in enumerate(seq):
        if x <= elem:
            return i
        else:
            return len(seq)
        
