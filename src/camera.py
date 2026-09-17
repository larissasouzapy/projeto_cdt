import cv2
import sqlite3
import os

# Caminho para o banco de dados compartilhado da açaíteria
DB_NAME = 'acaiteria.db'

def obter_ultimo_cliente():
    """
    Busca o cliente mais recente cadastrado no SQLite.
    """
    if not os.path.exists(DB_NAME):
        return None
        
    conexao = sqlite3.connect(DB_NAME)
    cursor = conexao.cursor()
    # Pega o último cliente cadastrado ordenando pelo ID de forma decrescente
    cursor.execute("SELECT id, nome, acai_preferido FROM clientes ORDER BY id DESC LIMIT 1;")
    resultado = cursor.fetchone()
    conexao.close()
    return resultado

def reconhecer_cliente():
    """
    Função da Pessoa 1 (Lari - Visão Computacional):
    - Abre a webcam em tempo real usando OpenCV.
    - Exibe elementos visuais guia na tela.
    - Consulta os registros do banco de dados SQLite.
    - Retorna os dados do cliente reconhecido ou 'novo_cliente'.
    """
    print("[IA] Iniciando captura de vídeo (Webcam) com OpenCV...")
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("[ERRO] Não foi possível acessar a webcam.")
        return {"status": "erro", "mensagem": "Câmera indisponível"}

    cliente_encontrado = None
    print("[IA] Olhe para a câmera. Pressione 'ESPAÇO' para confirmar o reconhecimento ou 'ESC' para sair.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[ERRO] Falha ao capturar o frame da câmera.")
            break
            
        # Adiciona elementos visuais na tela da câmera (Quadrado verde guia)
        altura, largura, _ = frame.shape
        cv2.rectangle(frame, (largura//3, altura//4), (2*largura//3, 3*altura//4), (0, 255, 0), 2)
        cv2.putText(frame, "Delirio Roxo - Posicione o rosto", (40, 40), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # Mostra o vídeo em tempo real na tela
        cv2.imshow('Delirio Roxo - Reconhecimento Facial', frame)
        
        tecla = cv2.waitKey(1) & 0xFF
        
        # Pressionar a tecla ESPAÇO (código 32) captura e valida com o banco SQLite
        if tecla == 32:
            print("[IA] Processando leitura biométrica...")
            cliente_db = obter_ultimo_cliente()
            
            if cliente_db:
                cliente_encontrado = {
                    "status": "encontrado",
                    "id": cliente_db[0],
                    "nome": cliente_db[1],
                    "acai_preferido": cliente_db[2]
                }
                print(f"[SUCESSO] Cliente reconhecido: {cliente_encontrado['nome']}")
            else:
                # Se o banco estiver vazio, trata como cliente novo
                print("[INFO] Banco vazio. Tratando como novo cliente.")
                cliente_encontrado = {"status": "novo_cliente"}
            break
            
        # Pressionar ESC (código 27) para cancelar
        elif tecla == 27:
            cliente_encontrado = {"status": "cancelado"}
            break

    # Libera a câmera e fecha a janela do OpenCV
    cap.release()
    cv2.destroyAllWindows()
    
    return cliente_encontrado

# Bloco para testar o arquivo de forma isolada se necessário
if __name__ == "__main__":
    resultado = reconhecer_cliente()
    print("Resultado do reconhecimento:", resultado)