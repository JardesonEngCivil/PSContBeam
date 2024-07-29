from software.Executor.run         import  DictProcessado
from software.Executor.leitura_arq import leitura_dados
from software.Plotagem.tensao       import Tensao
from software.Forca_nodais.Cargas_nodais import MomentosNodais
from software.Reacoes.Esforcos import Esforcos
from software.exemplos.tensoes_vpro import inflexao
import matplotlib.pyplot as plt
import matplotlib.ticker  as tk
from software.exemplos.tensoes_vpro import inflexao

inf = "ex_vpro.json"
#leitura do arquivo.json 
#dados = leitura_dados(inf)
#d = DictProcessado(dados, size = 1, c_externo= False)
##mnodal = MomentosNodais(dados[0], dados[1])
#print(mnodal.m)
#hiper = Esforcos(mnodal, dados[2], dados[3]).hiperestatico()
#print([round(i,4) for i in hiper])
# tensao = Tensao(d)
# tensao.verific_sup()





dados = leitura_dados(inf)
d = DictProcessado(dados, size = .5, c_externo= True)

plt.rc('font', family='Times New Roman')
tqs = "TQS VPRO"
py  = "PYTHON"
plan = "PLANILHA"
sigma = '\u03c3'

tensao = Tensao(d)
#tensao.verific_inf()
plt.style.use('bmh')
ato = tensao.elu_ato()
f   = tensao.els_f()
d   = tensao.els_d()

