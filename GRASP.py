import json
import random
import time
import random as rd
from copy import deepcopy
from classes.Config import Config

config = Config()

#tm = 10#tempo
#bs=5#base_stations
#us=30#usuários
#limit=18#limite de usuários por bs
alpha_limit = 0.0



#users = 'instances/' + str(us) + '/users.json'
#bs_f = 'instances/' + str(us) + '/base_stations.json'
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
                #if bsUL==bsDL and BS_number_of_users[t][bsUL-1] < config.V-1:
                #    availableSolutions.append(item)
            
            
            # Configuração dos limites para a lista RCL
            #alpha = random.random()
            alpha = random.uniform(0, alpha_limit)
            min_cost = min(availableSolutions, key=lambda x: x[1])
            max_cost = max(availableSolutions, key=lambda x: x[1])
            threeshould_of_RCL = min_cost[1] + alpha*(max_cost[1] - min_cost[1])
            RCL = []

            
            #print('1', dict_BIPs[(str(t), str(u))])
            #print('2', availableSolutions)
            
            
            
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
            #print('Before', BS_number_of_users[t][dlID-1])
            #BS_number_of_users[t][ulID-1] = BS_number_of_users[t][ulID-1] + 1
            BS_number_of_users[t][dlID-1] = BS_number_of_users[t][dlID-1] + 1
            #print('After', BS_number_of_users[t][dlID-1])
            
    #print('This is the values', BS_number_of_users)
   
    return solution, objective/config.ti, BS_number_of_users
            
    


# Criar solução candidata
def create_new_solution(dict_BIPs, initial_solution, initial_objective, BS_number_of_users):
    
    # Preparação para criação de nova solução
    new_solution = deepcopy(initial_solution)
    new_objective = initial_objective
    # Escolher aleatóriamente um periodo t para realizarmos mudanças no UPL e DWL
    
    index_item_to_change = random.randrange(0, len(new_solution)-1)
    
    timeID = str(new_solution[index_item_to_change][0].split('_')[0])
    userID = str(new_solution[index_item_to_change][0].split('_')[1])
    oldulID = str(new_solution[index_item_to_change][0].split('_')[2])
    olddlID = str(new_solution[index_item_to_change][0].split('_')[3])
    
    #BS_number_of_users[int(timeID)][int(oldulID)-1] = BS_number_of_users[int(timeID)][int(oldulID)-1] - 1
    BS_number_of_users[int(timeID)][int(olddlID)-1] = BS_number_of_users[int(timeID)][int(olddlID)-1] - 1
    
    
    available_itens = []
    
    for item in dict_BIPs[(timeID, userID)]:
        ulID = int(item[0].split('_')[0])
        dlID = int(item[0].split('_')[1])
        
        if BS_number_of_users[int(timeID)][dlID-1] < config.V:
            if ulID != oldulID or dlID != olddlID:
                available_itens.append(item)
                
        #if ulID == dlID and BS_number_of_users[int(timeID)][ulID-1] < config.V-1:
        #    if ulID != oldulID or dlID != olddlID:
        #        available_itens.append(item)
          
        
    newsol = random.randint(0, len(available_itens)-1)

    #print('this is the value', available_itens[newsol])
    newulID = int(available_itens[newsol][0].split('_')[0])
    newdlID = int(available_itens[newsol][0].split('_')[1])
    
    #BS_number_of_users[int(timeID)][newulID-1] = BS_number_of_users[int(timeID)][newulID-1] + 1
    BS_number_of_users[int(timeID)][newdlID-1] = BS_number_of_users[int(timeID)][newdlID-1] + 1
    

    
    new_objective = new_objective - (new_solution[index_item_to_change][1]/config.ti)
    new_objective = new_objective + available_itens[newsol][1]
    
    #print(new_solution[index_item_to_change])
    new_solution[index_item_to_change] = (timeID + '_' + userID + '_' + available_itens[newsol][0], available_itens[newsol][1])
    #print(new_solution[index_item_to_change])
    #print('Available')

    return new_solution, new_objective, BS_number_of_users
    

