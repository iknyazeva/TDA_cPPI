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

def write_intervals(intervals, filename):
    with open(filename, 'w') as file:
        for item in intervals['d0int']:
            file.write(f"{item[0]},{item[1]}\n")



if __name__ == "__main__":

    id_ = '01'
    indNums = ['0' + el if len(el) < 2 else el for el in [str(el) for el in np.arange(1, 25)]]

    folder_path = "../Dec_vs_Hon_207_ROIs/intEirene/"
    b0ind = {id_: []}
    for id_ in indNums:
        b0ind[id_] = compare_connected_ind(folder_path , nodeset=[124,128,181,182], id_=id_)
    #create_dict()
    with open('../Dec_vs_Hon_207_ROIs/cPPI/b0cPPI.pickle', 'wb') as handle:
        pickle.dump(b0ind, handle, protocol=pickle.HIGHEST_PROTOCOL)

    print('Done')