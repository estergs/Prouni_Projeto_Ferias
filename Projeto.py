from email import charset
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


#importando todas as bases( dos últimos 10 anos disponiíveis)
df10 = pd.read_csv ('pda-prouni-2010.csv',sep=';', encoding='ISO-8859-1')
df11 = pd.read_csv ('pda-prouni-2011.csv',sep=';', encoding='ISO-8859-1')
df12 = pd.read_csv ('pda-prouni-2012.csv',sep=';', encoding='ISO-8859-1')
df13 = pd.read_csv ('pda-prouni-2013.csv',sep=';', encoding='ISO-8859-1')
df14 = pd.read_csv ('pda-prouni-2014.csv',sep=';', encoding='ISO-8859-1')
df15 = pd.read_csv ('pda-prouni-2015.csv',sep=';', encoding='ISO-8859-1')
df16 = pd.read_csv ('pda-prouni-2016.csv',sep=';', encoding='ISO-8859-1')
df17 = pd.read_csv ('pda-prouni-2017.csv',sep=';', encoding='UTF-8') # esse é diferente
df18 = pd.read_csv ('pda-prouni-2018.csv',sep=';', encoding='UTF-8')
df19 = pd.read_csv ('pda-prouni-2019.csv',sep=';', encoding='UTF-8')
df20 = pd.read_csv ('pda-prouni-2020.csv',sep=';', encoding='ISO-8859-1')


#Criando Listas pra facilitar os procedimentos 
lista_dfs = [df10,df11,df12,df13,df14,df15,df16,df17,df18,df19,df20]

# usei o concat pra juntar todas as bases em uma só, e logo em seguida, troquei a coluna ano pra int, antes estava como float
df= pd.concat(lista_dfs, ignore_index=True)
df['ANO_CONCESSAO_BOLSA'] = df['ANO_CONCESSAO_BOLSA'].astype('Int64')

#Tratando a base os nomes das colunas estão divergentes

df['Sexo'] = df['SEXO_BENEFICIARIO'].combine_first(df['SEXO_BENEFICIARIO_BOLSA'])
df['Raca'] = df['RACA_BENEFICIARIO'].combine_first(df['RACA_BENEFICIARIO_BOLSA'])
df['UF'] = df['UF_BENEFICIARIO'].combine_first(df['SIGLA_UF_BENEFICIARIO_BOLSA'])
df['Municipio'] = df['MUNICIPIO_BENEFICIARIO'].combine_first(df['MUNICIPIO_BENEFICIARIO_BOLSA'])
df['Municipio'] = df['Municipio'].combine_first(df['MUNICIPIO'])
df['Regiao'] = df['REGIAO_BENEFICIARIO'].combine_first(df['REGIAO_BENEFICIARIO_BOLSA'])

# Eliminando as colunas duplicadas antigas e obsoletas
df.drop(columns=[
    'CPF_BENEFICIARIO', 'CPF_BENEFICIARIO_BOLSA',
    'DATA_NASCIMENTO', 'DT_NASCIMENTO_BENEFICIARIO',
    'SEXO_BENEFICIARIO', 'SEXO_BENEFICIARIO_BOLSA',
    'RACA_BENEFICIARIO', 'RACA_BENEFICIARIO_BOLSA',
    'UF_BENEFICIARIO', 'SIGLA_UF_BENEFICIARIO_BOLSA',
    'MUNICIPIO', 'MUNICIPIO_BENEFICIARIO','MUNICIPIO_BENEFICIARIO_BOLSA',
    'REGIAO_BENEFICIARIO', 'REGIAO_BENEFICIARIO_BOLSA'
], inplace=True)

# Renomeando as outras colunas pra facilitar
df = df.rename(columns={
    # Padronização de ano
    'ANO_CONCESSAO_BOLSA': 'Ano',

    # IES
    'CODIGO_EMEC_IES_BOLSA': 'Codigo_IES',
    'NOME_IES_BOLSA': 'Nome_IES',
    
    # Curso
    'CAMPUS': 'Campus',
    'TIPO_BOLSA': 'Tipo_Bolsa',
    'MODALIDADE_ENSINO_BOLSA': 'Modalidade',
    'NOME_CURSO_BOLSA': 'Curso',
    'NOME_TURNO_CURSO_BOLSA': 'Turno',

    # Beneficiário
    'BENEFICIARIO_DEFICIENTE_FISICO': 'Deficiencia'
})

df['Tipo_Bolsa'] = df['Tipo_Bolsa'].replace({
    'BOLSA INTEGRAL': 'INTEGRAL',
    'INTEGRAL': 'INTEGRAL',
    'BOLSA PARCIAL 50%': 'PARCIAL',
    'PARCIAL': 'PARCIAL'
})

#Criei uma coluna auxiliar pra me ajudar a fazer os agrupamentos
df['Cont'] = 1

# Padronizando o texto
df['Curso'] = df['NOME_CURSO_BOLSA'].str.title().str.strip()

# Evolução do numero de bolsa________________________________________________
df_bolsa = df.groupby('Ano')['Cont'].sum().reset_index()

#gráfico
plt.plot(df_bolsa['Ano'],df_bolsa['Cont'])
plt.title('\nEvolução Concessão de bolsa\n')
plt.xlabel('\nAno\n')
plt.ylabel('\nConcessão de bolsa\n')
plt.grid(True)
plt.show

# Distribuição por tipo de bolsa_____________________________________________
df_tipo_bolsa= df.groupby('Tipo_Bolsa')['Cont'].sum().reset_index()

# Cursos Mais procurados_____________________________________________________ 
df_curso = df.groupby('Curso')['Cont'].sum().reset_index()
df_curso = df_curso.sort_values(by='Cont', ascending=False)

# Distribuiçnao por municipio________________________________________________            
df_muni = df.groupby('Municipio')['Cont'].sum().reset_index()
df_muni = df_muni.sort_values(by='Cont', ascending=False)