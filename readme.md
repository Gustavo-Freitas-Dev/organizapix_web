# 📄 Organizador de Pix

Aplicação prática em Python com [Streamlit](https://streamlit.io) para organizar e extrair dados de transações Pix a partir de textos brutos — ideal para dados copiados de WhatsApp, e-mails ou relatórios.

## ✅ Funcionalidades

- Extração automática de:
  - Nome do favorecido
  - Nome do banco (com variações populares)
  - Chave Pix (CPF, CNPJ, e-mail ou telefone)
  - Agência e conta (quando informadas)
  - Valor da transação
- Formatação limpa e padronizada
- Interface interativa com visual intuitivo
- Cópia rápida do resultado com apenas um clique
- Compatível com desktop e mobile

## 🚀 Como usar localmente

### 1. Clonar o repositório

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

### 2. Instalar dependências

Recomenda-se utilizar um ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Executar a aplicação

```bash
streamlit run streamlit_app.py
```

A aplicação será aberta em `http://localhost:8501`.

## 🛠 Tecnologias utilizadas

- Python 3.8+
- Streamlit
- Expressões regulares (Regex)
- HTML + JavaScript (para cópia interativa)

## 📄 Exemplo de entrada

```text
Itau jose da silva de silva PIX CPF 020.000.017-00 AG 0046 CC 06007-2 R$ 2.364,00
Bradesco MARIA FERNANDES PIX CPF 00011122245 R$ 1.000,00
```

## ✨ Resultado gerado

```text
🏦 Banco: Itau
👤 Nome: jose da silva de silva
🔑 Chave Pix: CPF: 02000001700
🏢 Agência: 0046
💳 Conta: 06007-2
💰 Valor: R$ 2.364,00
────────────────────

🏦 Banco: Bradesco
👤 Nome: MARIA FERNANDES
🔑 Chave Pix: CPF: 00011122245
🏢 Agência: -
💳 Conta: -
💰 Valor: R$ 1.000,00
────────────────────

Total de transações: 2
Total em valor: R$ 3.364,00
```

## 👤 Autor

Desenvolvido com 💚 por **[@gustavo.python](https://www.instagram.com/gustavo.python)**  
© 2025 • Todos os direitos reservados.
