import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# links 

file_id10 = '1GlXcIkS3K3hvP6dFsVZMun4pMTuBJnqb' 
url10 = f'https://drive.google.com/uc?export=download&id={file_id10}'

file_id11 = '1AMZRm7jFOCtGrcHKSDU67rS9V2DZUE4t' 
url11 = f'https://drive.google.com/uc?export=download&id={file_id11}'

file_id12 = '1kqY4RaUPNwZMFYlewF5k_M9131WdKcE-' 
url12 = f'https://drive.google.com/uc?export=download&id={file_id12}'

file_id13 = '1P9LnCmvX15LfHbdQ1rZQ_6V19eRobBr7' 
url13 = f'https://drive.google.com/uc?export=download&id={file_id13}'

file_id14 = '18uaJARuPpA3p308l2NcZm55saLURIpTO' 
url14 = f'https://drive.google.com/uc?export=download&id={file_id14}'

file_id15 = '1RHPGVVmG2qRekAwysHvmnJvAXn0qmH5J' 
url15 = f'https://drive.google.com/uc?export=download&id={file_id15}'

file_id16 = '1LVwvD3GrUF6qFAKW4w9RnsrIDMJ9soNq' 
url16 = f'https://drive.google.com/uc?export=download&id={file_id16}'

file_id17 = '1h0b_jzFAMbjgQzQ9s1reZGgbXTThPcPr' 
url17 = f'https://drive.google.com/uc?export=download&id={file_id17}'

file_id18 = '14goWMFuD76M5P-SavPIxI8B_WiXgrnd9' 
url18 = f'https://drive.google.com/uc?export=download&id={file_id18}'

file_id19 = '1ArTa_67aIf5w0wC6tZ5PVq7lJAMXYZX2'
url19 = f'https://drive.google.com/uc?export=download&id={file_id19}'

file_id20 = '1ey7pDu2uTkfn0Jr0fhBJwACk_uP1lXd2' 
url20 = f'https://drive.google.com/uc?export=download&id={file_id20}'

#importando todas as bases( dos últimos 10 anos disponiíveis)
df10 = pd.read_csv (url10,sep=';', encoding='ISO-8859-1')
df11 = pd.read_csv (url11,sep=';', encoding='ISO-8859-1')
df12 = pd.read_csv (url12,sep=';', encoding='ISO-8859-1')
df13 = pd.read_csv (url13,sep=';', encoding='ISO-8859-1')
df14 = pd.read_csv (url14,sep=';', encoding='ISO-8859-1')
df15 = pd.read_csv (url15,sep=';', encoding='ISO-8859-1')
df16 = pd.read_csv (url16,sep=';', encoding='ISO-8859-1')
df17 = pd.read_csv (url17,sep=';', encoding='UTF-8') 
df18 = pd.read_csv (url18,sep=';', encoding='UTF-8')
df19 = pd.read_csv (url19,sep=';', encoding='UTF-8')
df20 = pd.read_csv (url20,sep=';', encoding='ISO-8859-1')

lista_dfs = [df10,df11,df12,df13,df14,df15,df16,df17,df18,df19,df20]

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
df['Modalidade'] = df['Modalidade'].replace({
    'EDUCAÇÃO A DISTÂNCIA': 'EAD',
    'PRESENCIAL': 'Presencial',

})

#Criei uma coluna auxiliar pra me ajudar a fazer os agrupamentos
df['Cont'] = 1

# Padronizando o texto
df['Curso'] = df['Curso'].str.title().str.strip()

# Evolução do numero de bolsa________________________________________________
df_bolsa = df.groupby('Ano')['Cont'].sum().reset_index()

#exportando pra csv
df_bolsa.to_csv('evolucao_bolsa.csv', index=False)

'''#gráfico
plt.plot(df_bolsa['Ano'],df_bolsa['Cont'])
plt.title('\nEvolução Concessão de bolsa\n')
plt.xlabel('\nAno\n')
plt.ylabel('\nConcessão de bolsa\n')
plt.grid(True)
plt.show'''

# Distribuição por tipo de bolsa_____________________________________________
df_tipo_bolsa= df.groupby('Tipo_Bolsa')['Cont'].sum().reset_index()
df_tipo_bolsa

