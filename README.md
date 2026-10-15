# 🧾 Auditoria de Notas Fiscais com Python e Power BI

> Pipeline de dados end-to-end para detecção automática de inconsistências em notas fiscais, com dashboard analítico para monitoramento de riscos financeiros por fornecedor, inspirado em um problema real do varejo.

---

## 📌 Sobre o Projeto

Trabalhar no varejo expõe um problema silencioso: notas fiscais com erros passam despercebidas e geram prejuízo financeiro difícil de rastrear. Duplicatas pagas em dobro, valores divergentes do pedido, itens entregues a mais, cada um desses erros representa dinheiro em risco.

Este projeto nasceu dessa observação e replica um sistema de auditoria fiscal do zero: geração de notas sintéticas com erros intencionais, validação automática via Python com pandas, e um dashboard Power BI que transforma os dados em decisões, mostrando onde está o risco, quanto custa e quem são os fornecedores que mais geram problemas.

---

## 🎯 Objetivos

- Simular um volume realista de notas fiscais com inconsistências controladas
- Detectar automaticamente 5 tipos de erro via script Python
- Calcular o custo financeiro em risco por categoria de problema
- Identificar os fornecedores com maior concentração de inconsistências
- Monitorar a evolução da taxa de inconsistência ao longo dos meses

---

## 📊 Resultados do Dashboard

| KPI | Valor |
|-----|-------|
| Total de notas fiscais analisadas | **515** |
| Notas com inconsistências | **87** |
| Taxa de inconsistência | **16,89%** |
| Custo em risco por duplicidade | **R$ 50.789,27** |
| Custo estimado por itens excedentes | **R$ 41.547,70** |
| Custo em risco por divergência de valor | **R$ 20.779,22** |
| **Custo total em risco** | **R$ 113.116,19** |

### Distribuição de inconsistências por tipo
| Tipo de erro | Descrição |
|---|---|
| Duplicata | Mesmo número de nota emitido mais de uma vez |
| Divergência de valor | Valor da nota diferente do valor do pedido |
| Quantidade divergente | Itens entregues em quantidade diferente do pedido |
| Sem pedido de referência | Nota emitida sem pedido vinculado |
| Fornecedor vazio | Campo fornecedor ausente na nota |
| Combinações múltiplas | Nota com mais de um tipo de erro simultaneamente |

---

## 🛠️ Como foi feito

### 1. Geração de dados sintéticos (`gerar_dados.py`)

O primeiro desafio foi criar dados realistas o suficiente para simular um ambiente real de notas fiscais. Para isso foi usada a biblioteca **Faker** com locale `pt_BR`, gerando nomes de empresas brasileiras automaticamente.

**Estrutura de cada nota fiscal gerada:**
```
numero_nota       → sequencial a partir de 1000
fornecedor        → escolhido aleatoriamente entre 18 empresas fictícias
data_emissao      → data aleatória nos últimos 6 meses
pedido_referencia → sequencial a partir de 5000
valor_pedido      → valor entre R$ 200,00 e R$ 5.000,00
quantidade_pedido → entre 1 e 20 itens
valor_nota        → inicialmente igual ao valor_pedido (correto)
quantidade_itens  → inicialmente igual à quantidade_pedido (correto)
status            → "emitida"
```

**Inconsistências inseridas de forma controlada:**
```python
inserir_duplicatas(df, qtd=15)           # 15 notas com número repetido
inserir_divergencia_valor(df, qtd=25)    # 25 notas com valor 10% a 50% maior
inserir_nota_sem_pedido(df, qtd=10)      # 10 notas sem pedido de referência
inserir_quantidade_divergente(df, qtd=20) # 20 notas com quantidade errada
inserir_campos_vazios(df, qtd=8)         # 8 notas com fornecedor em branco
```

O dataset é embaralhado ao final para que os erros não fiquem agrupados, simulando a aleatoriedade de um ambiente real. Exportado como `notas_fiscais_bruto.csv`.

---

### 2. Validação e classificação (`validar_dados.py`)

O maior desafio técnico foi estruturar a lógica de detecção de forma modular e criar métricas de custo em risco a partir dos erros detectados — especialmente porque uma mesma nota pode ter múltiplos problemas simultaneamente.

**5 funções de checagem independentes:**

```python
checar_duplicatas(df)
# Detecta número de nota repetido (subset="numero_nota", keep=False)
# Retorna índices de todas as ocorrências duplicadas

checar_divergencia_valor(df)
# Compara valor_nota != valor_pedido
# Retorna índices onde há divergência

checar_nota_sem_pedido(df)
# Identifica pedido_referencia nulo (isnull)
# Retorna índices sem pedido vinculado

checar_quantidade_divergente(df, tolerancia=0)
# Compara quantidade_itens != quantidade_pedido
# Aceita parâmetro de tolerância para uso futuro

checar_campos_vazios(df)
# Verifica fornecedor em branco (isnull)
# Retorna índices com campo ausente
```

