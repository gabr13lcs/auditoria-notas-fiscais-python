# 🧾 Auditoria de Notas Fiscais com Python e Power BI

> Pipeline de dados para detecção automática de inconsistências em notas fiscais, com dashboard analítico para monitoramento de riscos financeiros por fornecedor.

---

## 📌 Sobre o Projeto

Este projeto simula um sistema de auditoria fiscal end-to-end: geração de notas fiscais com inconsistências intencionais, validação automática via Python e visualização dos riscos em um dashboard Power BI — replicando um problema real enfrentado por times de controladoria e compras.

---

## 🎯 Objetivos

- Detectar automaticamente inconsistências em notas fiscais (duplicatas, divergências de valor, itens excedentes, pedidos ausentes e campos vazios)
- Quantificar o custo financeiro em risco por tipo de erro
- Identificar os fornecedores com maior volume de problemas
- Monitorar a taxa de inconsistência ao longo do tempo

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

### Tipos de inconsistência detectados
- Duplicata
- Divergência de valor
- Quantidade divergente
- Nota sem pedido de referência
- Fornecedor vazio
- Combinações múltiplas (ex: Duplicata + Valor)

---

## 🛠️ Como foi feito

### Geração de dados (`gerar_dados.py`)
- Geração de **500 notas fiscais** sintéticas com a biblioteca **Faker** (`pt_BR`)
- **18 fornecedores** fictícios gerados dinamicamente
- Inserção controlada de inconsistências:
  - 15 duplicatas
  - 25 divergências de valor (fator entre 1.1x e 1.5x)
  - 10 notas sem pedido de referência
  - 20 divergências de quantidade
  - 8 campos de fornecedor vazios
- Exportação para `notas_fiscais_bruto.csv`

### Validação (`validar_dados.py`)
- 5 funções de checagem independentes com pandas:
  - `checar_duplicatas()` — detecta número de nota repetido
  - `checar_divergencia_valor()` — compara `valor_nota` vs `valor_pedido`
  - `checar_nota_sem_pedido()` — identifica `pedido_referencia` nulo
  - `checar_quantidade_divergente()` — compara `quantidade_itens` vs `quantidade_pedido`
  - `checar_campos_vazios()` — verifica fornecedor em branco
- Flag `tem_inconsistencia` consolidada por linha
- Exportação do dataset enriquecido para `notas_fiscais_analisadas.csv`

### Dashboard Power BI (`Relatorio NF.pbix`)
- **2 páginas**: Visão Geral e Detalhamento por Fornecedor
- **6 KPIs** em DAX com custo em risco calculado
- Gráfico de linha com taxa de inconsistência mensal (abril–outubro)
- Top 10 fornecedores por volume de problemas
- Gráfico de bolhas: volume de notas × taxa de inconsistência × custo em risco
- Filtro dinâmico por fornecedor

---

## 📁 Estrutura do Repositório

```
auditoria-notas-fiscais-python/
│
├── gerar_dados.py               # Geração de notas fiscais sintéticas com erros
├── validar_dados.py             # Validação e classificação das inconsistências
├── notas_fiscais_bruto.csv      # Dataset bruto gerado
├── notas_fiscais_analisadas.csv # Dataset com flags de inconsistência
├── Relatorio NF.pbix            # Dashboard Power BI
└── README.md
```

---

## 🔧 Tecnologias

| Ferramenta | Uso |
|------------|-----|
| Python 3 | Pipeline de geração e validação |
| pandas | Manipulação e análise dos dados |
| Faker (`pt_BR`) | Geração de dados sintéticos realistas |
| Power BI Desktop | Dashboard analítico |
| DAX | Cálculo de KPIs e métricas de risco |
| Power Query | ETL e transformação dos dados |

---

## ▶️ Como executar

```bash
# 1. Instale as dependências
pip install pandas faker

# 2. Gere os dados brutos
python gerar_dados.py

# 3. Execute a validação
python validar_dados.py

# 4. Abra o dashboard
# Abra o arquivo Relatorio NF.pbix no Power BI Desktop
# Atualize a fonte de dados apontando para notas_fiscais_analisadas.csv
```

---

## 👤 Autor

**Gabriel Silva Costa** — Estudante de Arquitetura de Dados — Anhanguera  
📧 gabr13lc0stah@gmail.com · 📍 São Luís – MA · 🔗 [github.com/gabr13lcs](https://github.com/gabr13lcs)

---

*Projeto desenvolvido para fins educacionais e de portfólio.*
