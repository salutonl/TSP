import random
import math
import json
import numpy as np
SCORE_NONE = -1


class Life(object):
    """
    individual class, each individual include its gene(route) and score(calculate from march function)

    """
    def __init__(self, aGene = None):
        self.gene = aGene
        self.score = SCORE_NONE


class GA(object):

    def __init__(self, cro_rate, muta_rate, life_num, gene_len, mat_fun=lambda life: 1):
        self.crossover_rate = cro_rate
        self.mutation_rate = muta_rate
        self.life_count = life_num
        self.gene_length = gene_len
        self.mat_function = mat_fun
        self.lives = []
        self.best = None
        self.bounds = 0.0
        self.init_pop()

    def init_pop(self):
        self.lives = []
        for i in range(self.life_count):
            gene = [x for x in range(self.gene_length)]
            random.shuffle(gene)
            life = Life(gene)
            self.lives.append(life)

    def evaluate(self):
        self.bounds = 0.0
        self.best = self.lives[0]
        for life in self.lives:
            life.score = self.mat_function(life)
            self.bounds += life.score
            if self.best.score < life.score:
                self.best = life

    def crossover(self, parent1, parent2):
        index1 = random.randint(0, self.gene_length - 1)
        index2 = random.randint(index1, self.gene_length - 1)
        temp_ge = parent2.gene[index1:index2]
        new_gene = []
        p1len = 0
        for g in parent1.gene:
            if p1len == index1:
                new_gene.extend(temp_ge)
                p1len += 1
            if g not in temp_ge:
                new_gene.append(g)
                p1len += 1
        return new_gene

    def mutation(self, gene):
        index1 = random.randint(0, self.gene_length - 1)
        index2 = random.randint(0, self.gene_length - 1)
        new_gene = gene[:]
        new_gene[index1], new_gene[index2] = new_gene[index2], new_gene[index1]
        return new_gene

    def select(self):
        r = random.uniform(0, self.bounds)
        for life in self.lives:
            r -= life.score
            if r <= 0:
                return life

        raise Exception("error", self.bounds)

    def offspring(self):
        parent1 = self.select()
        rate = random.random()

        if rate < self.crossover_rate:
            parent2 = self.select()
            gene = self.crossover(parent1, parent2)
        else:
            gene = parent1.gene

        rate = random.random()
        if rate < self.mutation_rate:
            gene = self.mutation(gene)

        return Life(gene)

    def next_generation(self):
        self.evaluate()
        newLives = []
        newLives.append(self.best)
        while len(newLives) < self.life_count:
            newLives.append(self.offspring())
        self.lives = newLives


class TSP(object):
    def __init__(self, life_num=100, ):
        self.load_cities()
        self.life_count = life_num
        self.ga = GA(cro_rate=0.7,
                     muta_rate=0.01,
                     life_num=self.life_count,
                     gene_len=len(self.citys),
                     mat_fun=self.mat_function())

    def load_cities(self):
        self.citys = []
        with open("att48.txt") as f:
            for each_line in f:
                tmp = each_line.split()
                xy = (int(tmp[1]), int(tmp[2]))
                self.citys.append(xy)

    def distance(self, order):
        distance = 0.0
        for i in range(-1, len(self.citys) - 1):
            index1, index2 = order[i], order[i + 1]
            city1, city2 = self.citys[index1], self.citys[index2]
            dis = math.sqrt(((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2) / 10)
            if round(dis) < dis:
                dis = round(dis) + 1
            else:
                dis = round(dis)
            distance += dis
        return distance

    def mat_function(self):
        """
        match function, small distance get higher probability
        """
        return lambda life: 1.0 / self.distance(life.gene)

    def run(self, n=0):
        distance_list = []
        generate = [index for index in range(1, n + 1)]
        while n > 0:
            self.ga.next_generation()
            distance = self.distance(self.ga.best.gene)
            distance_list.append(distance)
            n -= 1
        return distance


def main():
    tsp = TSP()
    final = tsp.run(3000)
    dic = {
        "best distance:": final,
        "crossoverRate:": tsp.ga.crossover_rate,
        "mutation_rate:": tsp.ga.mutation_rate,
        "polulation:": tsp.ga.life_count,
        "best route:": tsp.ga.best.gene
    }
    js = json.dumps(dic)
    fileObject = open('ga.txt', 'a+')
    fileObject.write(js)
    fileObject.write('\n')
    fileObject.close()


def mean_di(fname,s ,e):
    values = []
    fin = open(fname, 'r')
    a = fin.readlines()
    a = a[s:e]
    for line in a:
        values.append(json.loads(line)['best distance:'])
    fin.close()
    return values


if __name__ == '__main__':
    for i in range(31):
        main()
    ga = mean_di('ga.txt', 22, 52)

    mean = np.mean(ga)
    std = np.std(ga)
    print(mean, std)