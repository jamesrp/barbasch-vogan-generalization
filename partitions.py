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

current = [[2]]
n = 1
for loop in range(5):
    intermediate = []
    for partition in current:
        intermediate.extend(branch_up(partition))
    # Use the fact that there is a copy of the trivial in uppers, hence 
    # there is a copy of the trivial in intermediate
    n += 2
    intermediate.remove([n])
    uppers = search_up(intermediate)
    assert(len(uppers) == 1)
    current = [[n+1]] + uppers[0]
    print current
