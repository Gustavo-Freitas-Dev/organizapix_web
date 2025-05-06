import streamlit as st
import re

# LISTA DE BANCOS
bancos = [
    # Banco do Brasil
    "Banco do Brasil", "BB", "Banco Brasil", "Bco do Brasil", "Bco Brasil", "Brasil",

    # Bradesco
    "Bradesco", "Banco Bradesco", "Bradesco S.A.", "Bradesco SA", "Bco Bradesco",

    # Itaú / Itau
    "Itaú", "Itau", "Banco Itaú", "Banco Itau", "Itau Unibanco", "Itaú Unibanco", "Banco Itau SA", "Itau SA",

    # Santander
    "Santander", "Banco Santander", "Santander Brasil", "Santander S.A.", "Santander SA", "Bco Santander",

    # Caixa Econômica
    "Caixa", "CEF", "Caixa Econômica", "Caixa Economica", "Caixa Federal", "Caixa Econômica Federal", "Caixa Econ Federal", "Caixa Econ.", "Cx Econômica", "Cxa", "Cxa Econômica",

    # Nubank
    "Nubank", "NuBank", "Nu Pagamentos", "Nu Pagto", "Banco Nubank", "Nu",

    # Inter
    "Inter", "Banco Inter", "Intermedium", "Banco Intermedium", "Inter SA", "Banco Inter SA",

    # Original
    "Banco Original", "Original", "Original SA",

    # Safra
    "Banco Safra", "Safra", "Safra SA",

    # Pan
    "Banco Pan", "Banco PAN", "Pan", "Banco PAN SA", "Panamericano", "Banco Panamericano",

    # C6
    "C6", "C6 Bank", "Banco C6", "C6 SA",

    # Neon
    "Neon", "Banco Neon", "Neon Pagamentos",

    # PagBank / PagSeguro
    "PagBank", "Pagseguro", "PagSeguro", "Banco Pagseguro", "Banco PagBank", "Pagseg", "Pag",

    # Mercado Pago
    "Mercado Pago", "MercadoLivre", "ML", "MPago", "Mercado",

    # BTG
    "BTG", "BTG Pactual", "Banco BTG", "BTG SA",

    # XP
    "XP", "XP Investimentos", "Banco XP", "XP SA",

    # Modal
    "Modal", "Banco Modal", "ModalMais", "Modal Mais",

    # Daycoval
    "Daycoval", "Banco Daycoval", "Daycoval SA",

    # BMG
    "BMG", "Banco BMG", "BMG SA",

    # Sofisa
    "Sofisa", "Banco Sofisa", "Sofisa Direto", "Banco Sofisa Direto",

    # Votorantim
    "Votorantim", "Banco Votorantim", "BV", "BV Financeira", "Banco BV",

    # ABC Brasil
    "ABC", "Banco ABC Brasil", "ABC Brasil", "Banco ABC",

    # Pine
    "Pine", "Banco Pine",

    # Topázio
    "Topázio", "Topazio", "Banco Topázio", "Banco Topazio", "Topázio Bank", "Topazio Bank",

    # BS2
    "BS2", "Banco BS2", "Banco Bonsucesso", "Bonsucesso",

    # Stone
    "Stone", "Stone Pagamentos", "Banco Stone",

    # Sicoob
    "Sicoob", "Banco Sicoob", "Sistema Sicoob", "Sicoob Cred", "Sicoob SA",

    # Sicredi
    "Sicredi", "Banco Sicredi", "Sistema Sicredi", "Sicredi SA",

    # Banrisul
    "Banrisul", "Banco Banrisul", "Banco do Estado do RS", "Banrisul SA",

    # Banestes
    "Banestes", "Banco Banestes",

    # BRB
    "BRB", "Banco BRB", "Banco de Brasília", "BRB SA",

    # HSBC
    "HSBC", "Banco HSBC",

    # Citibank
    "Citibank", "Citi", "Banco Citi", "Banco Citibank", "Citi SA",

    # JP Morgan
    "JP Morgan", "J.P. Morgan", "Banco JP Morgan", "Banco J.P. Morgan",

    # Rabobank
    "Rabobank", "Banco Rabobank",

    # Western Union
    "Western Union", "WU", "Banco Western Union",

    # Creditas
    "Creditas", "Banco Creditas",

    # Master
    "Master", "Banco Master",

    # Indusval
    "Indusval", "Banco Indusval",

    # BBM
    "BBM", "Banco BBM",

    # Banese
    "Banese", "Banco Banese",

    # PIX / Outros
    "PIX", "Pix", "Chave Pix", "Transferência Pix", "Transferencia Pix", "Pix Transferência",

    # XP
    'XP', 'xp', 'XP (348)', 'Xp', 'Xp (348)', 

     # PicPay
    "Picpay", "PicPay", "Banco Picpay", "PicPay S.A.",
]

