
import collections
import random
import scipy.special


class Triest:
    
    def __init__(self, path, M):
        self.M = M  # memory
        self.stream = open(path, 'r') # stream of the dataset
        self.S = set()  # S is Sample of  Gt: up to M edges (int)
        self.tau = 0 # tau global counter for the global number of triangles
        self.tauLocal= collections.defaultdict(int)
        self.t = 0
        self.epsilon = 0
        self.estimate = 0
        # dynamic
        self.d_i = 0
        self.d_o = 0
        self.w = 0
        self.s = 0
        self.k = 0
        self.p = 0

    def coin_flip(self, prob):
        #coin_toss = random.random()
        return random.random() < prob
        

    def sampleEdge(self):
        #decide if you need to sample a new edge or not
        if self.t <= self.M:
            return True
        elif self.coin_flip(self.M/self.t):
            remove = random.sample(self.S,1)[0]
            self.S.remove(remove)
            self.updateCounters("-", remove)
            return True
        return False


    def get_neighbours(self, edge):
        #get shared neighbors to the vertices, which are edge[0] and edge[1]
        # in the set of S
        neighbours_u = set()
        neighbours_v = set()

        for t in self.S:
            if t[0] == edge[0]:
                neighbours_u.add(t[1])
            if t[1] == edge[0]:
                neighbours_u.add(t[0])
            if t[0] == edge[1]:
                neighbours_v.add(t[1])
            if t[1] == edge[1]:
                neighbours_v.add(t[0])
        return neighbours_u, neighbours_v

    def updateCounters(self, operation, edge):
        neighbours_u, neighbours_v = self.get_neighbours(edge)
        neighbours_intersection = neighbours_u.intersection(neighbours_v)
        number_of_shared_neighbours = len(neighbours_intersection)

        if operation == '+' and number_of_shared_neighbours > 0 :
            self.tau += number_of_shared_neighbours
            self.tauLocal[edge[0]] += number_of_shared_neighbours
            self.tauLocal[edge[1]] += number_of_shared_neighbours
            for c in neighbours_intersection:
                self.tauLocal[c] += 1
        elif operation == '-' and number_of_shared_neighbours > 0:
            self.tau -= number_of_shared_neighbours
            self.tauLocal[edge[0]] -= number_of_shared_neighbours
            self.tauLocal[edge[1]] -= number_of_shared_neighbours
            for c in neighbours_intersection:
                self.tauLocal[c] -= 1


    def triest_base(self):
        self.t =0
        self.tau=0
        self.S = set()
        for line in self.stream:
            #get edge
            line= line.split()
            # skip comments starting with %
            if '%' not in line:
                u = int(line[0])
                v = int(line[1])
                edge = (u, v)
                #increment the number of extracted edges as variable t
                self.t += 1
                #check if memory is filled and remove an edge if neccessary
                if self.sampleEdge():
                    self.S.add(edge)
                    self.updateCounters('+', edge)
        
        self.epsilon = max(1, (self.t*(self.t-1)*(self.t-2))/(self.M*(self.M-1)*(self.M-2)))
        if self.t > self.M:
            self.estimate = self.tau * self.epsilon
        else:
            self.estimate = self.tau

