from Bayesian_Network_Resolver import Solve

if __name__ == "__main__":
    NetworkFile = input("NetworkFile Name: ")
    QueryFile = input("QueryFile Name: ")
    Solve(NetworkFile, QueryFile)
    print("press something to exit...")
    input()