#exportando pra csv
df_tipo_bolsa.to_csv('tipo_bolsa.csv', index=False)

'''#grafico
df_tipo_bolsa.plot(kind= 'barh', x = 'Tipo_Bolsa', y= 'Cont')
plt.title('\nDistribuição por tipo de bolsa\n')
plt.xlabel('\nTipo de Bolsa\n')
plt.ylabel('\nQuantidade\n')
plt.xlim(0, 2000000) 
plt.show'''

# Cursos Mais procurados_____________________________________________________ 
df_curso = df.groupby('Curso')['Cont'].sum().reset_index()
df_curso = df_curso.sort_values(by='Cont', ascending=False).head(10)

#exportando pra csv
df_curso.to_csv('Cursos_mais_procurados.csv', index=False)

'''df_curso.plot(kind= 'barh', x = 'Curso', y= 'Cont')
plt.title('\nCursos mais procurados\n')
plt.xlabel('\nCurso\n')
plt.ylabel('\nQuantidade\n')
plt.xlim(0, 400000) 
plt.show'''

# Distribuiçao por municipio________________________________________________            
df_muni = df.groupby('Municipio')['Cont'].sum().reset_index()
df_muni = df_muni.sort_values(by='Cont', ascending=False).head(10)

#exportando pra csv
df_muni.to_csv('Municipios.csv', index=False)

'''df_muni.plot(kind= 'barh', x = 'Municipio', y= 'Cont')
plt.title('\nDistribuição por tipo de bolsa\n')
plt.xlabel('\nMunicípio\n')
plt.ylabel('\nQuantidade\n')
plt.show'''

# Universidades que compoem as 25% com mais bolsas ____________________________
df_uni= df.groupby('Nome_IES')['Cont'].sum().reset_index()
dados_uni= np.array(df_uni['Cont'])
q3= np.percentile(dados_uni,75)

maior_uni_25= df_uni.loc[df_uni['Cont'] >= q3]
maior_uni_25= maior_uni_25.sort_values('Cont', ascending=False).head(10)

#exportando pra csv
maior_uni_25.to_csv('Cursos_mais_procurados.csv', index=False)

'''# gráfico 
maior_uni_25.plot(kind= 'barh', x = 'Nome_IES', y= 'Cont')
plt.title('\nUniversidades que concedem mais bolsas\n')
plt.xlabel('\nQuantidade\n')
plt.ylabel('\nUniversidade de Bolsas\n')
plt.show'''

# Impacto da Digitalização na Modalidade de Ensino _______________________________________________________________

df_modalidade = df.groupby(['Ano', 'Modalidade']).size().reset_index(name='Cont')
df_total_ano = df_modalidade.groupby('Ano')['Cont'].transform('sum')

df_modalidade['Porcentagem'] = (df_modalidade['Cont'] / df_total_ano) * 100 # adicionando uma coluna de porcentagem pra cada modalidade
df_modalidade['Porcentagem'] = df_modalidade['Porcentagem'].round(2) # arredondando 

#exportando pra csv
df_modalidade.to_csv('Modalidade.csv', index=False)

# evolução da Porcentagem de Bolsas EAD 

df_ead = df_modalidade[df_modalidade['Modalidade'] == 'EAD']
df_ead = df_ead.sort_values(by='Ano')

'''#gráfico
plt.plot(df_ead['Ano'],df_ead['Porcentagem'])
plt.title('\nEvolução da Porcentagem de Bolsas EAD \n')
plt.xlabel('\nAno\n')
plt.ylabel('\nPorcentagem\n')
plt.grid(True)
plt.show
'''
# evolução da Porcentagem de Bolsas Presenciais

df_presencial = df_modalidade[df_modalidade['Modalidade'] == 'Presencial']
df_presencial = df_presencial.sort_values(by='Ano')

'''#gráfico
plt.plot(df_presencial['Ano'],df_presencial['Porcentagem'])
plt.title('\nEvolução da Porcentagem de Bolsas Presencial \n')
plt.xlabel('\nAno\n')
plt.ylabel('\nPorcentagem\n')
plt.grid(True)
plt.show'''







