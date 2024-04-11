
# how to store the tables?

class node:

    def __init__(self, variable) -> None:
        self.variable = variable # variable must be positive
        self.factor = [] # (case vector, probability)
        self.parents = [] # parents will be filled later
        self.children = []


network: dict[int,node] = {}

def build_table(arr: list[int], i) -> list[list[int]]:
    tab:list[list[int]] = []
    if i == 0:
        tab = [[arr[i]], [-arr[i]]]
        return tab
    for j in [1, -1]:
        for k in build_table(arr, i-1):
            z = [j*arr[i]] + k
            tab.append(z)
    return tab


def build_network(data: str):
    global network

    inputs = data.split("\n")
    n = int(inputs[0])
    i = 1
    while i < len(inputs):
        j = list(map(int, inputs[i].split()))
        curr:node = None
        for k in j:
            if k in network:
                continue
            else:
                network[k] = node(k)

            if k == j[0]:
                curr = network[k]
        
        for k in j[1:]:
            curr.parents.append(k)

        network[curr.variable] = curr

        cases:list[list[int]] = build_table(j, len(j)-1)
        indx = 0
        for k in range(2**(len(j)-1)):
            p1, p2 = map(float, inputs[i+k+1].split())
            curr.factor.append([cases[indx], p1])
            curr.factor.append([cases[indx+1], p2])
            indx += 2
        
        i += 2**(len(j)-1) + 1


def print_table(L: int|list):
    if type(L) == int:
        if L not in network:
            print("No such node")
            return
        for i in network[L].factor:
            for j in i[:len(i)-1]:
                for k in j:
                    if k > 0:
                        print(f"+{k}", end=" ")
                    else:
                        print(k, end=" ")
            print(i[len(i)-1])
    elif type(L) == list:
        for i in L:
            for j in i[:len(i)-1]:
                for k in j:
                    if k > 0:
                        print(f"+{k}", end=" ")
                    else:
                        print(k, end=" ")
            print(i[len(i)-1])


def Reduce(factor: list[list[list[int], int]], variable_value: int) -> list[list[list[int], int]]: # if variable_value is positive then the variable is true, else false
    ans = []
    for i in factor:
        for j in i[0]:
            if j == variable_value:
                ans.append(i)
                break
    return ans

def Join(factor1: list[list[list[int], int]], factor2: list[list[list[int], int]]) -> list[list[list[int], int]]: # gives a conjunctive table: P(A/B) * P(B) = P(A, B)
    common_elements = set()
    for i in factor1[0][0]:
        if i in factor2[0][0]:
            common_elements.add(i)
    if len(common_elements) == 0:
        print("No common elements to join")
        return
    ans = []
    for e1, p1 in factor1:
        for e2, p2 in factor2:
            continue_flag = 0
            cmm_eles = []
            for i in e1:
                if abs(i) in common_elements and i not in e2:
                    continue_flag = 1
                    break
                elif abs(i) in common_elements:
                    cmm_eles.append(i)
            if continue_flag:
                continue
            z = [[0]*(len(e1)+len(e2)-len(common_elements)), p1*p2]
            j = 0
            for i in e1:
                z[0][j] = i
                j += 1
            for i in e2:
                if abs(i) not in common_elements:
                    z[0][j] = i
                    j += 1
            ans.append(z)
    return ans

def Sum(factor: list[list[list[int], int]], variable: int) -> list[list[list[int], int]]: # factor is a conjunctive table not a conditional probability table
    e_p = {}
    for e, p in factor:
        z = []
        for i in e:
            if abs(i) != variable:
                z.append(i)
        t = tuple(z)
        if t in e_p:
            e_p[t] += p
        else:
            e_p[t] = p
    ans = [0]*len(e_p)
    j = 0
    for i in e_p:
        ans[j] = [[k for k in i], e_p[i]]
        j += 1
    return ans

def Normalize():
    """ to do """
    pass

text = """2
1
0.1 0.9
2 1
0.8 0.2
0.1 0.9"""


build_network(text)

print_table(Join(network[2].factor, network[1].factor))

print('')

print_table(Sum(Join(network[2].factor, network[1].factor), 1))

# print_table(reduce(network[2].factor, 2))