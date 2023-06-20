#! pip install -r requirements.txt

# Importar bibliotecas
import csv
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np


class CondicionamentoPre20:
    """
    Classe que recebe como argumento uma lista e cria os parâmetros correspondentes
    ao cabeçalho dos ficheiros sobre condicionamentos de trânsito da Câmara Municipal de Lisboa.

    A classe aceita os ficheiros de 2018 e 2019.
    """
    def __init__(self, lista=list):
        self.entity_id = lista[0]
        self.impacto = lista[1]
        self.rest = lista[2]
        self.morada = lista[3]
        self.cond = lista[4].split(',')
        self.motivo = lista[5]
        self.position = lista[6]
        self.creation = lista[7]
        self.end_date = float(self.cond[0][15:-1])
        self.start_date = float(self.cond[5][16:-3])

    def periodo_cond(self):
        """
        Método da classe que calcula a diferença, em horas, entre o início e o fim do condicionamento do objeto.

        O método utiliza os parâmetros self.end_date e self.start_date, criados na inicialização da classe, e retorna
        o resultado do cálculo a dividir por 3.600, que transforma segundos em horas com o módulo datetime.
        """
        horas = datetime.fromtimestamp(self.end_date / 1000) - datetime.fromtimestamp(self.start_date / 1000)
        diferenca = horas.total_seconds() / 3600
        return round(diferenca)


class CondicionamentoPos20:
    """
    Classe que recebe como argumento uma lista e cria os parâmetros correspondentes
    ao cabeçalho dos ficheiros sobre condicionamentos de trânsito da Câmara Municipal de Lisboa.

    A classe aceita os ficheiros de 2020 e 2021, após alterações na estrutura do ficheiro padrão.
    """
    def __init__(self, lista=list):
        self.entity_id = lista[0]
        self.impacto = lista[1]
        self.rest = lista[2]
        self.morada = lista[3]
        self.cond = lista[4].split(',')
        self.motivo = lista[5]
        self.position = lista[6]
        self.creation = lista[7]
        self.end_date = self.cond[0][15:-1]
        self.start_date = self.cond[4][16:-1]

    def periodo_cond(self):
        """
        Método da classe que calcula a diferença, em horas, entre o início e o fim do condicionamento do objeto.

        O método utiliza os parâmetros self.end_date e self.start_date, criados na inicialização da classe, e retorna
        o resultado do cálculo a dividir por 3.600, que transforma segundos em horas com o módulo datetime.
        """
        horas = datetime.fromtimestamp(float(self.end_date) / 1000) - datetime.fromtimestamp(float(self.start_date) / 1000)
        diferenca = horas.total_seconds() / 3600
        return round(diferenca)