############## Improved version:

    def sampleEdge_improved(self):
        # decide if you need to sample a new edge or not
        if self.t <= self.M:
            return True
        else:
            if self.coin_flip(self.M / self.t):
                remove = random.sample(self.S, 1)[0]
                self.S.remove(remove)
                return True
        return False

    def updateCounters_improved(self, edge):
        neighbours_u, neighbours_v = self.get_neighbours(edge)
        neighbours_intersection = neighbours_u.intersection(neighbours_v)
        n_t = max(1, ((self.t-1)*(self.t-2))/(self.M*(self.M-1)))
        number_of_shared_neighbours_improved = len(neighbours_intersection)*n_t
        self.tau += number_of_shared_neighbours_improved
        self.tauLocal[edge[0]] += number_of_shared_neighbours_improved
        self.tauLocal[edge[1]] += number_of_shared_neighbours_improved
        for c in neighbours_intersection:
            self.tauLocal[c] += n_t

    def triest_improved(self):
        self.S = set()
        self.t=0
        self.tau=0
        for line in self.stream:
            # get edge
            line = line.split()
            # skip comments starting with %
            if '%' not in line:
                u = int(line[0])
                v = int(line[1])
                edge = (u, v)
                # increment the number of extracted edges as variable t
                self.t += 1
                self.updateCounters_improved(edge)
                # check if memory is filled and remove an edge if neccessary
                if self.sampleEdge_improved():
                    self.S.add(edge)
        self.estimate = self.tau

############### Full Dynamic version
        
    def sampleEdge_Fd(self, edge):
         # decide if you need to sample a new edge or not
        if self.d_i + self.d_o == 0:
            if len(self.S) < self.M:
                self.S.add(edge)
                return True
            elif self.coin_flip(self.M / self.t):
                remove = random.sample(self.S, 1)[0]
                self.updateCounters("-", remove)
                self.S.remove(remove)
                self.S.add(edge)
                return True
        elif self.coin_flip(self.d_i/ (self.d_i + self.d_o)):
            self.S.add(edge)
            self.d_i -= 1
            return True
        else:
            self.d_o -= 1
            return False
        
            
    def triest_dynamic(self):
        self.t = 0
        self.tau = 0
        self.S = set()

        for line in self.stream:
            # get edge
            line = line.split()
            # skip comments starting with %
            if '%' not in line:
                u = int(line[0])
                v = int(line[1])
                edge = (u, v)

                # increment the number of extracted edges as variable t
                self.t += 1
                operation = '+' if random.random() < 0.9 else '-'
                if operation == '+':
                    self.s += 1
                elif operation == '-':
                    self.s -= 1
                
                if operation == '+':
                    if self.sampleEdge_Fd(edge):
                        self.updateCounters('+', edge)
                elif edge in self.S:
                    self.updateCounters('-', edge)
                    self.S.remove(edge)
                    self.d_i +=1
                else:
                    self.d_o +=1

        self.w = min(self.M, (self.s + self.d_o + self.d_i))
        self.k = 1
        for j in range(0, 2):
            s_j = scipy.special.binom(self.s, j)
            d_d_w_j = scipy.special.binom((self.d_i+self.d_o), (self.w-j))
            s_d_d_w = scipy.special.binom((self.s+self.d_i+self.d_o), self.w)
            self.k -= (s_j * d_d_w_j / s_d_d_w)

        if self.M < 3:
            self.p = 0
        else:
            t_k = (self.tau / self.k)
            c_i = (self.s*(self.s-1)*(self.s-2))
            b_i = (self.M*(self.M-1)*(self.M-2))
            self.p = t_k * c_i / b_i
        self.estimate = self.p






if __name__ == "__main__":


    dataset = input("Enter the number of dataset you want to test: ")
    M = int(input("Enter a value for M"))

    if dataset == "1":        
    # triangle count 57; n = 49	m = 107
        path = "./DataSet/out.contiguous-usa"
    elif dataset == "2":
         #tc: 16,750 n =	1,858  m=12,534
        path = "./DataSet/out.petster-friendships-hamster-uniq"
    elif dataset == '3':
        # triangle count = 36,365; n =26,475 m =53,381
        path = "./DataSet/out.as-caida20071105"
    

    triest_base = Triest(path, M)
    triest_base.triest_base()
    print("Base:")
    print(triest_base.estimate)

    triest_improved = Triest(path, M)
    triest_improved.triest_improved()
    print('Improved:')
    print(triest_improved.estimate)

    triest_dynamic = Triest(path, M)
    triest_dynamic.triest_dynamic()
    print("Dynamic:")
    print(triest_dynamic.estimate)





