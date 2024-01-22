import pandas as pd
import matplotlib.pyplot as plt 


things = '80'
df = pd.read_csv('../saidas/SA/' + things + '_solution.csv', sep=';')



y = df['Solution']
x = list(range(1, len(y)+1))

fig,ax = plt.subplots()

fig.set_size_inches(6, 4)
ax.plot(x, y, "-", label="Complete model", linewidth=2.0, markersize=12, color='#006bb3')

#ax.set_ylim(400,500)

ax.set_xlabel("Iteração", fontsize=24, labelpad=8)
ax.set_ylabel("Valor total",fontsize=24)

xticks = [0, 1500, 3000,4500, 6000]
#xticks = [0, 250, 500, 750, 1000]
ax.set_xticks(xticks)
ax.set_xticklabels(xticks, fontsize=22)



#yticks = [3000, 7000, 12000, 16000, 22000]

#yticks = [1000, 3000, 5000, 7000, 9000, 11000, 13000]

#yticks = [0, 100, 10000, 15000, 20000, 25000, 30000]

#yticks = [0, 15000, 25000, 35000, 45000,55000]

yticks = [1200, 2000,2800, 3600, 4400,]
ax.set_yticks(yticks)
ax.set_yticklabels(yticks, fontsize=22)
#tkw = dict(size=4, width=1.5)
#ax.tick_params(axis='y', **tkw, labelsize=22)

ax.set_title('KSP '+ things + ' itens', fontsize=22)
#ax.tick_params(axis='x', **tkw, labelsize=16)

ax.grid(b=True, which='major', linestyle='--')

plt.savefig(things + ".pdf", bbox_inches='tight')
plt.savefig(things + ".png", bbox_inches='tight')

#plt.show()