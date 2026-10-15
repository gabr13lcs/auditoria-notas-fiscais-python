import pandas as pd

df = pd.read_csv("notas_fiscais_bruto.csv")

def checar_duplicatas(df):
    duplicadas = df[df.duplicated(subset="numero_nota", keep=False)]
    return duplicadas.index.tolist()

def checar_divergencia_valor(df):
    divergentes = df[df["valor_nota"] != df["valor_pedido"]]
    return divergentes.index.tolist()

def checar_nota_sem_pedido(df):
    sem_pedido = df[df["pedido_referencia"].isnull()]
    return sem_pedido.index.tolist()

def checar_quantidade_divergente(df, tolerancia=0):
    divergentes = df[df["quantidade_itens"] != df["quantidade_pedido"]]
    return divergentes.index.tolist()

def checar_campos_vazios(df):
    vazios = df[df["fornecedor"].isnull()]
    return vazios.index.tolist()

indices_duplicatas = checar_duplicatas (df)
indices_valor = checar_divergencia_valor (df)
indices_sem_pedido = checar_nota_sem_pedido (df)
indices_quantidade = checar_quantidade_divergente (df)
indices_vazios = checar_campos_vazios (df)

df["problema_duplicata"] = df.index.isin(indices_duplicatas)
df["problema_valor"] = df.index.isin(indices_valor)
df["problema_sem_pedido"] = df.index.isin(indices_sem_pedido)
df["problema_quantidade"] = df.index.isin(indices_quantidade)
df["problema_fornecedor_vazio"] = df.index.isin(indices_vazios)
df["duplicata_excedente"] = df.duplicated(subset="numero_nota", keep="first")

df["tem_inconssistencia"] = df[[
    "problema_duplicata",
    "problema_valor",
    "problema_sem_pedido",
    "problema_quantidade",
    "problema_fornecedor_vazio"
]].any(axis=1)

print("Total de notas:", len(df))
print("Notas com duplicata:", len(indices_duplicatas))
print("Notas com divergência de valor:", len(indices_valor))
print("Notas com divergência de pedido", len(indices_sem_pedido))
print("Notas com quantidade divergente:", len(indices_quantidade))
print("Notas com fornecedor vazio", len(indices_vazios))

df.to_csv("notas_fiscais_analisadas.csv", index=False)