# SA
def SimulatedAnnealing(dict_BIPs, initial_solution, initial_objective, BS_number_of_users, temperature):

    k = 0 # iteração sem mudança na solução
    LIST_OF_SOLUTIONS = []
    best_solution = deepcopy(initial_solution)
    best_solution_objective = initial_objective
    
    # Itera enquanto a solução não melhorar em k iterações
    while k < number_iterations_solution_is_not_improved:
        # Conjunto de soluções vizinhas locais a serem exploradas
        for l in range(iterations_each_temperature):
            
            # Gera solução candidata
            #print('before')
            candidate_solution, candidate_objective, BS_number_of_users = create_new_solution(dict_BIPs, initial_solution, initial_objective, BS_number_of_users)
            
            delta_C = candidate_objective - initial_objective
            
            # Compara se a solução candidata é melhor do que a solução inicial
            if delta_C < 0:
                initial_solution = candidate_solution
                initial_objective = candidate_objective
            # Se não for ainda existe possibilidade de aceitação da solução conforme a variação da temperatura
            else:
                variable_control = random.random()
                
                expo = (-1 * delta_C)/temperature
                # Solução degradada é aceita    
                if variable_control <= pow(EULER, expo):
                    initial_solution = candidate_solution
                    initial_objective = candidate_objective

        #Atualização da temperatura
        temperature = temperature*alpha
        

        #print('Actual Solution Cost --> ', initial_objective, 'k: ', k, 'T: ', temperature)
        
        # A melhor solução em cada valor de temperatura é guardada

        if initial_objective < best_solution_objective:
            best_solution = initial_solution
            best_solution_objective = initial_objective
            k = 0
        else:
            k = k + 1
                
        print('Best Solution Cost --> ', best_solution_objective, 'k: ', k, 'T: ', temperature)
                
        #LIST_OF_SOLUTIONS.append(initial_objective)
        
    #record_solutions(solutions=LIST_OF_SOLUTIONS)

    return best_solution, best_solution_objective
 
    
    
def GRASP(dict_BIPs, temperature):

    k = 0 # iteração sem mudança na solução
    LIST_OF_SOLUTIONS = []
    LIST_OF_BEST = []
    
    best_solution = None
    best_solution_objective = None

    
    # Itera enquanto a solução não melhorar em k iterações
    while k < number_iterations_grasp:
        # Conjunto de soluções vizinhas locais a serem exploradas

        # Gera solução candidata
        new_solution, new_objective, BS_number_of_users  = constructed_solution(dict_BIPs)

        #print(new_objective)

        new_solution, new_objective = SimulatedAnnealing(dict_BIPs, new_solution, new_objective, BS_number_of_users, temperature)


        
        if best_solution_objective == None or new_objective < best_solution_objective:
            best_solution = new_solution
            best_solution_objective = new_objective

        k = k + 1

    # print('Best Solution Cost --> ', best_solution_objective, 'k: ', k)
        
                
        #LIST_OF_SOLUTIONS.append(new_cost)
        #LIST_OF_BEST.append(best_solution_cost)
        
    # record_solutions(solutions=LIST_OF_SOLUTIONS, best=LIST_OF_BEST, suf='_solution.csv')
    # record_solutions(solutions=LIST_OF_BEST, suf='_best.csv')

    return best_solution, best_solution_objective





# Gravar soluções em arquivo
def record_solutions(solutions):
    
    with open('saidas/GP-SA/' + str(configus) + '_solution.csv', 'w') as file:
        file.write('Solution\n')
    
    with open('saidas/GP-SA/' + str(config.us) + '_solution.csv', 'a') as file:
        for item in solutions:
            file.write(str(item) + '\n')
                
if __name__ == '__main__':
    
    start = time.time()
    
    EULER = 2.718281828459
    temperature = 1000
    alpha = 0.98
    iterations_each_temperature = 5
    number_iterations_solution_is_not_improved = 5
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

    final_solution, final_objective= GRASP(dict_BIPs, temperature)
    
    #for item in final_solution:
    #    print(item)
    final = time.time()
    
    print('Time: ', final-start)
    print('Solution: ', final_objective)
    
    with open('saidas/grasp_sa.txt', 'a') as file:
        file.write("{:.5f}".format(final_objective) + ' ' + str(final-start) + '\n')
    
    
    
    
            
    
    
    
    
    
    