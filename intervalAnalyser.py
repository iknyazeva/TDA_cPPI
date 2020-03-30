from collections import Counter
import pandas as pd
import numpy as np
import warnings
import re


class IntervalAnalyser:
        def __init__(self, filepath, size = 207):
            self.filepath = filepath
            self.size = size
            
        def process_intervals(self):
            filename = self.filepath
            with open(filename, "r") as ins:
                d0int = []
                d0intervals = []
                d1int = []
                d1intervals = []
                d2intervals = []
                d2int = []
                d3int = []
                d3intervals = []
                for line in ins:
                    search_d0int = re.search('^\[0.000, (\d.\d+)\):\s\[(\d+)\]\+\[(\d+)\]', line)                    #^\[0\.\d+,\s\d\.\d+\):\s\[\d+\]\+\[\d+\]
                    search_d1int =re.search('\[(\d+),(\d+)\]',line)
                    search_d2int=re.search('\[(\d+),(\d+),(\d+)\]',line)
                    search_d3int=re.search('\[(\d+),(\d+),(\d+)\,(\d+)\]',line)

                    if search_d0int is not None:
                        d0intervals.append(float(search_d0int.group(1)))

                        #print( search_d0int.group(0))
                        d0int.append([int(search_d0int.group(2)),int(search_d0int.group(3))])
                    elif  search_d1int is not None:
                        holes = []

                        d1intervals.append(line.split(':')[0][1:-1])

                        splitted_line = line.split('+')
                        for records in splitted_line:
                            search_d1 =re.search('\[(\d+),(\d+)\]',records)
                            holes.append([int(search_d1.group(i)) for i in range(1,3)])
                        d1int.append(holes) 
                    elif  search_d2int is not None: 
                        holes = []
                        d2intervals.append(line.split(':')[0][1:-1])
                        splitted_line = line.split('+')
                        for records in splitted_line:
                            search_d2 =re.search('\[(\d+),(\d+),(\d+)\]',records)
                            holes.append([int(search_d2.group(i)) for i in range(1,4)])
                        d2int.append(holes)   
                    elif  search_d3int is not None:
                        holes = []
                        d3intervals.append(line.split(':')[0][1:-1])

                        splitted_line = line.split('+')
                        for records in splitted_line:
                            search_d3 =re.search('\[(\d+),(\d+),(\d+)\,(\d+)\]',records)
                            holes.append([int(search_d3.group(i)) for i in range(1,5)]) 
                        d3int.append(holes) 
            self.d0int = sorted(zip(d0intervals,d0int))
            self.d1int = [d1int,d1intervals]
            self.d2int = [d2int,d2intervals]
            self.d3int = [d3int ,d3intervals]
            return {'d0int':sorted(zip(d0intervals,d0int)), 'd1int':[d1int,d1intervals],
                    'd2int': [d2int,d2intervals], 'd3int': [d3int ,d3intervals]}

        def extract_intervals_withnodes(self,dim=1, nodeset = {7,8,9,10}) -> object:

            try:
                intervals = getattr(self,'d'+str(dim)+'int')
                setlist = [(set(np.array(item1).flatten()), item2) for item1, item2 in
                             zip(intervals[0], intervals[1])]
                return [el for el in setlist  if len(nodeset.intersection(el[0])) > 0]

            except AttributeError:
                print('There is no intervals first this dimension ...')

            
        def compute_interval_statistics(self, dim=1, filter_by_length = None, filter_by_start = None):
            
            """
            filter_by_start: values from with start from the value or greater
            """
            assert (filter_by_length is None) or (filter_by_length is np.inf) or (isinstance(filter_by_length,float)), 'Value should by np.inf or float'

            try:
                intervals = getattr(self,'d'+str(dim)+'int')
                
                if (filter_by_length is None) and (filter_by_start is None):
                    intervals = [(set(np.array(item1).flatten()),item2) for item1, item2 in zip(intervals[0],intervals[1])]
                else:    
                    interval_set = set(intervals[1])
                    interval_dict = {}
                    for element in interval_set:
                        vals = [float(el) for el in element.split(',')]
                        interval_dict[element] = (vals[0],np.diff(vals)) 
                
            
                
                    if filter_by_start is not None:
                        klist = []

                        for k,v in interval_dict.items():
                            if v[0]<= filter_by_start:
                                klist.append(k)
                        intervals = [(set(np.array(item1).flatten()),item2) for item1, item2 in zip(intervals[0],intervals[1]) if item2 in klist]
       
                    
                    if filter_by_length == np.inf:
                        klist = []
                        for k,v in interval_dict.items():
                            if v[1] == np.inf:
                                klist.append(k)
                        intervals = [(set(np.array(item1).flatten()),item2) for item1, item2 in zip(intervals[0],intervals[1]) if item2 in klist]
    
                    elif isinstance(filter_by_length,float):
                        klist = []
                        for k,v in interval_dict.items():
                            if v[1] >= filter_by_length:
                                klist.append(k)
                        intervals = [(set(np.array(item1).flatten()),item2) for item1, item2 in zip(intervals[0],intervals[1]) if item2 in klist]

    
                        
                    

                #overallCnt = Counter()
                #cnts = []
                #for cycle, barcode in intervals:
                #    cnt = Counter(np.array(cycle).flatten())
                #    cnts.append(cnt)
                #    overallCnt.update(cnt)
                #return cnts, overallCnt  
                return intervals
            except AttributeError:
                print('You should process intervals first with process_intervals ...')

        def compute_interval_node_stat(self, dim=1, nodesize = 139):
            intervals = getattr(self, 'd' + str(dim) + 'int')

            output = []
            for item1, item2 in zip(intervals[0], intervals[1]):
                output.append((set(np.array(item1).flatten()), (len(set(np.array(item1).flatten())),item2)))
            _,collists = list(zip(*output))
            cols = list(set(collists))
            df = pd.DataFrame(0,index = np.arange(nodesize),columns=cols)

            for cycle, interval in output:
                for node in cycle:
                    df.iloc[node][interval] += 1

            
            return df