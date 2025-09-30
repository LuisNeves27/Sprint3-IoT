# Sprint3-IoT

Projeto do terceiro sprint da disciplina **Disruptive Architectures: IoT, IoB & Generative IA (FIAP)**.
O objetivo foi desenvolver e integrar uma solução IoT com simulação de sensores, banco de dados Oracle e dashboard em tempo real para monitorar ocorrências envolvendo motocicletas.

---

## 🧩 Estrutura do Repositório

```
/
├── backend/
│   ├── app.py           # Servidor Flask com API REST
│   ├── dashboard/       # Arquivos HTML/JS do painel
│   └── ...
├── simulators/          # Scripts simuladores de sensores/dispositivos
├── vision/              # Scripts de visão computacional (detecções)
├── scriptsql.sql        # Criação e carga inicial do banco Oracle
├── requirements.txt     # Dependências Python
└── README.md
```

---

## 🔧 Funcionalidades Implementadas

* API REST em Flask integrada ao banco Oracle.
* Rota `/devices` para leitura e atualização de sensores IoT.
* Rota `/detections` para inserção e consulta de eventos de visão computacional.
* Rota `/occurrences` para consulta das **ocorrências simuladas** (descrição, cidade, clima, gravidade).
* Dashboard em HTML/JS que consulta periodicamente a API e exibe dados em tempo real.
* Script SQL com tabelas e dados simulados (sensores, detecções, ocorrências etc.).

---

## 🛠️ Tecnologias Utilizadas

* **Python 3.11+**
* **Flask** (API REST)
* **Flask-CORS** (cross-origin requests)
* **oracledb / cx_Oracle** (conexão com Oracle)
* **HTML + JavaScript** (dashboard)
* **Oracle Database** (tabelas de sensores, ocorrências e logs)

---

## 🚀 Como Executar

1. Clone o repositório:

   ```bash
   git clone https://github.com/LuisNeves27/Sprint3-IoT.git
   cd Sprint3-IoT
   ```

2. Crie e ative um ambiente virtual (opcional):

   ```bash
   python -m venv .venv
   . .venv/bin/activate   # Linux/macOS
   .venv\Scripts\activate  # Windows
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure o banco Oracle e execute o script SQL:

   ```bash
   sqlplus usuario/senha@oracle @scriptsql.sql
   ```

5. Execute o servidor Flask:

   ```bash
   python backend/app.py
   ```

6. Acesse o dashboard:

   ```
   http://localhost:5000/
   ```

---

## 📋 Endpoints da API

| Método | Endpoint         | Descrição                              |
| ------ | ---------------- | -------------------------------------- |
| GET    | `/devices`       | Lista os sensores IoT                  |
| POST   | `/device_update` | Atualiza ou insere dados de sensor     |
| GET    | `/detections`    | Lista eventos de visão computacional   |
| POST   | `/detections`    | Registra nova detecção                 |
| GET    | `/occurrences`   | Retorna lista de ocorrências simuladas |

---

## 🧪 Casos de Uso

* Ocorrência de moto estacionada em local irregular
* Moto desaparecida e posterior recuperação
* Uso de moto em clima adverso (chuva/enchente)
* Diferentes níveis de gravidade simulados

Essas ocorrências já estão cadastradas via `scriptsql.sql` e podem ser consultadas no dashboard.

---

## 🔍 Melhorias Futuras

* Inserção dinâmica de ocorrências diretamente pelo dashboard.
* Integração de dispositivos reais (ex.: ESP32 + MQTT).
* Alertas/Notificações automáticas com base na gravidade.
* Exibição de mapa com localização em tempo real.
* Detecção de motos com algoritmos de visão computacional (YOLO, etc.).

---

## 👥 Equipe

**Gustavo Rangel**
💼 Estudante de Análise e Desenvolvimento de Sistemas - FIAP
🔗 [LinkedIn](#)

**David Rapeckman**
💼 Estudante de Análise e Desenvolvimento de Sistemas - FIAP
🔗 [LinkedIn](#)

**Luis Felippe Morais**
💼 Estudante de Análise e Desenvolvimento de Sistemas - FIAP
🔗 [LinkedIn](#)

---
