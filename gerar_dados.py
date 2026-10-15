from faker import Faker
from datetime import date, timedelta
import pandas as pd
import random

fake = Faker('pt_BR')

def data_aleatoria(meses_atras=6):
     hoje = date.today()
     dias_atras = random.randint(0, meses_atras * 30)
     return hoje - timedelta(days=dias_atras)

FORNECEDORES = [fake.company() for _ in range(18)]

def gerar_notas(qtd=500):
    notas = []
    for i in range(qtd):
        nota = {
            "numero_nota": 1000 + i,
            "fornecedor": random.choice(FORNECEDORES),
            "data_emissao": data_aleatoria(),
            "pedido_referencia": 5000 + i,
            "valor_pedido": round(random.uniform(200, 5000), 2),
            "quantidade_pedido": random.randint(1, 20),
        }
        nota["valor_nota"] = nota["valor_pedido"]
        nota["quantidade_itens"] = nota["quantidade_pedido"]
        nota["status"] = "emitida"
        notas.append(nota)
    return pd.DataFrame(notas)

df = gerar_notas()

def inserir_duplicatas(df, qtd=15):
    duplicadas = df.sample(qtd)
    return pd.concat([df, duplicadas], ignore_index=True)

def inserir_divergencia_valor(df, qtd=25):
    indices = df.sample(qtd).index
    for i in indices:
        df.loc[i, "valor_nota"] = round(df.loc[i, "valor_pedido"] * random.uniform(1.1, 1.5), 2)
    return df

def inserir_nota_sem_pedido(df, qtd=10):
    indices = df.sample(qtd).index
    df.loc[indices, "pedido_referencia"] = None
    return df
    
def inserir_quantidade_divergencia(df, qtd=20):
    indices = df.sample(qtd).index
    for i in indices:
        df.loc[i, "quantidade_itens"] = df.loc[i, "quantidade_itens"] + random.randint(1, 5)
    return df

def inserir_campos_vazios(df, qtd=8):
    indices = df.sample(qtd).index
    df.loc[indices, "fornecedor"] = None
    return df

df = inserir_duplicatas(df)
df = inserir_divergencia_valor(df)
df = inserir_nota_sem_pedido(df)
df = inserir_quantidade_divergencia(df)
df = inserir_campos_vazios(df)

df = df.sample(frac=1).reset_index(drop=True)

df.to_csv("notas_fiscais_bruto.csv", index=False)