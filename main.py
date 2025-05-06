import streamlit as st
import re
import pyperclip
import unicodedata

# CONFIGURAÇÕES DA PÁGINA
st.set_page_config(page_title="Pix Organiza", layout="centered")

# CSS
st.markdown("""
    <style>
    html, body {
        background-color: #F4F6FB;
        font-family: 'Segoe UI', sans-serif;
    }
    .stTextArea textarea {
        background-color: #F9FAFB !important;
        border: 1px solid #ccc;
        border-radius: 20px;
        padding: 12px;
        font-size: 15px;
    }
    .stButton>button {
        padding: 10px 20px;
        border-radius: 24px;
        font-weight: 600;
        border: none;
    }
    .card {
        background-color: white;
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 3px 10px rgba(0,0,0,0.07);
        margin-bottom: 20px;
    }
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# LISTA DE BANCOS (resumida para exemplo — inclua todos se quiser)
bancos = [
    "Banco do Brasil", "BB", "Bradesco", "Itaú", "Itau", "Santander", "Nubank", "Caixa", "CEF",
    "Banco Inter", "Banco Original", "Banco Safra", "Banco Pan", "C6 Bank", "Neon", "PagBank",
    "Mercado Pago", "BTG", "XP", "Modal", "Daycoval", "BMG", "Sofisa", "Votorantim", "ABC",
    "Pine", "Topázio", "BS2", "Stone", "Sicoob", "Sicredi", "Banrisul", "Banestes", "BRB",
    "HSBC", "Citibank", "J.P. Morgan", "Rabobank", "Western Union", "Creditas", "Master",
    "Indusval", "BBM", "Banese", "PIX", "Pix"
]

# TÍTULO
st.markdown("### <span style='color:#007BFF'>Organizador de Pix</span>", unsafe_allow_html=True)

# ENTRADA
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("**💡 Cole os dados das transações abaixo:**")
texto_digitado = st.text_area("Digite os dados", label_visibility="collapsed", height=160)
st.markdown("</div>", unsafe_allow_html=True)

# TRATAR DADOS
def tratar_dados(texto):
    padrao = re.compile(
        r"(?P<nome>[A-Za-zÀ-ÖØ-öø-ÿ0-9&\s.\-]+?)\s+PIX\s+"
        r"(?:(?:CPF|CNPJ)\s*(?P<chave>[\d. /-]+)|"
        r"Email\s*(?P<email>[\w.\-]+@[a-zA-Z0-9.\-]+)|"
        r"Fone\s*(?P<fone>\+?[0-9\s()\-]+))\s*"
        r"(?:AG\s*(?P<agencia>[0-9\-A-Za-z]+))?\s*"
        r"(?:C[\/\s]?(?:C|POUP|CC|CNPJ|C/POUP)?\s*(?P<conta>[\w.\-]+))?\s*"
        r"R\$\s*(?P<valor>\d{1,3}(?:[.,]?\d{3})*[.,]\d{2})",
        flags=re.IGNORECASE
    )

    linhas = texto.splitlines()
    resultados = []
    total_valor = 0.0
    total_contas = 0

    for linha in linhas:
        if not linha.strip():
            continue

        match = padrao.search(linha)
        if not match:
            continue

        dados = match.groupdict()

        # Detectar banco pela linha completa
        banco_detectado = "Não identificado"
        for banco_ref in bancos:
            if re.search(rf"\b{re.escape(banco_ref)}\b", linha, re.IGNORECASE):
                banco_detectado = banco_ref
                break

        nome = dados.get('nome', '').strip()
        agencia = dados.get('agencia') or '-'
        conta = dados.get('conta') or '-'
        chave_pix = dados.get('chave') or dados.get('email') or dados.get('fone') or 'Não informado'

        # Tratamento da chave
        if re.fullmatch(r"[\d.\-/ ()]+", chave_pix):
            chave_numerica = re.sub(r"[^\d]", "", chave_pix)
            if len(chave_numerica) == 14:
                chave_pix = f"CNPJ: www.pixcnpj.com/{chave_numerica}"
            elif len(chave_numerica) == 11:
                chave_pix = f"CPF: {chave_numerica}"
            else:
                chave_pix = chave_numerica

        valor_texto = dados.get('valor', '0,00')
        if len(valor_texto) >= 2:
            casa_decimais = valor_texto[-2:]
            centena = valor_texto[:-3]
            total_valor += float(f'{centena.replace(".", "").replace(",", "")}.{casa_decimais}')
            valor_formatado = f'{centena},{casa_decimais}'
        else:
            valor_formatado = '0,00'

        resultado = (
            f"Banco: {banco_detectado}\n"
            f"Nome: {nome}\n"
            f"Chave Pix: {chave_pix.strip()}\n"
            f"Agência: {agencia}\n"
            f"Conta: {conta}\n"
            f"Valor: R$ {valor_formatado}\n"
            f"{'─'*40}\n"
        )

        if resultado not in resultados:
            resultados.append(resultado)
            total_contas += 1

    total_formatado = f"R$ {total_valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

    return "\n".join(resultados) + f"\nTotal de transações: {total_contas}\nTotal em valor: {total_formatado}\n" if resultados else "⚠️ Nenhuma transação válida encontrada."

# BOTÕES
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("✅ Tratar os Dados"):
        if texto_digitado.strip():
            st.session_state["resultado"] = tratar_dados(texto_digitado)

with col2:
    if st.button("🗑️ Limpar Dados"):
        st.session_state["resultado"] = ""
        st.rerun()

with col3:
    if st.button("📋 Copiar Dados"):
        if "resultado" in st.session_state:
            pyperclip.copy(st.session_state["resultado"])
            st.success("✅ Resultado copiado!")

# RESULTADO
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("**📤 Resultado Formatado**")
st.text_area("Resultado", value=st.session_state.get("resultado", ""), height=300, label_visibility="collapsed", disabled=True)
st.markdown("</div>", unsafe_allow_html=True)

# RODAPÉ
st.markdown("""
<div style='text-align: center; font-size: 12px; color: #888; padding-top: 10px;'>
    ⚙️ Feito por <a href='https://www.instagram.com/guuh_black?igsh=aDR2cG9rdGtweTV6' target='_blank' style='color:#007BFF;text-decoration:none;'>@gustavo.python</a> • Powered by Python • © 2025
</div>
""", unsafe_allow_html=True)