# Função para tratar os dados
def tratar_dados(entrada):
    padrao = re.compile(
        rf"(?P<banco>{'|'.join(re.escape(b) for b in bancos)})\s+"  
        r"(?P<nome>[A-Za-zÀ-ÖØ-öø-ÿ0-9&\s.\-]+?)\s+PIX\s+"  
        r"(?:(?:CPF|CNPJ)\s*(?P<chave>[\d. /-]+)|"
        r"Email\s*(?P<email>[\w.\-]+@[a-zA-Z0-9.\-]+)|"  
        r"Fone\s*(?P<fone>\+?[0-9\s()\-]+))\s*"  
        r"(?:AG\s*(?P<agencia>[0-9\-A-Za-z]+))?\s*"  
        r"(?:C[\/\s]?(?:C|POUP|C/C|CC|CPOUP|CNPJ|C/POUP)?\s*(?P<conta>[\w.\-]+))?\s*"  
        r"R\$\s*(?P<valor>\d{1,3}(?:[.,]?\d{3})*[.,]\d{2})",  
        flags=re.IGNORECASE
    )

    resultados = []
    total_valor = 0.0
    total_contas = 0

    for match in padrao.finditer(entrada):
        dados = match.groupdict()
        banco = dados['banco'].strip() if dados.get('banco') else 'Não informado'
        nome = dados['nome'].strip() if dados.get('nome') else 'Não informado'
        agencia = dados.get('agencia') or '-'
        conta = dados.get('conta') or '-'
        chave_pix = dados.get('chave') or dados.get('email') or dados.get('fone') or 'Não informado'

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
            f"Banco: {banco}\n"
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

    valor_total_formatado = f"R$ {total_valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

    if resultados:
        resultado_final = "\n".join(resultados)
        resultado_final += f"Total de transações: {total_contas}\nTotal em valor: {valor_total_formatado}\n"
        return resultado_final
    else:
        return "Nenhuma transação válida encontrada."

# Interface Streamlit
st.set_page_config(page_title="Pix Organiza", layout="centered")

st.title("📄 Organizador de Pix")
st.markdown("---")

with st.expander("✏️ Digite os dados das transações"):
    entrada = st.text_area("Insira os dados brutos", height=300)

col1, col2, col3 = st.columns(3)

with col1:
    tratar = st.button("✅ Tratar Dados")

with col2:
    limpar = st.button("🧹 Limpar Campos")

with col3:
    copiar = st.button("📋 Copiar Resultado")

if "resultado" not in st.session_state:
    st.session_state.resultado = ""

if tratar and entrada:
    st.session_state.resultado = tratar_dados(entrada)

if limpar:
    entrada = ""
    st.session_state.resultado = ""

if copiar and st.session_state.resultado:
    st.code("Resultado copiado com sucesso!")  # apenas feedback visual

st.markdown("---")
st.subheader("📌 Dados Tratados")
st.text_area("Resultado", st.session_state.resultado, height=400)

st.markdown("---")
st.markdown("<center><sub>🛠 Feito por @gustavo.python • ⚙ Powered by Python • © 2025</sub></center>", unsafe_allow_html=True)
