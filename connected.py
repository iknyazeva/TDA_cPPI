
class UnionFind(object):
    def __init__(self, n):
        self.n = n
        self.parent = [-1] * n
        self.link = [-1]*n
        for i in range(n):
            self.parent[i] = i
            self.link[i] = i

    def find(self, i):
        # Path Compression
        if self.parent[i] != i:
            self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, x, y):
        xroot = self.find(x)
        yroot = self.find(y)
        if xroot != yroot:
            self.parent[yroot] = xroot
            self.create_link(x,y)

    def create_link(self,x,y):
        temp = self.link[y]
        self.link[y] = self.link[x]
        self.link[x] = temp


    def print_set(self,x):
        root = x
        conn_set = [x]
        while self.link[x]!=root:
            x = self.link[x]
            conn_set.append(x)
        return [conn+1 for conn in conn_set]



def read_data(filename, nlines=206):
    import re
    data = []
    with open(filename,'r') as f:
        for x in range(nlines):
            line = next(f)
            pattern = re.search("(\d.\d+),\[(\d+),\s(\d+)", line)
            #pattern = re.search("(\d+)", line)
            #record = [float(pattern.group(1), int(pattern.group(2),int(pattern.group(3))]
            record = float(pattern.group(1)), int(pattern.group(2)), int(pattern.group(3))
            data.append(record)
    return data



class ProcessConnected(object):
    def __init__(self, data, n):
        self.n = n
        self.data = data
        self._node_of_interest = []
        self._node_appearence = []
        self._compt = []

    def find_first_appearance(self, node):
        """

        :param data: list of b0 intervals, where each record is tuple (level, start, end)
        :param node: interested node
        :return:  level and line_number where node first appeared
        """
        self._node_of_interest = node

        assert node <= self.n, "Current node couldn't be less then the number of nodes"

        isFind = False
        for idx, record in enumerate(self.data):
            if (record[1] == node) | (record[2] == node):
                isFind = True
                break
        if isFind:

            self._node_appearence = (idx + 1, record[0])

            return (idx + 1, record[0])
        else:
            return None

    def find_connected_comp(self,node):
        i, level = self.find_first_appearance(node)
        uf = UnionFind(self.n)
        for record in self.data[:i]:
            uf.union(record[1] - 1, record[2] - 1)
        self._compt = uf.print_set(node - 1)


if __name__ == "__main__":
    data = read_data('b0.txt')
    node  = 128
    #i, level = find_first_appearance(data, node)
    #uf = UnionFind(207)
    #for record in data[:i]:
    #    uf.union(record[1]-1,record[2]-1)
    #compt = uf.print_set(node-1)
    pc = ProcessConnected(data, 207)
    pc.find_connected_comp(128)
    pc.find_connected_comp(124)


    print('Hi')
