import streamlit as st
import streamlit.components.v1 as components
import re
import unicodedata
import html

st.set_page_config(page_title="Pix Organiza", layout="centered")

def limpar_entrada(texto):
    texto = unicodedata.normalize('NFKC', texto)
    texto = re.sub(r'\*+', ' ', texto)
    texto = texto.replace('\r', '\n')
    texto = re.sub(r'[ \t]+', ' ', texto)
    texto = re.sub(r'\n{2,}', '\n', texto)
    return texto.strip()

bancos = [
    "Banco do Brasil", "BB", "Banco Brasil", "Bco do Brasil", "Bco Brasil", "Brasil",
    "Bradesco", "Banco Bradesco", "Bradesco S.A.", "Bradesco SA", "Bco Bradesco",
    "Itaú", "Itau", "Banco Itaú", "Banco Itau", "Itau Unibanco", "Itaú Unibanco", "Banco Itau SA", "Itau SA",
    "Santander", "Banco Santander", "Santander Brasil", "Santander S.A.", "Santander SA", "Bco Santander",
    "Caixa", "CEF", "Caixa Econômica", "Caixa Economica", "Caixa Federal", "Caixa Econômica Federal",
    "Nubank", "NuBank", "Nu Pagamentos", "Banco Nubank", "Nu", "Nunbank",
    "Inter", "Banco Inter", "Intermedium", "Banco Intermedium",
    "Original", "Banco Original", "Original SA",
    "PagBank", "Pagseguro", "PagSeguro", "Banco Pagseguro", "Banco PagBank",
    "Mercado Pago", "MercadoLivre", "ML", "MPago", "Mercado",
    "BTG", "BTG Pactual", "Banco BTG",
    "XP", "XP Investimentos", "Banco XP", "XP (348)",
    "Picpay", "PicPay", "Banco Picpay",
    "Sicoob", "Banco Sicoob",
    "Sicredi", "Banco Sicredi",
    "Banrisul", "Banco Banrisul",
    "BRB", "Banco BRB",
    "PIX", "Pix", "Chave Pix", "Transferência Pix", "Pix Transferência", "C6 (336)", "creditag"
]

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
        banco = dados['banco'].strip()
        nome = dados['nome'].strip()
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
            f"🏦 Banco: {banco}\n"
            f"👤 Nome: {nome}\n"
            f"🔑 Chave Pix: {chave_pix.strip()}\n"
            f"🏢 Agência: {agencia}\n"
            f"💳 Conta: {conta}\n"
            f"💰 Valor: R$ {valor_formatado}\n"
            f"{'─'*20}\n"
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


# Interface
st.title("📄 Organizador de Pix")
st.markdown("---")

if "resultado" not in st.session_state:
    st.session_state.resultado = ""

if "limpar" in st.session_state and st.session_state["limpar"]:
    st.session_state["entrada"] = ""
    st.session_state["limpar"] = False

with st.expander("✏️ Digite os dados das transações"):
    entrada = st.text_area("Insira os dados brutos", height=300, key="entrada")

# Botões centralizados com espaço proporcional
col1, col2, _ = st.columns([1, 1, 2])

with col1:
    tratar = st.button("✅ Tratar Dados", use_container_width=True)

with col2:
    limpar = st.button("🧹 Limpar Campos", use_container_width=True)

if tratar and entrada:
    entrada = limpar_entrada(entrada)
    st.session_state.resultado = tratar_dados(entrada)

if limpar:
    st.session_state.resultado = ""
    st.session_state["limpar"] = True
    st.rerun()

st.markdown("---")
st.subheader("📌 Dados Tratados")

if st.session_state.resultado:
    resultado_html = html.escape(st.session_state.resultado).replace("\n", "<br>").replace(" ", "&nbsp;")
    components.html(f"""
        <div style="
            background-color: #f5f5f5;
            border-radius: 6px;
            padding: 16px;
            font-family: monospace;
            white-space: pre-wrap;
            cursor: pointer;
            border: 1px solid #ddd;
        " onclick="copiarResultado()" title="Clique para copiar">
            {resultado_html}
        </div>
        <script>
        function copiarResultado() {{
            navigator.clipboard.writeText(`{st.session_state.resultado.replace("`", "\\`")}`)
                .then(() => {{
                    alert("✅ Resultado copiado com sucesso!");
                }})
                .catch(err => {{
                    alert("❌ Erro ao copiar: " + err);
                }});
        }}
        </script>
    """, height=400)

st.markdown("---")
st.markdown("<center><sub>🛠 Feito por @gustavo.python • ⚙ Powered by Python • © 2025</sub></center>", unsafe_allow_html=True)
