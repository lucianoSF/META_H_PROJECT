import json
import random
import numpy as np
import time
import random as rd
from copy import deepcopy
from classes.Config import Config

config = Config()


n_iterations = 150
size_of_population = 50
e = 0.01
itens_to_change = int(0.10 * size_of_population)


alpha_limit = 1
#itens_to_change = 1


bip = 'instances/' + str(config.us) + '/BIP_for_all_combinations.json'

def constructed_solution(dict_BIPs):
    solution = []
    BS_number_of_users = {}
    objective = 0
    
    for t in range(1, config.ti+1):
    
        BS_number_of_users[t] = [0]*config.bs
    

    for t in range(1, config.ti+1):
        for u in range(1, config.us+1):
            
            # Apenas soluções onde as BS estão disponíveis
            availableSolutions = []
            for item in dict_BIPs[(str(t), str(u))]:
                bsUL = int(item[0].split('_')[0])
                bsDL = int(item[0].split('_')[1])
                if BS_number_of_users[t][bsDL-1] < config.V:
                    availableSolutions.append(item)
 
            #RCL = availableSolutions
    
            alpha = random.uniform(0, alpha_limit)
            min_cost = min(availableSolutions, key=lambda x: x[1])
            max_cost = max(availableSolutions, key=lambda x: x[1])
            threeshould_of_RCL = min_cost[1] + alpha*(max_cost[1] - min_cost[1])
            RCL = []
            
            # Criação da lista
            for item in availableSolutions:
                bsUL = item[0].split('_')[0]
                bsDL = item[0].split('_')[1]
                if item[1]<=threeshould_of_RCL:
                    RCL.append(item)
                    
            size_RCL = len(RCL)
            sol = random.randint(0, size_RCL-1)
            ulID = int(RCL[sol][0].split('_')[0])
            dlID = int(RCL[sol][0].split('_')[1])
            solution.append((str(t) + '_' + str(u) + '_' + RCL[sol][0], RCL[sol][1]))
            objective = objective + RCL[sol][1]

            BS_number_of_users[t][dlID-1] = BS_number_of_users[t][dlID-1] + 1

    return solution, objective/config.ti, BS_number_of_users
            


# Gravar soluções em arquivo
'''
def record_solutions(solutions):
    
    with open('saidas/SA/' + str(configus) + '_solution.csv', 'w') as file:
        file.write('Solution\n')
    
    with open('saidas/SA/' + str(config.us) + '_solution.csv', 'a') as file:
        for item in solutions:
            file.write(str(item) + '\n')
'''
            
def create_initial_population(dict_BIPs):
    population = []
    obj = []
    min_obj = None
    max_obj = None
    best_solution = None
    
    k = 0
    while k < size_of_population:
        solution, objective, BS_number_of_users = constructed_solution(dict_BIPs)
        population.append(solution)
        obj.append(objective)
        if min_obj == None or objective <= min_obj:
            min_obj = objective
            best_solution = solution
        if max_obj == None or objective >= max_obj:
            max_obj = objective

        k = k + 1
        
    #print(max_obj)    
    return population, obj, min_obj, max_obj, best_solution
    
    
def calculate_fitness(obj, min_obj, max_obj):

    fitness = []
    sum_fitness = 0
    for item in obj:
        ft = 1-((item-min_obj)/(max_obj-min_obj + e))
        fitness.append(ft)
        sum_fitness = sum_fitness + ft
        
    return fitness, sum_fitness


def calculate_probability(fitness, sum_fitness):
    sum_probability = 0
    probability = []
    
    for item in fitness:
        probability.append((item/sum_fitness)+sum_probability)
        sum_probability = sum_probability + item/sum_fitness
        
    probability[-1] = 1
    return probability
    

def choose_solution(population, probability):
    random_p = rd.random()
    sol_prob = None
    ind = 0
    
    for item in probability:
        
        if random_p <= item:
            break
            
        ind = ind + 1   
            
    return population[ind]


def verify(c, dict_BIPs):
    ind = 0
    obj = 0
    BS_number_of_users = {}
    for t in range(1, config.ti+1):
        BS_number_of_users[t] = [0]*config.bs
    
    while ind < len(c):
        
        t = int(c[ind][0].split('_')[0])
        u = int(c[ind][0].split('_')[1])
        
        dl_bs = int(c[ind][0].split('_')[3])
        
        
        BS_number_of_users[t][dl_bs-1] = BS_number_of_users[t][dl_bs-1] + 1
        
        if BS_number_of_users[t][dl_bs-1] > config.V:
            availableSolutions = []
            for item in dict_BIPs[(str(t), str(u))]:
                DL = int(item[0].split('_')[1])
                if BS_number_of_users[t][DL-1] < config.V:
                    availableSolutions.append(item)
       
            availableSolutions = sorted(availableSolutions, key=lambda tup: tup[1])
        

            c[ind] = (str(t) + '_' + str(u) +  '_' + availableSolutions[0][0], availableSolutions[0][1])
        
            
        obj = obj + c[ind][1]
        ind = ind + 1
        
    
    return (c, obj/config.ti)        
                

