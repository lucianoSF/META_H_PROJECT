import pandas as pd
import matplotlib.pyplot as plt 
import ast

users = '300'
df = pd.read_csv('../saidas/GA/' + users + '_solution.csv', sep=';')

print(df)

y_sep = df['Pop']


y = []
x = []
ind = 1
for item in y_sep:
    list_of_obj = ast.literal_eval(item)
    y = y + list_of_obj
    x = x + [ind]*len(list_of_obj)
    ind = ind + 1


y_best = df['Best']

x_best = list(range(1, len(y_best)+1))


fig,ax = plt.subplots()

fig.set_size_inches(6, 4)
ax.plot(x, y, ".", label="Complete model", linewidth=2.0, markersize=12, color='#006bb3')
ax.plot(x_best, y_best, ".", label="Complete model", linewidth=2.0, markersize=12, color='red')
#ax.set_ylim(400,500)

ax.set_xlabel("Iteração", fontsize=24, labelpad=8)
ax.set_ylabel("FO",fontsize=24)

xticks = [0, 25, 50,75,100]
#xticks = [0, 250, 500, 750, 1000]
ax.set_xticks(xticks)
ax.set_xticklabels(xticks, fontsize=10)



#yticks = [3000, 7000, 12000, 16000, 22000]

#yticks = [1000, 3000, 5000, 7000, 9000, 11000, 13000]

#yticks = [0, 100, 10000, 15000, 20000, 25000, 30000]

#yticks = [0, 15000, 25000, 35000, 45000,55000]

#yticks = [1400, 1500, 1600, 1700, 1800]
#ax.set_yticks(yticks)
#ax.set_yticklabels(yticks, fontsize=22)
#tkw = dict(size=4, width=1.5)
#ax.tick_params(axis='y', **tkw, labelsize=22)

ax.set_title(users + ' usuários', fontsize=22)
#ax.tick_params(axis='x', **tkw, labelsize=16)

ax.grid(b=True, which='major', linestyle='--')

plt.savefig(users + "_pop.pdf", bbox_inches='tight')
plt.savefig(users + "_pop.png", bbox_inches='tight')

#plt.show()