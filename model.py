from docplex.mp.model import Model
import json
import sys
from classes.Config import Config
from classes.Users import Users
from classes.BaseStation import BaseStation
from classes.BIP import BIP
import time

bip = BIP()

config = Config()

def load_users():
    users = {}
    with open(config.users_file) as json_file:
        data = json.load(json_file)
        data = data['users']
        
        for i in range(0, config.us):
            x = {}
            y = {}
            height = {}
            orientation = {}
            ang_azim = {}
            for j in range(0, config.ti):
                x[j+1] = data[i]['coordinates_by_time'][j]['x']
                y[j+1] = data[i]['coordinates_by_time'][j]['y']
                height[j+1] = data[i]['coordinates_by_time'][j]['height_cm']
                orientation[j+1] = data[i]['coordinates_by_time'][j]['orientation']
                ang_azim[j+1] = data[i]['coordinates_by_time'][j]['ang_azim']
            
            users[i+1] = Users(data[i]['id'], x, y, height, orientation, ang_azim)
            
        return users
    
def load_base_stations():
    base_stations = {}
    with open(config.bs_file) as json_file:
        data = json.load(json_file)
        data = data['bs']
        
        for i in range(1, config.bs+1):
            base_stations[i] = BaseStation(data[str(i)]['id'],
                                           data[str(i)]['x'],
                                           data[str(i)]['y'],
                                           data[str(i)]['height_cm'])
            
        return base_stations

    
def solve_model():
    mdl = Model(name='xr-fed-esl', log_output=True)
    
    users = load_users()
    bs = load_base_stations()
    
    i = [(u, b, t) for u in users for b in bs for t in range(1, config.ti+1)]
    
    mdl.a_ul = mdl.binary_var_dict(keys=i, name='a_ul')
    mdl.a_dl = mdl.binary_var_dict(keys=i, name='a_dl')
    
    with open(config.decisions_file) as json_file:
        dict_BIPs = json.load(json_file)
        
    objective = mdl.sum(mdl.sum(mdl.a_ul[it1]*mdl.a_dl[it2]*dict_BIPs['t' + str(t) + '_u' + str(it1[0]) + '_bsUL' + str(it1[1]) + '_bsDL' + str(it2[1])] 
                        for it1 in i for it2 in i if it1[0] == it2[0] and it1[2] == it2[2] and t == it1[2]) for t in range(1, config.ti+1))/config.ti
    
    mdl.minimize(objective)
    
    for u in users:
        for t in range(1, config.ti+1):
            mdl.add_constraint(mdl.sum(mdl.a_ul[it] for it in i if it[0] == u and it[2] == t) == 1, 'just one bs for ul')
            mdl.add_constraint(mdl.sum(mdl.a_dl[it] for it in i if it[0] == u and it[2] == t) == 1, 'just one bs for dl')
            
            
    for b in bs:
        for t in range(1, config.ti+1):
            mdl.add_constraint(mdl.sum(mdl.a_dl[it] for it in i if it[1] == b and it[2] == t) <= config.V, 'BS users limit')
    #mdl.export_as_lp('model.lp')
    mdl.solve()
    

    results = {'users':{}}
    for item in users:
        results['users'][item] = {}
        for item2 in range(1, config.ti+1):
            results['users'][item]['t_' + str(item2)] = {'Uplink':None, 'Downlink':None}
    
    for it in i:
        if mdl.a_ul[it].solution_value > 0:
            results['users'][it[0]]['t_' + str(it[2])]['Uplink'] = it[1]
            #print("a_ul{} -> {}".format(it, mdl.a_ul[it].solution_value))
        if mdl.a_dl[it].solution_value > 0:
            results['users'][it[0]]['t_' + str(it[2])]['Downlink'] = it[1]
            #print("a_dl{} -> {}".format(it, mdl.a_dl[it].solution_value))
        
    with open(config.results_file, 'w') as json_file:
        json.dump(results, json_file, indent=4)
        
    return mdl.solution.get_objective_value()
    
    

if __name__ == '__main__':
    start = time.time()
    obj = solve_model()
    final = time.time()
    print('Time: ', final-start)
    print('Solution: ', obj)
    
    with open('outputs/model.txt', 'a') as file:
        file.write("{:.5f}".format(obj) + ' ' + str(final-start) + '\n')