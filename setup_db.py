import pymongo
import streamlit as st

def popular_banco_massivo():
    client = pymongo.MongoClient(st.secrets["mongo_uri"])
    db = client["veris_simp_db"]
    col = db["modelos_base"]
    
    marcas = ["RANDON", "FACCHINI", "GUERRA", "LIBRELATO", "NOMA"]
    # Padrões técnicos (código crlv, nome amigável)
    tipos = [
        ("CA", "Carroceria Aberta"), ("CA 3", "Carroceria Aberta 3 Eixos"),
        ("SID", "Sider"), ("SID 3", "Sider 3 Eixos"),
        ("BAS", "Basculante"), ("BAS 3", "Basculante 3 Eixos"),
        ("TAN", "Tanque"), ("PORT", "Porta-Contêiner")
    ]
    
    lista_modelos = []
    
    # Gerando os 820 registros em memória
    for marca in marcas:
        for sigla, nome in tipos:
            for ano in range(1986, 2027):
                idade = 2026 - ano
                valor_base = 200000.0 if "3" not in sigla else 240000.0
                fator = max(0.4, 1.0 - (idade * 0.02))
                base = valor_base * fator
                
                registro = {
                    "marca": marca,
                    "modelo_nome": f"{marca} {nome} ({ano})", # Chave para o selectbox
                    "crlv_padrao": f"SR/{marca[:3]} {sigla}", # Chave para o CRLV
                    "ano_modelo": ano,
                    "valor_base_novo": round(base, 2),
                    "notas": {
                        "n5": round(base, 2),
                        "n4": round(base * 0.9, 2),
                        "n3": round(base * 0.8, 2),
                        "n2": round(base * 0.6, 2),
                        "n1": round(base * 0.4, 2)
                    }
                }
                lista_modelos.append(registro)
    
    # Inserção segura
    col.delete_many({}) # Limpa base antiga
    col.insert_many(lista_modelos)
    st.success(f"Sucesso! {len(lista_modelos)} modelos foram carregados no banco.")

if __name__ == "__main__":
    st.title("Setup de Banco: 820 Registros")
    if st.button("Popular Base Completa"):
        popular_banco_massivo()
