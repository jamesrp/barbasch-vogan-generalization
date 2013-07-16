def pp(partition):
    return str(partition)[1:-1].replace(', ','-')

def branch_up(partition):
    out = []
    for i in range(len(partition)):
        if i > 0 and partition[i] == partition[i-1]:
            continue
        newp = list(partition)
        newp[i] += 1
        out.append(newp)
    out.append(list(partition)+[1])
    return out

def branch_down(partition):
    out = []
    for i in range(len(partition)-1):
        if partition[i] == partition[i+1]:
            continue
        newp = list(partition)
        newp[i] -= 1
        out.append(newp)
    if partition[-1] == 1:
        newp = partition[:-1]
    else:
        newp = list(partition)
        newp[-1] -= 1
    out.append(newp)
    return out

# I want to also define a search_down for completeness,
# however it's actually irrelevant as we can just flip everything
# and use search_up.
def search_up(down_elements, forbidden_choices= None):
    #print "search_up(%s,%s)"%(str(down_elements),str(forbidden_choices))
    if down_elements == []:
        return [[]]
    if forbidden_choices == None:
        forbidden_choices = []
    else:
        forbidden_choices = list(forbidden_choices)
    # Idea - in the BV case it seemed that there was a nice order to search in
    # which eliminated most decisions. We may want to sort the downstairs
    # by this order - is it dominance?
    out = []
    partition1 = down_elements[0]
    #print "checking ",partition1
    valid_choices = []
    for partition2 in branch_up(partition1):
        down_p2 = branch_down(partition2)
        if all(partition3 in down_elements for partition3 in down_p2):
            valid_choices.append([partition2,down_p2])
        else:
            forbidden_choices.append(partition2)
    #print "valid_choices = ",valid_choices
    #print "forbidden_choices = ",forbidden_choices
    for partition2,down_p2 in valid_choices:
        rest = list(down_elements)
        for partition3 in down_p2:
            rest.remove(partition3) # probably can combine this with the valid check to save time
        for result in search_up(rest,forbidden_choices):
            out.append([partition2]+result)
    return out

def BV():
    current = [[2]]
    n = 1
    for loop in range(3):
        intermediate = raise_all(current)
        # Use the fact that there is a copy of the trivial in uppers, hence 
        # there is a copy of the trivial in intermediate
        n += 2
        intermediate.remove([n])
        uppers = search_up(intermediate)
        assert(len(uppers) == 1)
        current = [[n+1]] + uppers[0]
        print current

def raise_all(down_elements):
    # Helper function to induce a list one level up.
    out = []
    for partition in down_elements:
        out.extend(branch_up(partition))
    return out

def pieri(partition,k,limit=None):
    out = []
    if limit == None:
        limit = k + partition[0]
    if partition == []:
        if k <= limit:
            if k > 0:
                return [[k]]
            if k == 0:
                return [[]]
        return []
    if k < 0:
        return []
    first = partition[0]
    for i in range(min(k,limit-first)+1):
        rest = partition[1:]
        for x in pieri(rest,k-i,first):
            out.append([first+i]+x)
    return out

def raise_all_pieri(elements,k):
    out = []
    for elem in elements:
        out.extend(pieri(elem,k))
    return out

def BVm(m,v=None):
    if v == None:
        v = [[m]]
    n=(1+sum(v[0])/m)
    if n > 4:
        return
    print "Analyzing V_%d"%n
    intermediate = sorted(raise_all_pieri(v,m-1))
    su = [sorted(x) for x in search_up(intermediate)]
    trivial = [sum(su[0][0])]
    def uniquep(x):
        n = len(x)
        for i in range(n-1):
            if x[i] == x[i+1]:
                return False
        return True
    valids = []
    for x in su:
        if trivial in x:
            print x
            valids.append(x)
            if uniquep(x):
                print "Multiplicity-Free"
            print ""
    if len(valids) == 1:
        print "1 valid detected. Continuing.\n"
        BVm(m,valids[0])

BVm(2)
