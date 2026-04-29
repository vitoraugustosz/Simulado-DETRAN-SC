import re
import random
from pypdf import PdfReader

# Execução
questoes_extraidas = carregar_questoes(r"./assets/banco-nacional-de-questoes.pdf")
iniciar_simulado(questoes_extraidas)

def carregar_questoes(caminho_pdf):
    questoes = []
    try:
        reader = PdfReader(caminho_pdf)
        texto_completo = ""
        for page in reader.pages:
            texto_completo += page.extract_text() + "\n"

        # Regex específica para o padrão do documento:
        # Pega a pergunta, a correta e o bloco de incorretas
        padrao = re.compile(
            r"\((\w+)\)\s+\d+\.\s+(.*?)\s+Alternativa correta:\s+(.*?)\s+✓.*?Respostas incorretas:(.*?)(?=\(\w+\)\s+\d+\.|$)", 
            re.DOTALL
        )

        matches = padrao.findall(texto_completo)
        
        for dificuldade, enunciado, correta, incorretas_bloco in matches:
            # Limpa as alternativas incorretas removendo os X ou ✗
            erradas = [linha.strip("X ✗ ").strip() for linha in incorretas_bloco.strip().split('\n') if linha.strip()]
            
            questoes.append({
                "pergunta": enunciado.strip(),
                "correta": correta.strip(),
                "opcoes": [correta.strip()] + erradas[:3]
            })
            
    except Exception as e:
        print(f"Erro ao ler PDF: {e}")
    
    return questoes

def iniciar_simulado(questoes):
    if not questoes:
        print("Nenhuma questão encontrada. Verifique se o arquivo PDF está na pasta correta.")
        return

    random.shuffle(questoes)
    acertos = 0

    print("=== SIMULADO DETRAN (TERMINAL) ===")
    
    for i, q in enumerate(questoes):
        print(f"\nQuestão {i+1}: {q['pergunta']}")
        
        opcoes = q['opcoes']
        random.shuffle(opcoes) # Embaralha A, B, C, D
        
        letras = ['A', 'B', 'C', 'D']
        mapa = dict(zip(letras, opcoes))
        
        for letra, texto in mapa.items():
            print(f"{letra}) {texto}")
            
        res = input("\nSua resposta (A, B, C, D): ").upper()
        
        if mapa.get(res) == q['correta']:
            print("Resposta: CORRETA!")
            acertos += 1
        else:
            print(f"Resposta: ERRADA! A correta era: {q['correta']}")
            
    print(f"\n--- FIM ---\nVocê acertou {acertos} de {len(questoes)} questões.")