**Flags por linha e consolidação:**
```python
# Uma flag booleana por tipo de erro
df["problema_duplicata"]         = df.index.isin(indices_duplicatas)
df["problema_valor"]             = df.index.isin(indices_valor)
df["problema_sem_pedido"]        = df.index.isin(indices_sem_pedido)
df["problema_quantidade"]        = df.index.isin(indices_quantidade)
df["problema_fornecedor_vazio"]  = df.index.isin(indices_vazios)
df["duplicata_excedente"]        = df.duplicated(subset="numero_nota", keep="first")

# Flag consolidada: TRUE se qualquer problema existir
df["tem_inconsistencia"] = df[[
    "problema_duplicata", "problema_valor",
    "problema_sem_pedido", "problema_quantidade",
    "problema_fornecedor_vazio"
]].any(axis=1)
```

Exportado como `notas_fiscais_analisadas.csv` para consumo pelo Power BI.

---

### 3. Dashboard Power BI (`Relatorio NF.pbix`)

O dashboard foi construído com foco em responder três perguntas de negócio:
- **Qual é o tamanho do problema?** → KPIs de volume e custo na visão geral
- **Onde está concentrado o risco?** → Rankings de fornecedores
- **Como está evoluindo?** → Taxa de inconsistência mês a mês

**Página 1 — Visão Geral (Controle de Inconsistências)**
- 6 KPIs: Total de NF, Notas com inconsistências, Taxa de inconsistência, e 3 custos em risco
- Gráfico de linha: taxa de inconsistência por mês (abril a outubro)
- Gráfico de barras horizontal: Top 10 fornecedores por notas com problema
- Gráfico de barras: Notas com problema por tipo de erro (incluindo combinações)
- Filtro dinâmico por fornecedor

**Página 2 — Visão por Fornecedor**
- Top 10 por custo em risco por divergência de valor
- Top 5 por custo em risco por duplicidade
- Top 5 por custo estimado em itens excedentes
- Top 5 por itens em excesso (quantidade absoluta)
- Gráfico de bolhas: volume de notas × taxa de inconsistência × custo em risco por divergência

**Principais medidas DAX:**
```
Taxa de Inconsistência = DIVIDE([Notas com Inconsistência], [Total NF])

Custo em Risco por Divergência = 
    SUMX(FILTER(Tabela, Tabela[problema_valor] = TRUE()),
    Tabela[valor_nota] - Tabela[valor_pedido])

Custo por Duplicidade = 
    SUMX(FILTER(Tabela, Tabela[duplicata_excedente] = TRUE()),
    Tabela[valor_nota])
```

---

## 💡 Aprendizados e Decisões Técnicas

**Por que Faker e não dados reais?**
Dados fiscais reais são sigilosos. O Faker com locale `pt_BR` gera nomes de empresas brasileiras realistas, permitindo simular o ambiente sem expor dados sensíveis.

**Por que flags booleanas por tipo de erro?**
Permite que uma nota tenha múltiplos erros simultaneamente sem duplicar linhas, e facilita filtros e agrupamentos no Power BI.

**Por que separar geração e validação em scripts distintos?**
Modularidade: o script de validação pode ser usado com qualquer CSV de notas fiscais reais, não apenas com os dados gerados pelo projeto.

---

## 📁 Estrutura do Repositório

```
auditoria-notas-fiscais-python/
│
├── gerar_dados.py                  # Geração de notas fiscais sintéticas com erros
├── validar_dados.py                # Validação e classificação das inconsistências
├── notas_fiscais_bruto.csv         # Dataset bruto gerado (500+ registros)
├── notas_fiscais_analisadas.csv    # Dataset com flags de inconsistência
├── Relatorio NF.pbix               # Dashboard Power BI (2 páginas)
└── README.md
```

---

## ▶️ Como executar

```bash
# 1. Instale as dependências
pip install pandas faker

# 2. Gere os dados brutos
python gerar_dados.py
# → Gera notas_fiscais_bruto.csv com ~515 registros

# 3. Execute a validação
python validar_dados.py
# → Gera notas_fiscais_analisadas.csv com flags de inconsistência
# → Exibe resumo no terminal:
#    Total de notas: 515
#    Notas com duplicata: X
#    Notas com divergência de valor: X
#    ...

# 4. Abra o dashboard
# Abra Relatorio NF.pbix no Power BI Desktop
# Atualize a fonte de dados apontando para notas_fiscais_analisadas.csv
```

---

## 🔧 Tecnologias

| Ferramenta | Versão | Uso |
|------------|--------|-----|
| Python | 3.x | Pipeline de geração e validação |
| pandas | — | Manipulação e análise dos dados |
| Faker (`pt_BR`) | — | Geração de dados sintéticos realistas |
| Power BI Desktop | — | Dashboard analítico com 2 páginas |
| DAX | — | Cálculo de KPIs e métricas de custo em risco |
| Power Query | — | ETL e transformação dos dados |

---

## 👤 Autor

**Gabriel Silva Costa** — Estudante de Arquitetura de Dados — Anhanguera  
📧 gabr13lc0stah@gmail.com · 📍 São Luís – MA

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/gabriel-silva-br/)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white)](https://github.com/gabr13lcs)

---

*Projeto desenvolvido para fins educacionais e de portfólio.*
