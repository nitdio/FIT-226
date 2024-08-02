import random
import os
import time
import copy

random.seed()
Density =0.8
Threshold = 0.7
N=11
M=11
class Agent:
    def __init__(self, agent_type, column, row):
        self.agent_type=agent_type
        self.column =column
        self.row=row

class Schelling_model:  # Class names should typically start with an uppercase letter
    def __init__(self, n: int, m: int):  # Corrected constructor method
        self.n = n
        self.m = m
        self.total_box = n*m

    def create_table(self):
        self._table = []
        for height in range(self.n):
            checkpoint = []
            for width in range(self.m):
                checkpoint.append('-')

            self._table.append(checkpoint)

    def add_agent(self,agent_type,y:int,x:int):
        self._table[y][x]=agent_type

    def agents_to_board(self,density:int):
        self.agents=[]
        self.empty=[]
        num_empty = int((1-density) * self.total_box)

        for column in range(self.n):
            for row in range(self.m):

                random_val=random.random()
                if random_val<num_empty/self.total_box:
                    self.add_agent('-',column,row)
                    self.empty.append((column,row))
                    num_empty-=1

                else:
                    agent=Agent(random.choice(['X','O']),column,row)
                    self.add_agent(agent.agent_type,agent.column,agent.row)
                    self.agents.append(agent)


    def print_table(self):
        for row in self._table:
            print(' '.join(str(cell) for cell in row))

    def step(self,threshold):
        sequence = list(range(len(self.agents)))
        random.shuffle(sequence)
        self.unhappy = 0
        for i in sequence:


            same = 0
            different = 0
            y, x = self.agents[i].column, self.agents[i].row
            empty_nei = []
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    if (dy == 0 and dx == 0) or (y + dy < 0) or (y + dy >= self.m) or (x + dx < 0) or (x + dx >= self.n):
                        continue
                    elif self._table[y + dy][x + dx] != '-':
                        if self._table[y][ x] == self._table[y + dy][x + dx]:
                            same += 1
                        else:
                            different += 1
                    else:
                        empty_nei.append((y + dy, x + dx))
            if same + different == 0:
                similar = 0
            else:
                similar = same / (same + different)
            if threshold > similar:
                self.unhappy += 1
                if len(empty_nei) != 0:
                    random.shuffle(empty_nei)

                    self.add_agent('-',y,x)
                    self.add_agent(self.agents[i].agent_type,empty_nei[0][0],empty_nei[0][1])

                    self.empty.append((y, x))

                    self.empty.remove(empty_nei[0])
                    self.agents[i].column, self.agents[i].row= empty_nei[0][0],empty_nei[0][1]




    def run(self):
        t=0
        self.create_table()
        self.agents_to_board(Density)
        self.print_table()
        record =None
        while True:

            record=copy.deepcopy(self._table)
            t+=1
            self.step(Threshold)
            if t%100==0:
                time.sleep(2)
                os.system('clear')
                self.print_table()

            if self._table==record:

                print(f"Time finished at {t} interval and no change")
                self.print_table()
                break

#hello

a=Schelling_model(10,10)
a.run()




