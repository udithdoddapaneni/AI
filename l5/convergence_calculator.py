import matplotlib.pyplot as mat
from Bayesian_Network_Resolver import VariableElimination, RejectionSampling, build_network, network


def error_vs_no_samples_plot(convergence_table: list):
    x_axis = [] # number of samples
    y_axis = [] # error
    for i in convergence_table:
        x_axis.append(i[0])
        y_axis.append(i[3])
    
    mat.xlabel("no.of samples")
    mat.ylabel("error percentage")

    mat.plot(x_axis, y_axis)
    mat.show()

def convergence(convergence_table: list):
    true_probability = convergence_table[0][1]

    x_axis = [] # number of samples
    y_axis = [] # average of rejection sampling values over given number of samples

    for i in convergence_table:
        x_axis.append(i[0])
        y_axis.append(i[2])

    mat.xlabel("no.of samples")
    mat.ylabel("avg value of rejection sampling")

    mat.plot(x_axis, y_axis, label = "Rejection Sampling")
    y_true_axis = [true_probability]*len(y_axis)
    mat.plot(x_axis, y_true_axis, label = "Variable Elimination")

    legend = mat.legend(loc='lower right')
    mat.show()


def example_plots(Network):

    "ve q 4 5 e ~1 2 3"
    "ve q 4 e ~2 3"
    "rs q 4 e 1"

    ex1 = convergence_calculator(Network, [4,5], [-1, 2, 3])
    ex2 = convergence_calculator(Network, [4], [-2, 3])
    ex3 = convergence_calculator()

def convergence_calculator(Network: str, dependents: list[int], evidences: list[int]):
    global network
    network.clear()
    build_network(Network)

    true_probability = VariableElimination.variable_elimination(dependents, evidences)

    convergence_table = []

    for i in range(1, 11):
        no_of_sample = i
        avg_estimated_probability = 0
        for j in range(1000):
            avg_estimated_probability += RejectionSampling.rejection_sampling(dependents, evidences, no_of_sample)/1000
        error_percentage = (abs(avg_estimated_probability-true_probability)/true_probability)*100
        t = [no_of_sample ,true_probability, avg_estimated_probability, error_percentage]
        convergence_table.append(t)
    
    return convergence_table

text = """5
4 2 3
0.5 0.5
0.5 0.5
0.5 0.5
0.5 0.5
2 1
0.5 0.5
0.5 0.5
3 1
0.5 0.5
0.5 0.5
1
0.5 0.5
5 3
0.5 0.5
0.5 0.5"""

if __name__ == "__main__":
    convergence_table = convergence_calculator(text, [4], [-2, 3])
    for t in convergence_table:
        print(f"no.of samples: {t[0]} ; Actual Probability: {t[1]} ; Estimated Probability: {t[2]} ; Error Percentage: {t[3]}")

    convergence(convergence_table)
    error_vs_no_samples_plot(convergence_table)
