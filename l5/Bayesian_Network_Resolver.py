
import copy
import random

# how to store the tables?
DEP = 0
EVD = 1
TAB = 2

class node:

    def __init__(self, variable) -> None:
        self.variable: int = variable # variable must be positive
        self.factor: list[list[int], int] = [] # (case vector, probability)
        self.parents: list[node] = [] # parents will be filled later
        self.children: list[node] = []


network: dict[int,node] = {}

def build_table(arr: list[int], i) -> list[list[int]]:
    tab:list[list[int]] = []
    if i == len(arr):
        return []
    if i == len(arr)-1:
        tab = [[arr[i]], [-arr[i]]]
        return tab
    for j in [1, -1]:
        for k in build_table(arr, i+1):
            z = [j*arr[i]] + k
            tab.append(z)
    return tab


def build_network(data: str):
    global network

    inputs:list[str] = data.split("\n")
    n = int(inputs[0])
    i = 1
    while i < len(inputs):
        j = list(map(int, inputs[i].split()))
        curr:node = None
        for k in j:
            if k not in network:
                network[k] = node(k)

            if k == j[0]:
                curr = network[k]

        for k in j[1:]:
            curr.parents.append(k)

        network[curr.variable] = curr

        # cases:list[list[int]] = build_table(j, len(j)-1)
        cases: list[list[int]] = []
        if len(j) == 1:
            cases.append([j[0]])
            cases.append([-j[0]])
        else:
            for g in build_table(j, 1):
                cases.append([j[0]]+g)
                cases.append([-j[0]] + g)
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

class operations:

    @staticmethod
    def Reduce(table: list[list[list[int], int]], variable_values: list[int]) -> list[list[int], int]: # if variable_value is positive then the variable is true, else false
        ans = []
        for i in table:
            continue_flag = 0
            for j in variable_values:
                if j not in i[0]:
                    continue_flag = 1
            if continue_flag:
                continue
            ans.append(i)
        return ans

    @staticmethod
    def Join(table1: list[list[list[int], int]], table2: list[list[list[int], int]]) -> list[list[int], int]: # gives a conjunctive table: P(A/B) * P(B) = P(A, B)
        if len(table1) == 0:
            return table2
        if len(table2) == 0:
            return table1
        common_elements = set()
        for i in table1[0][0]:
            if i in table2[0][0]:
                common_elements.add(abs(i))

        ans = []
        if len(common_elements) == 0:
            # cartesian product
            for e1, p1 in table1:
                for e2, p2 in table2:
                    z = [e1+e2, p1*p2]
                    ans.append(z)
            # print(ans)
            # print('hh')
            return ans

        for e1, p1 in table1:
            for e2, p2 in table2:
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

    @staticmethod
    def Sum(table: list[list[list[int], int]], variables: list[int]) -> list[list[int], int]: # table is a conjunctive table not a conditional probability table

        e_p = {}
        for e, p in table:
            z = []
            for i in e:
                if abs(i) not in variables:
                    z.append(i)
            t = tuple(z)
            if t in e_p:
                e_p[t] += p
            else:
                e_p[t] = p
        ans = [[] for i in range(len(e_p))]
        j = 0
        for i in e_p:
            ans[j] = [[k for k in i], e_p[i]]
            j += 1
        if len(ans) == 0:
            return []
        if len(ans[0][0]) == 0:
            return []
        return ans
    
    @staticmethod
    def Normalize(table: list[list[int], int], evidence: list[list[int], int]) -> list[list[int], int]: # takes joint probability distribution table of given variables and evidences and does normalization
        ans = []
        for e1, p1 in table:
            for e2, p2 in evidence:
                continue_flag = 0
                for i in e2:
                    if i not in e1:
                        continue_flag = 1
                        break
                if continue_flag:
                    continue
                if p1 == 0:
                    ans.append([e1, 0])
                    continue
                ans.append([e1, p1/p2])
        if len(ans) == 0:
            return table
        return ans

    @staticmethod
    def find_common(table: list[list[int], int], vars: list[int]) -> list[int]:
        cmm = []
        if len(table) == 0:
            return []
        k = [abs(i) for  i in table[0][0]]
        for i in vars:
            if abs(i) in k:
                cmm.append(i)
        return cmm
    
