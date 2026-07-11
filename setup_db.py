import pymongo
import streamlit as st
import pandas as pd

def popular_banco_tecnico():
    # Conexão segura (garanta que mongo_uri esteja no seu secrets)
    client = pymongo.MongoClient(st.secrets["mongo_uri"])
    db = client["veris_simp_db"]
    col = db["modelos_base"]
    
    marcas = ["RANDON", "FACCHINI", "GUERRA", "LIBRELATO", "NOMA"]
    
    # Lista de tipos com os padrões do CRLV
    tipos = [
        ("CA", "Carroceria Aberta"), ("CA 3", "Carroceria Aberta 3 Eixos"),
        ("SID", "Sider"), ("SID 3", "Sider 3 Eixos"),
        ("BAS", "Basculante"), ("BAS 3", "Basculante 3 Eixos"),
        ("TAN", "Tanque"), ("PORT", "Porta-Contêiner")
    ]
    
    lista_modelos = []
    
    for marca in marcas:
        for sigla, nome in tipos:
            for ano in range(1986, 2027):
                idade = 2026 - ano
                # Base de valor com ágio para eixos extras
                valor_base = 200000.0 if "3" not in sigla else 240000.0
                
                # Cálculo de depreciação: perda de 2% ao ano, limite de 40% do valor
                fator = max(0.4, 1.0 - (idade * 0.02))
                base = valor_base * fator
                
                registro = {
                    "marca": marca,
                    "modelo_crlv": f"SR/{marca[:3]} {sigla}", 
                    "modelo_completo": f"{marca} {nome}",
                    "ano_modelo": ano,
                    "valor_n5": round(base, 2),
                    "valor_n4": round(base * 0.9, 2),
                    "valor_n3": round(base * 0.8, 2),
                    "valor_n2": round(base * 0.6, 2),
                    "valor_n1": round(base * 0.4, 2)
                }
                lista_modelos.append(registro)
    
    # Inserção no Banco
    col.delete_many({}) # Limpa base anterior
    col.insert_many(lista_modelos)
    
    # Exporta para Excel automaticamente como backup
    df = pd.DataFrame(lista_modelos)
    df.to_excel("Base_Tecnica_Completa.xlsx", index=False)
    
    st.success(f"Banco populado! {len(lista_modelos)} registros criados e backup gerado.")

if __name__ == "__main__":
    st.title("⚙️ Painel de Setup Técnico")
    if st.button("Executar: Popular Banco e Gerar Excel"):
        popular_banco_tecnico()
