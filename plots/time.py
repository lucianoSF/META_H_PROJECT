import pandas as pd
import matplotlib.pyplot as plt 


#things = '80'
#df = pd.read_csv('../saidas/SA/' + things + '_solution.csv', sep=';')

def read_data(file_name):
    data = []
    # Using readlines()
    file = open(file_name, 'r')
    lines = file.readlines()

    count = 0
    
    for line in lines:
        count += 1
        data.append(float(line.strip().split()[1]))
        
    return data

if __name__ == "__main__":
    timeOpt = read_data('../saidas/model.txt')
    timeSA = read_data('../saidas/grasp_sa.txt')
    timeGA = read_data('../saidas/ga_grasp.txt')

    x = [30, 60, 90, 120, 150, 180, 210, 240, 270, 300]
    fig,ax = plt.subplots()

    fig.set_size_inches(10, 4.5)
    ax.plot(x, timeOpt, "-o", label="Solução ótima - ILP", linewidth=2.0, markersize=12, color='#006bb3')
    ax.plot(x, timeSA, "-^", label="GRASP+SA", linewidth=2.0, markersize=12, color='red')
    ax.plot(x, timeGA, "-v", label="GA+GRASP", linewidth=2.0, markersize=12, color='green')
    
    ax.set_xlabel("Numero de usuários", fontsize=20, labelpad=8)
    ax.set_ylabel("tempo (s)",fontsize=20)

    ax.set_xticks(x)
    ax.set_xticklabels(x, fontsize=20)

    ticks = [0, 1000, 2000, 3000, 4000]
    
    '''
    for i,j,l  in zip(timeOpt,timeSA,x):
        #print(x, y)
        labelI = "{:.2f}s".format(i)
        labelJ = "{:.2f}s".format(j)

        ax.annotate(labelI, # this is the text
                     (l,i), # these are the coordinates to position the label
                     textcoords="offset points", # how to position the text
                     xytext=(0,10), # distance from text to points (x,y)
                     ha='center') # horizontal alignment can be left, right or center
        
        ax.annotate(labelJ, # this is the text
                     (l,j), # these are the coordinates to position the label
                     textcoords="offset points", # how to position the text
                     xytext=(0,10), # distance from text to points (x,y)
                     ha='center') # horizontal alignment can be left, right or center
    '''    
    ax.set_yticks(ticks)
    ax.set_yticklabels(ticks, fontsize=20)

    ax.legend(fontsize=18)
    ax.grid(axis='y', which='major', linestyle='--')
    plt.savefig("time.pdf", bbox_inches='tight')
    plt.savefig("time.png", bbox_inches='tight')
    #plt.show()