class VariableElimination:

    @staticmethod
    def get_all_related(ele: int, all_elements: set):
        global network
        if ele == None:
            return
        all_elements.add(ele)
        for p in network[ele].parents:
            VariableElimination.get_all_related(p, all_elements)

    @staticmethod
    def joint_distribution(req_vars: list[int]):
        global network
        all_elements = set()
        pure_vars = {abs(i) for i in req_vars}
        for i in network:
            all_elements.add(i)
            
        hidden_vars = set()
        for i in all_elements:
            if i not in pure_vars:
                hidden_vars.add(i)
        
        query = []
        for i in all_elements:
            x = [abs(j) for j in network[i].factor[0][0]]
            y = operations.find_common(network[i].factor, req_vars)
            if len(y) > 0:
                z  = {DEP: {x[0]}, EVD: set(x[1:]), TAB: operations.Reduce(network[i].factor, y)}
            else:
                z = {DEP: {x[0]}, EVD: set(x[1:]), TAB: network[i].factor}
            query.append(z)

        while len(hidden_vars) > 0:
            x = hidden_vars.pop()
            f = {DEP: set(), EVD: set(), TAB: []}
            to_remove_from_query = []
            for i in query:
                if len(f[TAB]) == 0:
                    if x in i[DEP] or x in i[EVD]:
                        f[TAB] = i[TAB]
                        f[DEP] = i[DEP]
                        f[EVD] = i[EVD]
                        to_remove_from_query.append(i)
                    else:
                        continue
                else:
                    if len(i[EVD] & f[DEP]) > 0 or len(i[DEP] & f[EVD]) > 0 or len(i[DEP] & f[DEP]) > 0 or len(i[EVD] & f[EVD]) > 0:
                        stab_dep = copy.deepcopy(f[DEP])
                        stab_evd = copy.deepcopy(f[EVD])
                        f[DEP] |= i[DEP]
                        f[DEP] |= i[EVD] & f[DEP]
                        f[DEP] |= f[EVD] & i[DEP]

                        f[EVD] |= i[EVD]
                        f[EVD] -= i[EVD] & stab_dep
                        f[EVD] -= i[DEP] & stab_evd
                        f[TAB] = operations.Join(f[TAB], i[TAB])
                        to_remove_from_query.append(i)
            
            # summing out hidden variables
            if x not in f[EVD]:
                f[TAB] = operations.Sum(f[TAB], [x])

                if x in f[DEP]:
                    f[DEP].remove(x)
                elif x in f[EVD]:
                    f[EVD].remove(x)
            else:
                hidden_vars.add(x)
            # removing joined terms
            for i in to_remove_from_query:
                query.remove(i)
            # adding the new factor to the query terms
            query.append(f)

        if len(query) == 0:
            return []

        ans = []
        for i in query:
            ans = operations.Join(i[TAB], ans)
        return ans

    @staticmethod
    def variable_elimination(dependents: list[int], evidences: list[int]):
        global network
        all_elements = set()
        req_vars = dependents+evidences
        
        full_joint_form = VariableElimination.joint_distribution(req_vars)
        evidence_joint_form = VariableElimination.joint_distribution(evidences)
        ans = operations.Normalize(full_joint_form, evidence_joint_form)
        if len(ans) == 0:
            return 0
        return ans[0][1]

