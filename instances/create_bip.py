import json
import random as rd

users = 225
time = 10
base_stations = 5

def create_bip():
    bip = {}
    
    for t in range(1, time+1):
        for us in range(1, users+1):
            for bsUL in range(1, base_stations+1):
                for bsDL in range(1, base_stations+1):
                    bip_calculation = rd.uniform(10, 100)
                    bip['t' + str(t) + '_u' + str(us) + '_bsUL' + str(bsUL) + '_bsDL' + str(bsDL)] = bip_calculation
                    
                    
    with open(str(users) + '/BIP_for_all_combinations.json', 'w') as json_file:
        json.dump(bip, json_file, indent=4)
                    

if __name__ == '__main__':
    create_bip()