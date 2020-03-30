import numpy as np
from intervalAnalyser import IntervalAnalyser
from connected import ProcessConnected
import pickle
import pandas as pd



def compare_connected_ind(folder_path, nodeset = [124,128,181,182], id_ = "01"):

    states = ["Dec","Honest"]
    b0ind = {state:[] for state in states}
    for state in states:

        filename = folder_path + id_ + '_int_cPPI_207'+state+'.txt'
        tda = IntervalAnalyser(filename)
        intervals = tda.process_intervals()

        data = [(interval[0], interval[1][0], interval[1][1]) for interval in intervals['d0int']]
        pc = ProcessConnected(data, 207)

        for node in nodeset:
            pc.find_connected_comp(node)

            b0ind[state].append({'node': node, 'level': pc._node_appearence[1],'len_comp':len(pc._compt),'compt': pc._compt})


    return b0ind

def compute_cycles_ind(folder_path, dim=1, nodeset = [124,128,181,182], id_ = "01"):
    states = ["Dec", "Honest"]
    b1ind = {state: [] for state in states}
    for state in states:
        filename = folder_path + id_ + '_int_cPPI_207' + state + '.txt'
        tda = IntervalAnalyser(filename)
        intervals = tda.process_intervals()
        for node in nodeset:
            b1 = tda.extract_intervals_withnodes(dim=dim, nodeset={node})
            if len(b1)>0:
                cycles, ints = list(zip(*b1))
                len_cycles = [len(cycle) for cycle in cycles]
                b1ind[state].append({'node': node,"ints": list(ints), "cycles":list(cycles), "len_cycles":len_cycles})
            else:
                b1ind[state].append({'node': node, "ints": [], "cycles": [], "len_cycles": []})

    return b1ind

def compute_all_b0(folder_path , nodeset=[124,128,181,182]):
    b0ind = {"01": []}
    indNums = ['0' + el if len(el) < 2 else el for el in [str(el) for el in np.arange(1, 25)]]

    for id_ in indNums:
        b0ind[id_] = compare_connected_ind(folder_path, nodeset=[124, 128, 181, 182], id_=id_)
    # create_dict()
    with open('b0cPPI.pickle', 'wb') as handle:
        pickle.dump(b0ind, handle, protocol=pickle.HIGHEST_PROTOCOL)
    return b0ind


def compute_all_cycles(folder_path,nodeset=[124,128,181,182]):
    b1ind = {"01":[]}
    b2ind = {"01":[]}
    indNums = ['0' + el if len(el) < 2 else el for el in [str(el) for el in np.arange(1, 25)]]
    for id_ in indNums:
        b1ind[id_] = compute_cycles_ind(folder_path, dim=1, nodeset = nodeset, id_ = id_)
        b2ind[id_] = compute_cycles_ind(folder_path, dim=2, nodeset=nodeset, id_= id_)

    # create_dict()
    with open('b1cPPI.pickle', 'wb') as handle: #../Dec_vs_Hon_207_ROIs/cPPI/
        pickle.dump(b1ind, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open('b2cPPI.pickle', 'wb') as handle:
        pickle.dump(b2ind, handle, protocol=pickle.HIGHEST_PROTOCOL)
    return b1ind, b2ind


    return b1ind

def write_intervals(intervals, filename):
    with open(filename, 'w') as file:
        for item in intervals['d0int']:
            file.write(f"{item[0]},{item[1]}\n")



if __name__ == "__main__":


    folder_path = "../Dec_vs_Hon_207_ROIs/intEirene/"
    b0ind = compute_all_b0(folder_path, nodeset=[124,128,181,182])
    #b1dim = compute_cycles_ind(folder_path, dim=1, nodeset=[124], id_="01")
    #b2dim = compute_cycles_ind(folder_path, dim=1, nodeset=[124], id_="01")
    b1dim, b2dim = compute_all_cycles(folder_path, nodeset=[124, 128, 181, 182])

    print('Done')