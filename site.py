import streamlit as st
import pandas as pd
import numpy as np
import random 
from scipy.stats import poisson

st.title('Prevendo o campeonato brasilerio')

clube = pd.read_excel('C:/Users/User/Desktop/trabalho/times.xlsx', sheet_name = 'clube', index_col = 0)

fifa = clube['PontosRankingFIFA']
a, b = min(fifa), max(fifa) 
fa, fb = 0.15, 1 
b1 = (fb - fa)/(b-a) 
b0 = fb - b*b1
forca = b0 + b1*fifa 

def Resultado(gols1, gols2):
    if gols1 > gols2:
        res = 'V'
    if gols1 < gols2:
        res = 'D' 
    if gols1 == gols2:
        res = 'E'       
    return res

def MediasPoisson(clube1, clube2):
    forca1 = forca[clube1]
    forca2 = forca[clube2] 
    mgols = 2.75
    l1 = mgols*forca1/(forca1 + forca2)
    l2 = mgols*forca2/(forca1 + forca2)
    return [l1, l2]
    
def Distribuicao(media):
    probs = []
    for i in range(7):
        probs.append(poisson.pmf(i,media))
    probs.append(1-sum(probs))
    return pd.Series(probs, index = ['0', '1', '2', '3', '4', '5', '6', '7+'])

def ProbabilidadesPartida(clube1, clube2):
    l1, l2 = MediasPoisson(clube1, clube2)
    d1, d2 = Distribuicao(l1), Distribuicao(l2)  
    matriz = np.outer(d1, d2)    #   Monta a matriz de probabilidades

    vitoria = np.tril(matriz).sum()-np.trace(matriz)    #Soma a triangulo inferior
    derrota = np.triu(matriz).sum()-np.trace(matriz)    #Soma a triangulo superior
    probs = np.around([vitoria, 1-(vitoria+derrota), derrota], 3)
    probsp = [f'{100*i:.1f}%' for i in probs]

    nomes = ['0', '1', '2', '3', '4', '5', '6', '7+']
    matriz = pd.DataFrame(matriz, columns = nomes, index = nomes)
    matriz.index = pd.MultiIndex.from_product([[clube1], matriz.index])
    matriz.columns = pd.MultiIndex.from_product([[clube2], matriz.columns]) 
    output = {'clube1': clube1, 'clube2': clube2, 
             'f1': forca[clube1], 'f2': forca[clube2], 
             'media1': l1, 'media2': l2, 
             'probabilidades': probsp, 'matriz': matriz}
    return output

def Pontos(gols1, gols2):
    rst = Resultado(gols1, gols2)
    if rst == 'V':
        pontos1, pontos2 = 3, 0
    if rst == 'E':
        pontos1, pontos2 = 1, 1
    if rst == 'D':
        pontos1, pontos2 = 0, 3
    return pontos1, pontos2, rst


def Jogo(clube1, clube2):
    l1, l2 = MediasPoisson(clube1, clube2)
    gols1 = int(np.random.poisson(lam = l1, size = 1))
    gols2 = int(np.random.poisson(lam = l2, size = 1))
    saldo1 = gols1 - gols2
    saldo2 = -saldo1
    pontos1, pontos2, result = Pontos(gols1, gols2)
    placar = '{}x{}'.format(gols1, gols2)
    return [gols1, gols2, saldo1, saldo2, pontos1, pontos2, result, placar]

######## COMEÇO DO APP


st.markdown("# 🏆 Campeonato brasileiro 2022") 

st.markdown("## ⚽ Probabilidades das Partidas")
st.markdown('---')

listaclube1 = clube.index.tolist()  
listaclube1.sort()
listaclube2 = listaclube1.copy()

j1, j2 = st.columns(2)
clube1 = j1.selectbox('Escolha o primeiro clube', listaclube1) 
listaclube2.remove(clube1)
clube2 = j2.selectbox('Escolha o segundo clube', listaclube2, index = 1)
st.markdown('---')

jogo = ProbabilidadesPartida(clube1, clube2)
prob = jogo['probabilidades']
matriz = jogo['matriz']

col1, col2, col3, col4, col5 = st.columns(5)
col1.image(clube.loc[clube1, 'LinkBandeiraGrande'])  
col2.metric(clube1, prob[0])
col3.metric('Empate', prob[1])
col4.metric(clube2, prob[2]) 
col5.image(clube.loc[clube2, 'LinkBandeiraGrande'])

st.markdown('---')
st.markdown("## 📊 Probabilidades dos Placares") 

def aux(x):
	return f'{str(round(100*x,1))}%'
st.table(matriz.applymap(aux))


st.markdown('---')
st.markdown("## 🌍 Probabilidades dos Jogos do campeonato brasileiro")