class RejectionSampling:

    @staticmethod
    def choose_row(table:list[list[int], int], sample: list[int]) -> list[int]:
        number = random.random() # gives a random number between [0,1]
        cumulative = 0
        sample_following_rows = []
        for row in table:
            continue_flag = 0
            for i in sample:
                if -i in row[0]:
                    continue_flag = 1
                    break
            if continue_flag:
                continue
            sample_following_rows.append(row)
        sum_check = 0
        for i in sample_following_rows:
            sum_check += i[1]
        if sum_check > 1:
            raise Exception("more than 1")
        if sum_check < 1:
            return
        for row in sample_following_rows:
            cumulative += row[1]
            if number <= cumulative:
                return row[0]

    @staticmethod
    def traversal(n: int, visited:set[int] = set(), sample:list[int] = []):
        global network
        if n in visited:
            return
        for p in network[n].parents:
            if p in visited:
                continue
            RejectionSampling.traversal(p, visited, sample)
        if n not in visited:
            visited.add(n)
            table = RejectionSampling.choose_row(network[n].factor, sample)
            if table is None:
                return
            for i in table:
                if i not in sample:
                    sample.append(i)
                    continue
    @staticmethod
    def rejection_sampling(dependents: list[int], evidence: list[int]):
        global network
        samples = []
        for i in range(10000):
            sample = []
            visited = set()
            for j in network:
                RejectionSampling.traversal(j, visited, sample)
            samples.append(sample)
        
        samples_following_evidence = []
        for i in samples:
            continue_flag = 0
            for j in evidence:
                if j not in i:
                    continue_flag = 1
                    break
            if continue_flag:
                continue
            samples_following_evidence.append(i)
        
        dependent_samples = 0 # no of these samples having given dependents
        for i in samples_following_evidence:
            continue_flag = 0
            for j in dependents:
                if j not in i:
                    continue_flag = 1
                    break
            if continue_flag:
                continue
            dependent_samples += 1
        if dependent_samples == 0:
            return 0
        return dependent_samples/len(samples_following_evidence)

def enumeration_method(dependents, evidences): # for verification of solution
    global network
    req_vars = dependents + evidences
    all_elemenets = set()
    all_evidences_related = set()
    for i in network:
        all_elemenets.add(i)
        all_evidences_related.add(i)
    x1 = []
    for i in all_elemenets:
        x1 = operations.Join(network[i].factor, x1)
    x2 = []
    for i in all_evidences_related:
        x2 = operations.Join(network[i].factor, x2)

    pure_vars = {abs(i) for i in req_vars}
    pure_evidences = {abs(i) for i in evidences}

    hidden_vars = []
    hidden_evidences = []
    for i in all_elemenets:
        if i not in pure_vars:
            hidden_vars.append(i)
    
    for i in all_evidences_related:
        if i not in pure_evidences:
            hidden_evidences.append(i)

    y1 = operations.Reduce(x1, operations.find_common(x1, req_vars))
    y2 = operations.Reduce(x2, operations.find_common(x2, evidences))

    z1 = operations.Sum(y1, hidden_vars)
    z2 = operations.Sum(y2, hidden_evidences)


    ans1 = operations.Normalize(z1, z2)
    if len(ans1) == 0:
        return 0
    if len(ans1[0]) == 0:
        return 0
    return ans1[0][1]

def query_processor(query:str):
    global network
    if query[:2] == 've': # variable elimination
        dependent_str, evidence_str = query[5:].split('e')
        dependent_eles, evidence_eles = dependent_str.split(), evidence_str.split()
        dependents = []
        evidences = []
        for i in dependent_eles:
            if i[0] == '~':
                dependents.append(-int(i[1:]))
            else:
                dependents.append(int(i))
        
        for i in evidence_eles:
            if i[0] == '~':
                evidences.append(-int(i[1:]))
            else:
                evidences.append(int(i))
        return VariableElimination.variable_elimination(dependents, evidences)

    else:
        dependent_str, evidence_str = query[5:].split('e')
        dependent_eles, evidence_eles = dependent_str.split(), evidence_str.split()
        dependents = []
        evidences = []
        for i in dependent_eles:
            if i[0] == '~':
                dependents.append(-int(i[1:]))
            else:
                dependents.append(int(i))
        
        for i in evidence_eles:
            if i[0] == '~':
                evidences.append(-int(i[1:]))
            else:
                evidences.append(int(i))
        return RejectionSampling.rejection_sampling(dependents, evidences)

def Solve(NetworkFile: str, QueryFile: str):
    global network
    network.clear()
    file = open(NetworkFile, 'r')
    build_network(file.read().strip())
    file.close()
    
    file = open(QueryFile, 'r')
    Queries = file.read().strip().split("\n")
    file.close()
    for Query in Queries:
        print(query_processor(Query))

def main():
    NetworkFile = "b3.txt"
    QueryFile = "q3.txt"
    Solve(NetworkFile, QueryFile)


main()
