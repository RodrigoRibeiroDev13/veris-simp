# calculator.py
import datetime
from api_fipe import BrasilApiFipe
from fpdf import FPDF

class CalculadoraAgregados:
    @staticmethod
    def calcular_depreciacao_local(valor_base, ano_fabricacao):
        ano_atual = datetime.datetime.now().year
        idade = max(0, ano_atual - ano_fabricacao)
        fator = min(0.60, idade * 0.04) 
        return valor_base * (1 - fator)

    @staticmethod
    def obter_valor_sugerido(valor_base_banco, ano_fabricacao, estado_conservacao, codigo_fipe=None):
        valor_referencia = None
        fonte_dados = "Cálculo do Algoritmo Local"

        if codigo_fipe:
            consulta = BrasilApiFipe.consultar_preco_agregado(codigo_fipe, ano_fabricacao)
            if consulta["sucesso"]:
                valor_referencia = consulta["valor_fipe"]
                fonte_dados = f"Tabela FIPE via BrasilAPI ({consulta['mes_referencia']})"
        
        if valor_referencia is None:
            valor_referencia = CalculadoraAgregados.calcular_depreciacao_local(valor_base_banco, ano_fabricacao)

        ajustes = {
            "Excelente (Sem detalhes / Pneus Novos)": 1.10,
            "Bom (Marcas normais de uso)": 1.00,
            "Regular (Necessita de pequenas reformas)": 0.85,
            "Ruim (Avariado / Sem condições de rodagem)": 0.60
        }
        
        multiplicador = ajustes.get(estado_conservacao, 1.00)
        return {
            "valor_final": round(valor_referencia * multiplicador, 2),
            "fonte": fonte_dados
        }

    @staticmethod
    def gerar_pdf_laudo(dados):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 16)
        pdf.cell(0, 10, "VERIS SIMP - LAUDO DE AVALIACAO TECNICA", ln=True, align="C")
        pdf.ln(10)
        
        pdf.set_font("Helvetica", "", 12)
        pdf.cell(0, 10, f"Placa do Veiculo: {dados['placa']}", ln=True)
        pdf.cell(0, 10, f"Marca Fabricante: {dados['marca']}", ln=True)
        pdf.cell(0, 10, f"Texto CRLV: {dados['crlv_resumido']}", ln=True)
        pdf.cell(0, 10, f"Modelo Identificado: {dados['nome_completo']}", ln=True)
        pdf.cell(0, 10, f"Ano Fabricacao: {dados['ano_fabricacao']}", ln=True)
        pdf.cell(0, 10, f"Estado de Conservacao: {dados['estado_conservacao']}", ln=True)
        pdf.ln(5)
        
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 10, f"Valor Final Arbitrado: R$ {dados['valor_final_fixado']:,.2f}", ln=True)
        pdf.ln(10)
        
        pdf.set_font("Helvetica", "I", 11)
        pdf.cell(0, 10, "Justificativa / Parecer do Auditor:", ln=True)
        pdf.multi_cell(0, 10, dados['justificativa'])
        
        return pdf.output()
