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


