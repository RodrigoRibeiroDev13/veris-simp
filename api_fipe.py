# api_fipe.py
import requests

class BrasilApiFipe:
    BASE_URL = "https://brasilapi.com.br/api/fipe/preco/v1"

    @staticmethod
    def consultar_preco_agregado(codigo_fipe, ano_modelo):
        if not codigo_fipe:
            return {"sucesso": False, "motivo": "Código não informado."}
        
        url = f"{BrasilApiFipe.BASE_URL}/{codigo_fipe}"
        
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                dados_modelos = response.json()
                for modelo in dados_modelos:
                    if str(ano_modelo) in modelo.get("anoModelo", ""):
                        valor_limpo = modelo.get("valor", "0").replace("R$", "").replace(".", "").replace(",", ".").strip()
                        return {
                            "sucesso": True,
                            "valor_fipe": float(valor_limpo),
                            "mes_referencia": modelo.get("mesReferencia", "Mês Atual"),
                            "modelo_fipe": modelo.get("modelo", "")
                        }
            return {"sucesso": False, "motivo": "Código FIPE ou Ano não localizado."}
        except requests.exceptions.RequestException as e:
            return {"sucesso": False, "motivo": f"Erro de conexão com a API: {e}"}