def crossover(p1, p2, dict_BIPs):
    mask = list(np.random.choice([0, 1], size=(len(p1),)))
    ind = 0
    c1 = []
    c2 = []

    for item in mask:
        if item == 0:
            c1.append(p1[ind])
            c2.append(p2[ind])

        if item == 1:
            c1.append(p2[ind])
            c2.append(p1[ind])
        ind = ind + 1
        
    c1, obj_c1 = verify(c1, dict_BIPs)
    
    c2, obj_c2 = verify(c2, dict_BIPs)
    
    return c1, obj_c1, c2, obj_c2


def create_population_of_childs(population, probability, dict_BIPs):
    new_population = []
    new_objectives = []
    min_obj = None
    max_obj = None
    m = 0
    
    while m < size_of_population/2:
        p1 = choose_solution(population, probability)
        p2 = choose_solution(population, probability)


        c1, obj_c1, c2, obj_c2 = crossover(p1, p2, dict_BIPs)

        new_population.append(c1)
        new_population.append(c2)

        new_objectives.append(obj_c1)
        new_objectives.append(obj_c2)
        
        
        if min_obj == None or obj_c1 <= min_obj:
            min_obj = obj_c1
        if max_obj == None or obj_c1 >= max_obj:
            max_obj = obj_c1
            
        if min_obj == None or obj_c2 <= min_obj:
            min_obj = obj_c2
        if max_obj == None or obj_c2 >= max_obj:
            max_obj = obj_c2

        m = m+1
        
    return new_population, new_objectives, min_obj, max_obj
    
    
    
    
def replace(population, fitness, obj, new_population, new_fitness, new_obj, best_solution, best_solution_cost):

    #print('\n\nOBJ', obj)
    #print('FIT', fitness)
    
    
    #print('\n\nNOBJ', new_obj)
    #print('NFIT', new_fitness)
    
    
    s = [(x,y) for _, x, y in sorted(zip(fitness, population, obj))]
        
    if s[-1][1] < best_solution_cost:
        best_solution_cost = s[-1][1]
        best_solution = s[-1][0]

    p1 = s[itens_to_change::]
    _, zp1 = zip(*(p1))
    #print('P1', zp1)

    s = [(x,y) for _, x, y in sorted(zip(new_fitness, new_population, new_obj), reverse=True)]

    if s[0][1] < best_solution_cost:
        best_solution_cost = s[0][1]
        best_solution = s[0][0]


    #print('test', itens_to_change, len(s))

    p2 = s[:itens_to_change:]
    _, zp2 = zip(*(p2))
    #print('P2', zp2)

    population, obj = zip(*(p1 + p2))
    
    
    #for item in p1:
    #    print(item)



    #print('POP', obj)
    
    sorted_obj = sorted(obj)
    
    max_obj = sorted_obj[-1]
    min_obj = sorted_obj[0]
    
    obj = list(obj)
    
    return population, obj, min_obj, max_obj, best_solution, best_solution_cost
    
    
# Gravar soluções em arquivo
def record_solutions(solutions, best, suf):
        with open('saidas/GA-GP/' + suf, 'a') as file:
            file.write('Pop;Best\n')
            
            for item1, item2 in zip(solutions, best):
                file.write(str(item1) +';' + str(item2) + '\n')    
    
    
def GA(dict_BIPs):
    l = 0
    
    best_solution = None
    best_solution_cost = None
    POP = []
    BEST = []
    population, obj, min_obj, max_obj, best_solution = create_initial_population(dict_BIPs)
    
    best_solution_cost = min_obj
    
    print('Best Sol: ', best_solution_cost)
    while l < n_iterations:
        
        POP.append(obj)
        BEST.append(best_solution_cost)

        m = 0

        fitness, sum_fitness = calculate_fitness(obj, min_obj, max_obj)


        probability = calculate_probability(fitness, sum_fitness)
        
        new_population, new_obj, new_min_obj,  new_max_obj = create_population_of_childs(population, probability, dict_BIPs)
    

        new_fitness, new_sum_fitness = calculate_fitness(new_obj, new_min_obj, new_max_obj)
        
        population, obj, min_obj, max_obj, best_solution, best_solution_cost = replace(population, fitness, obj, new_population, new_fitness, new_obj, best_solution, best_solution_cost)
        
        
        
        print('Best Sol: ', best_solution_cost)

        l = l + 1
        
    record_solutions(solutions=POP, best=BEST, suf=str(config.us) + '_solution.csv')
    return best_solution, best_solution_cost
    
    
if __name__ == '__main__':
    
    start = time.time()
    
    number_iterations_grasp = 1
  
 

    dict_BIPs = {}
    with open(bip) as json_file:
        data = json.load(json_file)
    
    for item in data:
        timeID = item.split('_')[0][1:]
        userID = item.split('_')[1][1:]
        ul_bs_ID = item.split('_')[2][4:]
        dl_bs_ID = item.split('_')[3][4:]
        
        
        if (timeID, userID) not in dict_BIPs:
            dict_BIPs[(timeID, userID)] = []

        dict_BIPs[(timeID, userID)].append((ul_bs_ID + '_' + dl_bs_ID, data[item]))

    #print(dict_BIPs)
    #print(asdasda)
    
    final_solution, final_objective = GA(dict_BIPs)
    

    final = time.time()
    
    print('Time: ', final-start)

    with open('saidas/ga_grasp.txt', 'a') as file:
        file.write("{:.5f}".format(final_objective) + ' ' + str(final-start) + '\n')
    
    
    
    
            
    
    
    
    
    
    