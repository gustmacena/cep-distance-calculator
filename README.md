# 📍 CEP Distance Calculator

Script em Python que calcula a distância geográfica (em quilômetros) entre dois CEPs brasileiros, utilizando coordenadas geográficas obtidas via **BrasilAPI** com fallback automático para o **Nominatim (OpenStreetMap)**.

---

## 🚀 Funcionalidades

- Consulta coordenadas geográficas para **quaisquer CEPs válidos do Brasil**
- Cálculo de distância utilizando a **fórmula de Haversine**
- Execução **paralela** com `ThreadPoolExecutor` para maior performance
- Resultado salvo diretamente na **coluna E de uma planilha Excel**
- Fallback automático para o Nominatim caso a BrasilAPI falhe ou não possua dados

---

## 📂 Estrutura esperada do Excel

| Coluna A         | Coluna B     | Coluna C | Coluna D      | Coluna E     |
|------------------|--------------|----------|---------------|--------------|
| Nome do CD (ex.) | CEP Centro   | ...      | CEP Destino   | Distância    |

- A coluna **E** será preenchida automaticamente pelo script com a distância entre os CEPs.
- Os CEPs devem estar em formato numérico ou texto com 8 dígitos.

---

## 🛠️ Requisitos

- Python 3.8+
- Bibliotecas:

```bash
pip install pandas requests tqdm openpyxl
```

---

## ▶️ Como executar

1. Certifique-se de que o arquivo Excel está no caminho correto, e o script aponta para ele.
2. Execute o script:

```bash
python main.py
```

3. O resultado será salvo no **mesmo arquivo Excel**, na coluna **E** (Distância).

---

## 💡 Exemplo de uso

```python
32183680  → CD Contagem (MG)  
01001000  → Praça da Sé (SP)

🧮 Saída na coluna E: 491.27
```

---

## 🧭 Tecnologias

- [BrasilAPI](https://brasilapi.com.br/)  
- [OpenStreetMap / Nominatim](https://nominatim.org/)
- Python `requests`, `pandas`, `tqdm`, `math`

---

## 📃 Licença

Este projeto está licenciado sob a licença [MIT](LICENSE).

---

## ✍️ Autor

**Gustavo Macena**  
[github.com/gustmacena](https://github.com/gustmacena)
