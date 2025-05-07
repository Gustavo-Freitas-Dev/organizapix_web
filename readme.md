# 📄 Organizador de Pix

Aplicação simples em Python com [Streamlit](https://streamlit.io) para organizar e extrair dados de transações Pix a partir de textos brutos (copiados do WhatsApp, e-mail, etc.).

## ✅ Funcionalidades

- Extrai nome, banco, chave Pix, agência, conta e valor.
- Formata automaticamente os dados.
- Exibe os dados organizados em uma área interativa.
- Permite copiar todo o conteúdo formatado com um clique.
- Design responsivo e otimizado para web.

## 🚀 Como usar

### 1. Clonar o repositório

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

### 2. Instalar dependências

É recomendado usar um ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Rodar a aplicação

```bash
streamlit run streamlit_app.py
```

A aplicação abrirá em `http://localhost:8501`.

## 🌐 Deploy

Se quiser publicar a aplicação gratuitamente:

1. Suba o projeto no GitHub.
2. Vá até [https://share.streamlit.io](https://share.streamlit.io)
3. Conecte sua conta do GitHub.
4. Escolha o repositório e arquivo principal (`streamlit_app.py`).
5. Pronto! O app será hospedado online.

## 🛠 Tecnologias

- Python 3.8+
- Streamlit
- Regex (re)
- HTML + JavaScript (para cópia)

## 📄 Exemplo de entrada

```text
Itau jose da silva de silva PIX CPF 020.000.017-00 AG 0046 CC 06007-2 R$ 2.364,00
Bradesco MARIA FERNANDES PIX CPF 00011122245 R$ 1.000,00
```

## ✨ Resultado

```text
🏦 Banco: Itau
👤 Nome: jose da silva de silva
🔑 Chave Pix: CPF: 020.000.017-00
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

Feito com 💚 por **[@gustavo.python](https://www.instagram.com/gustavo.python)**  
© 2025 • Todos os direitos reservados.
