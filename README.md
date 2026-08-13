# 🐂 dados-bovinos

> **Sistema Inteligente de Gestão Pecuária, Análise Financeira e Tomada de Decisão**

O **dados-bovinos** é uma aplicação Python desenvolvida para auxiliar produtores e gestores pecuários no controle de lotes de gado, cálculo de rendimento zootécnico e apuração financeira detalhada. O sistema integra banco de dados relacional, geração de relatórios gráficos e inteligência artificial (Google Gemini) para otimizar os resultados na pecuária de corte e leite.

---

## ✨ Funcionalidades Principais

* **🔐 Controle de Acesso e Autenticação:**
  * Cadastro e login de usuários com níveis de permissão (`comum` e `admin`).
  * Persistência de sessões e segurança de dados com SQLite.

* **🧮 Cálculos Zootécnicos e Financeiros:**
  * Cálculo de peso de carcaça e conversão automática em arrobas (@).
  * Apuração de receita bruta e líquida considerando taxas e impostos vigentes (**Funrural**, **SENAR**, **ICMS Interestadual**, vacinação, etc.).
  * Apuração do **Ponto de Equilíbrio** por lote de animais.

* **🧬 Parâmetros Específicos por Raça:**
  * Metadados zootécnicos pré-configurados com limites de **GMD (Ganho Médio Diário)** e **Rendimento de Carcaça** para raças como *Nelore*, *Angus*, *Guzerá* e *Girolando*.

* **📊 Visualização de Dados e Gráficos:**
  * Geração automatizada de gráficos comparativos de lucro e ponto de equilíbrio por lote utilizando **Matplotlib** e **NumPy**.

* **🤖 Assistente Inteligente (Google Gemini API):**
  * Integração com o ecossistema GenAI para insights pecuários e suporte na análise de dados operacionais.

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** [Python 3.x](https://www.python.org/)
* **Banco de Dados:** [SQLite3](https://www.sqlite.org/)
* **Análise e Gráficos:** [Matplotlib](https://matplotlib.org/) e [NumPy](https://numpy.org/)
* **Inteligência Artificial:** [Google GenAI SDK](https://pypi.org/project/google-genai/)
* **Variáveis de Ambiente:** [python-dotenv](https://pypi.org/project/python-dotenv/)
