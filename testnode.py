class Node:
    def __init__(self, id):
        self.id = id
        self.succ = self        # successor Node (not ID but Node)


def sort(myid, nlist):
    return sorted(nlist, key=lambda node: (node.id-myid) if node.id > myid else node.id-myid+2**32)

nodelist = [Node(65), Node(35), Node(1), Node(77), Node(100)]

for n in nodelist:
    print n.id

sl = sort(63, nodelist)

print

for n in sl:
    print n.id

