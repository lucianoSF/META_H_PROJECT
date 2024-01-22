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
        data.append(float(line.strip().split()[0]))
        
    return data

if __name__ == "__main__":
    timeOpt = read_data('../saidas/model.txt')
    timeSA = read_data('../saidas/grasp_sa.txt')
    timeGA = read_data('../saidas/ga_grasp.txt')
    
    x = [30, 60, 90, 120, 150, 180, 210, 240, 270, 300]
    fig,ax = plt.subplots()
    
    print(len(timeSA))

    fig.set_size_inches(10, 4.5)
    ax.plot(x, timeOpt, "-o", label="Solução ótima - ILP", linewidth=2.0, markersize=12, color='#006bb3')
    ax.plot(x, timeSA, "-^", label="GRASP+SA", linewidth=2.0, markersize=12, color='red')
    ax.plot(x, timeGA, "-v", label="GA+GRASP", linewidth=2.0, markersize=12, color='green')
    
    ax.set_xlabel("Numero de usuários", fontsize=20, labelpad=8)
    ax.set_ylabel("Break in Presence",fontsize=20)

    ax.set_xticks(x)
    ax.set_xticklabels(x, fontsize=20)

    ticks = [0, 2000, 4000, 6000, 8000, 10000, 12000, 14000]

    for i,j,l  in zip(timeOpt,timeSA,x):

        gap = (1-(i/j))*100

        label = "{:.2f}%".format(gap)
        if l == 300:
            ax.annotate(label, (l,i), textcoords="offset points", xytext=(0,-20), ha='center', color='red')
            ax.annotate("*",(l,i), textcoords="offset points", xytext=(0,-40), ha='center', fontsize=20, color='red') 
        else:
            ax.annotate(label, (l,i), textcoords="offset points", xytext=(0,10), ha='center', color='red')  
            
            
            
    for i,j,l  in zip(timeOpt,timeGA,x):

        gap = (1-(i/j))*100

        label = "{:.2f}%".format(gap)
        if l == 300:
            ax.annotate(label, (l,j), textcoords="offset points", xytext=(0,-20), ha='center', color='green')
            ax.annotate("*",(l,j), textcoords="offset points", xytext=(0,-40), ha='center', fontsize=20, color='green') 
        else:
            ax.annotate(label, (l,j), textcoords="offset points", xytext=(0,20), ha='center', color='green')
            
     
    ax.set_yticks(ticks)
    ax.set_yticklabels(ticks, fontsize=20)

    ax.legend(fontsize=18)
    ax.grid(axis='y', which='major', linestyle='--')
    plt.savefig("obj.pdf", bbox_inches='tight')
    plt.savefig("obj.png", bbox_inches='tight')
    #plt.show()