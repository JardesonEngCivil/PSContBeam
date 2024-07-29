import numpy as np
import matplotlib.pyplot  as plt
import matplotlib.ticker  as tk

x= np.array([0,0.833,	1.667,	2.5,	3.333,	4.167,	5,	5.833	,6.667,	7.5	,8.333	,9.167,10,	10.833,
              	11.667,	12.5,	13.333,	14.167,	15,	15.833,	16.667,17.5,	18.333,	19.167,	20,	20.833,
                    	21.667,22.5,	23.333,	24.167,	25,	25.833,	26.667,	27.5,	28.333,	29.167,	30])

f0 = np.array([97.66,	97.52,	97.22,	95.41,	93.76,	92.58,	90.47,	86.78,	82.92,	
            78.7,	74.77,	71.04,	68.14,	65.56,	63.75,	62.16,	60.26, 58.31,	56.47,
            	54.74,	53.22,	51.72,	50.4,	48.96,	47.24,	45.23,	43.06,	40.83,	38.58,
                	36.85,	35.47,	34.78,	34.33,	33.7,	33.07,	32.95,	32.9])

finf = np.array([90.98, 90.88, 90.65,	89.26, 87.99, 87.11, 85.55,	82.76, 79.75, 76.41, 73.28,
        70.26, 67.87, 65.56, 63.75,	62.16, 60.26, 58.31, 56.47,	54.74, 53.22, 51.72, 50.4,
        48.96, 47.24, 45.23, 43.06, 40.83, 38.58, 36.85, 35.47,	34.78, 34.33, 33.7,	33.07, 32.95,32.9])
plt.style.use("bmh")
plt.rc('font', family='Times New Roman')
#prop={ 'family': 'Times New Roman'}
fig, (right, left) = plt.subplots(nrows= 1, ncols= 2)

right.set_xlabel("Comprimento (m)")
right.set_ylabel("P (tf)")
right.set_title("FORÇA DE PROTENSÃO EM T = 0")
right.plot(x, f0, "g")
#right.plot(x, finf, "r")  
right.grid(True, which='both', axis='both', color='gray', linestyle='--', linewidth=0.5, alpha=0.5)

#right.legend(loc="lower right")
#right.set_ylim(-3.5, 2.5)
#right.yaxis.set_minor_locator(tk.MultipleLocator(.5))
#right.grid()

left.set_xlabel("Comprimento (m)")
left.set_ylabel("P (tf)")
left.set_title("FORÇA DE PROTENSÃO EM T = "+ "\u221e")
left.plot(x, finf, "r")    

#left.legend(loc="upper right")
#right.set_ylim(-5, 2)
#right.yaxis.set_minor_locator(tk.MultipleLocator(.5))
left.grid(True, which='both', axis='both', color='gray', linestyle='--', linewidth=0.5, alpha=0.5)



plt.show()