def criar_lista_objetos_pre20(file_name):
    """
    Cria a lista "condicionamentos" para um ficheiro passado como argumento. Cada item da lista é um objeto
    da classe Condicionamento e corresponde a uma linha do ficheiro.
    """
    with open(file_name, mode='r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        linhas = [i for i in reader]
        condicionamentos, soma, motivos, impactos = [], 0, [], []
        for num, linha in enumerate(linhas[1:]):
            try:
                condicionamentos.append(CondicionamentoPre20(linha))
            except Exception as e:
                pass
        return condicionamentos


def criar_lista_objetos_pos20(file_name):
    """
    Cria a lista "Condicionamentos" para um ficheiro passado como argumento, em que cada item da lista
    é um objeto da classe Condicionamento e corresponde a uma linha do ficheiro.
    """
    with open(file_name, mode='r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        linhas = [i for i in reader]
        condicionamentos, soma, motivos, impactos = [], 0, [], []
        for num, linha in enumerate(linhas[1:]):
            try:
                condicionamentos.append(CondicionamentoPos20(linha))
            except Exception as e:
                pass
        return condicionamentos


def sumula_duracao(condicionamentos=list):
    """
    A função calcula o total em horas da soma da duração dos constrangimentos de uma lista passada como argumento.
    A lista deve conter objetos da classe Condicionamentos para que seja possível utilizar o método periodo_cond para
    realizar o cálculo.
    """
    soma = 0
    for c in condicionamentos:
        soma += c.periodo_cond()
    return round(soma)


def duracao_por_motivo(condicionamentos=list):
    """
    A função cria um dicionário com todos os motivos únicos e a soma da duração dos constrangimentos por motivo encontrados
    no ficheiro, passado como lista. A lista deve conter objetos da classe Condicionamento para que seja possível
    utilizar o parâmetro motivo.
    """
    motivos = [c.motivo for c in condicionamentos]
    motivos_unicos = set(motivos)
    cpm = {f'{i}': 0 for i in motivos_unicos}

    for c in condicionamentos:
        for k, v in cpm.items():
            if c.motivo == k:
                cpm[k] += c.periodo_cond()
    return cpm


def casos_por_impacto(condicionamentos=list):
    """
    A função cria um dicionário com os diferentes impactos/relevâncias encontrados no ficheiro como chave e a contagem
    de casos por impacto como valor.
    A função recebe uma lista com objetos do tipo Condicionamento para que seja possível utilizar o parâmetro impactos do objeto.
    """
    impactos = [c.impacto for c in condicionamentos]
    impactos_unicos = set(impactos)
    imp = {f'{x}': 0 for x in impactos_unicos}

    for c in condicionamentos:
        for k, v in imp.items():
            if c.impacto == k:
                imp[k] += 1
    return imp


def lista_cond_causa(mot_ano):
    """
    A função cria uma string formatada com as causas de condicionamento e a súmula da duração em horas.
    Exemplo:
    PODA DE ÁRVORES: 1928767h
    """
    lista_mot_txt = ''
    for k, v in mot_ano.items():
        lista_mot_txt += f'{k}: {v}h\n'
    return lista_mot_txt


def lista_motivos(imp_ano):
    """
    A função cria uma string formatada com o tipo de impacto e o número de casos.
    Exemplo:
    Causa: 1000
    """
    lista_imp_txt = ''
    for k, v in imp_ano.items():
        lista_imp_txt += f'{k}: {v}\n'
    return lista_imp_txt


def report_ano(nome_arq, ano, sum_ano, mot_ano, imp_ano):
    """
    A função cria um relatório com os dados de condicionamentos em Lisboa no ano definido.

    Retorna um arquivo .txt com a súmula da duração dos condicionamentos no ano, a súmula da duração dos condicionamentos
    por causa no ano e a quantidade de causas por impacto.
    """

    txt = f"""Relatório de dados de condicionamento em Lisboa.

Fonte: https://lisboaaberta.cm-lisboa.pt/index.php/pt/dados/conjuntosde-dados
Arquivo: {nome_arq}
Ano: {ano}
-----------------------------------------------------

1. Súmula da duração dos condicionamentos no ano: {sum_ano}h

2. Lista da súmula da duração dos condicionamentos no ano por causa:

{lista_cond_causa(mot_ano)}
3. Número de casos das várias relevâncias por causa em cada ano:

{lista_motivos(imp_ano)}
-----------------------------------------------------
Autoras:
Natália Akemi Martins Costa Tokuzumi
Bianca Costa Lima
Data: {datetime.today().date()}
Professor: João Leitão
Curso: Aplicações Informáticas para Ciência de Dados
Instituição: IPLUSO
"""
    return txt


def report_ano_ano(a, b, c, d):
    """
    A função cria um ficheiro .txt com os dados de variação da súmula do total dos condicionamentos em Lisboa
    ano a ano.
    """
    ano_ano_txt = f"""Relatório de variação da súmula dos condicionamentos em Lisboa ano a ano:

Variação da súmula da duração total dos constrangimentos entre 2019 e 2018: {round((b/a - 1) * 100)}%
Variação da súmula da duração total dos constrangimentos entre 2020 e 2019: {round((c/b - 1) * 100)}%
Variação da súmula da duração total dos constrangimentos entre 2021 e 2020: {round((d/c - 1) * 100)}%

Veja o gráfico com a súmula da duração do total de condicionamentos por ano na figura - Visualização
do gráfico da súmula da duração do total de condicionamentos por ano - e a previsão para 2022.
    
-----------------------------------------------------
Autoras:
Natália Akemi Martins Costa Tokuzumi
Bianca Costa Lima
Data: {datetime.today().date()}
Professor: João Leitão
Curso: Aplicações Informáticas para Ciência de Dados
Instituição: IPLUSO
    """
    return ano_ano_txt


# Obter dados de 2018
dados_2018 = criar_lista_objetos_pre20('condicionamentostransito2018.csv')
sum_2018 = sumula_duracao(dados_2018)
mot_2018 = duracao_por_motivo(dados_2018)
imp_2018 = casos_por_impacto(dados_2018)

# Salvar os dados de 2018 em um arquivo .txt
with open('dados_2018.txt', mode='w', encoding='utf-8') as file:
    file.write(report_ano('condicionamentostransito2018.csv', '2018', sum_2018, mot_2018, imp_2018))
    file.close()

# Obter dados de 2019
dados_2019 = criar_lista_objetos_pre20('condicionamentostransito2019.csv')
sum_2019 = sumula_duracao(dados_2019)
mot_2019 = duracao_por_motivo(dados_2019)
imp_2019 = casos_por_impacto(dados_2019)

# Salvar os dados de 2019 em um arquivo .txt
with open('dados_2019.txt', mode='w', encoding='utf-8') as file:
    file.write(report_ano('condicionamentostransito2019.csv', '2019', sum_2019, mot_2019, imp_2019))
    file.close()

# Obter dados de 2020
dados_2020 = criar_lista_objetos_pos20('condicionamentostransito2020.csv')
sum_2020 = sumula_duracao(dados_2020)
mot_2020 = duracao_por_motivo(dados_2020)
imp_2020 = casos_por_impacto(dados_2020)

# Salvar os dados de 2020 em um arquivo .txt
with open('dados_2020.txt', mode='w', encoding='utf-8') as file:
    file.write(report_ano('condicionamentostransito2020.csv', '2020', sum_2020, mot_2020, imp_2020))
    file.close()

# Obter dados de 2021
dados_2021 = criar_lista_objetos_pos20('condicionamentostransito2021.csv')
sum_2021 = sumula_duracao(dados_2021)
mot_2021 = duracao_por_motivo(dados_2021)
imp_2021 = casos_por_impacto(dados_2021)

# Salvar os dados de 2021 em um arquivo.txt
with open('dados_2021.txt', mode='w', encoding='utf-8') as file:
    file.write(report_ano('condicionamentostransito2021.csv', '2021', sum_2021, mot_2021, imp_2021))
    file.close()

# Salvar os dados de variação ano a ano em um arquivo .txt
with open('variacao_por_ano.txt', mode='w', encoding='utf-8') as file:
    file.write(report_ano_ano(sum_2018, sum_2019, sum_2020, sum_2021))
    file.close()

# Visualização do gráfico da súmula da duração do total de condicionamentos por ano
fig, axs = plt.subplots(1, 2, constrained_layout=True, sharey=True)
anos = ['2018', '2019', '2020', '2021']
counts = [167.23, 120.61, 3.74, 3.04] # Valores convertidos para milhões de horas
#
# Gráfico Plot
axs[0].plot(anos, counts)
axs[0].set_xticks(anos)
axs[0].set_ylabel('Quantidade em milhões de horas')
axs[0].set_xlabel('Anos')

for i, valor in enumerate(counts):
    axs[0].annotate(str(valor), (anos[i], valor), xytext=(0, 5), textcoords='offset points', ha='center')

# Gráfico de Barras
bar_colors = ['tab:red', 'tab:blue', 'tab:green', 'tab:orange']
axs[1].bar(anos, counts, color=bar_colors)
axs[1].set_xticks(anos)
axs[1].set_xlabel('Anos')

for i, valor in enumerate(counts):
    axs[1].annotate(str(valor), (anos[i], valor), xytext=(0, 5), textcoords='offset points', ha='center')

fig.suptitle('Súmula da duração dos constrangimentos em Lisboa por ano', fontsize=14)
plt.savefig('Análise constrangimentos em Lisboa')


# 6. A vossa previsão em termos de duração total dos constrangimento para o ano de 2022
# Ajustamos uma curva quadrática a um conjunto de pontos (total dos constrangimentos em 2018, 2019, 2020 e 2021)
# e realizamos uma previsão para o ano de 2022 com base nessa curva

anos = ['2018', '2019', '2020', '2021']
valores = [sum_2018, sum_2019, sum_2020, sum_2021]

x = np.arange(len(anos))
y = np.array(valores)
coeficientes = np.polyfit(x, y, 2)
p = np.poly1d(coeficientes)

# Plot dos dados originais e da curva ajustada
plt.clf()  # Limpa a figura anterior
plt.plot(x, y, 'o', label='Dados')
plt.plot(x, p(x), label='Curva ajustada')
plt.xlabel('Ano')
plt.ylabel('Quantidade em milhões de horas')
plt.title('Súmula da duração dos constrangimentos em Lisboa por ano')
plt.legend()

# Obtendo a previsão para o ano de 2022
ano_2022 = len(anos)
valor_2022 = p(ano_2022)

plt.plot(ano_2022, valor_2022, 'ro', label='2022 (Previsão)')
plt.legend()

plt.savefig("Previsão 2022")
print(f"Previsão para 2022: {valor_2022} milhões de horas")
