import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="Resolutor de Sistemas Lineares", layout="wide")

st.title("🧮 Resolutor de Sistemas Lineares (Método de Escalonamento)")
st.markdown("""
Esta ferramenta resolve sistemas de até 10x10. 
Insira o tamanho, preencha a tabela e clique em **Resolver**.
""")

# 1. Configuração do Tamanho
n = st.sidebar.number_input("Tamanho do Sistema (n x n):", min_value=2, max_value=10, value=3)

st.subheader(f"1. Preencha os Coeficientes e o Termo Independente (b)")
st.info("Dica: As colunas de x1 até xn são os coeficientes. A última coluna (b) é o resultado após o '='.")

# Criar um DataFrame inicial para a entrada de dados (estilo Excel)
colunas = [f"x{i+1}" for i in range(n)] + ["b (Resultado)"]
df_input = pd.DataFrame(np.zeros((n, n + 1)), columns=colunas)

# Widget de edição de tabela
input_data = st.data_editor(df_input, use_container_width=True, hide_index=False)

if st.button("🚀 Resolver Sistema"):
    sistema = input_data.to_numpy()
    
    # Mostrar Sistema Original
    st.divider()
    st.subheader("2. Processamento")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Sistema Original:**")
        st.dataframe(input_data)

    # --- LÓGICA DE ESCALONAMENTO ---
    for i in range(n):
        # Pivoteamento Parcial
        for k in range(i + 1, n):
            if abs(sistema[k][i]) > abs(sistema[i][i]):
                sistema[[i, k]] = sistema[[k, i]]

        pivo = sistema[i][i]
        if abs(pivo) > 1e-10:
            for k in range(i + 1, n):
                fator = sistema[k][i] / pivo
                sistema[k] = sistema[k] - fator * sistema[i]
    
    with col2:
        st.write("**Sistema Escalonado:**")
        df_escalonado = pd.DataFrame(sistema, columns=colunas)
        st.dataframe(df_escalonado)

    # --- ANÁLISE DE SOLUÇÃO ---
    solucao = np.zeros(n)
    tipo_sistema = "SPD"

    for i in range(n - 1, -1, -1):
        soma = sum(sistema[i][j] * solucao[j] for j in range(i + 1, n))
        if abs(sistema[i][i]) < 1e-10:
            if abs(sistema[i][n] - soma) > 1e-10:
                tipo_sistema = "SI"
                break
            else:
                tipo_sistema = "SPI"
        else:
            solucao[i] = (sistema[i][n] - soma) / sistema[i][i]

    # --- EXIBIÇÃO DO RESULTADO FINAL ---
    st.divider()
    st.subheader("3. Conclusão")
    
    if tipo_sistema == "SI":
        st.error("❌ **Sistema Impossível (SI):** O sistema não possui solução.")
    elif tipo_sistema == "SPI":
        st.warning("⚠️ **Sistema Possível e Indeterminado (SPI):** O sistema possui infinitas soluções.")
    else:
        st.success("✅ **Sistema Possível e Determinado (SPD):** Solução única encontrada.")
        res_cols = st.columns(n)
        for i in range(n):
            res_cols[i].metric(label=f"x{i+1}", value=f"{solucao[i]:.4f}")

st.sidebar.markdown("---")
st.sidebar.write("Desenvolvido para o Trabalho de Álgebra Linear.")