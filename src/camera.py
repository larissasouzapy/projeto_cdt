import cv2
import sqlite3
import os
from deepface import DeepFace

DB_NAME = 'acaiteria.db'
PASTA_FOTOS = 'clientes_fotos' # Pasta onde salvamos a foto original do cadastro

def buscar_todos_clientes():
    """
    Busca todos os clientes cadastrados no SQLite que possuem foto registrada.
    """
    if not os.path.exists(DB_NAME):
        return []
        
    conexao = sqlite3.connect(DB_NAME)
    cursor = conexao.cursor()
    cursor.execute("SELECT id, nome, acai_preferido, foto_path FROM clientes;")
    resultados = cursor.fetchall()
    conexao.close()
    return resultados

def reconhecer_cliente():
    """
    Função da Lari (Visão Computacional):
    - Abre a webcam.
    - Ao pressionar ESPAÇO, tira uma foto temporária do frame atual.
    - Compara com as fotos dos clientes cadastrados no banco usando DeepFace.
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
            
        # Elementos visuais na tela
        altura, largura, _ = frame.shape
        cv2.rectangle(frame, (largura//3, altura//4), (2*largura//3, 3*altura//4), (0, 255, 0), 2)
        cv2.putText(frame, "Delirio Roxo - Posicione o rosto", (40, 40), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        cv2.imshow('Delirio Roxo - Reconhecimento Facial', frame)
        
        tecla = cv2.waitKey(1) & 0xFF
        
        # Pressionar ESPAÇO (código 32) faz a verificação biométrica real
        if tecla == 32:
            print("[IA] Processando leitura biométrica e comparando com o banco...")
            
            # Salva temporariamente o frame atual capturado da webcam
            temp_path = "temp_capture.jpg"
            cv2.imwrite(temp_path, frame)
            
            clientescadastrados = buscar_todos_clientes()
            
            if not clientescadastrados:
                print("[INFO] Nenhum cliente cadastrado no banco. Tratando como novo cliente.")
                cliente_encontrado = {"status": "novo_cliente"}
            else:
                match_encontrado = False
                
                # Compara o frame atual com a foto de cada cliente do banco
                for cliente in clientescadastrados:
                    cliente_id, nome, acai, foto_path = cliente
                    
                    if foto_path and os.path.exists(foto_path):
                        try:
                            # O DeepFace verifica se o rosto na webcam (temp_path) é igual ao do cadastro
                            resultado_deepface = DeepFace.verify(
                                img1_path=temp_path, 
                                img2_path=foto_path, 
                                model_name="Facenet", 
                                enforce_detection=False
                            )
                            
                            # Se passou no limiar de distância (verified = True)
                            if resultado_deepface["verified"]:
                                cliente_encontrado = {
                                    "status": "encontrado",
                                    "id": cliente_id,
                                    "nome": nome,
                                    "acai_preferido": acai
                                }
                                print(f"[SUCESSO] Cliente reconhecido: {nome} (Açaí favorito: {acai})")
                                match_encontrado = True
                                break
                        except Exception as e:
                            print(f"[AVISO] Erro ao processar biometria do cliente {nome}: {e}")
                
                if not match_encontrado:
                    print("[INFO] Rosto não encontrado no sistema. Redirecionando para cadastro.")
                    cliente_encontrado = {"status": "novo_cliente"}
            
            # Remove o arquivo temporário da foto da webcam
            if os.path.exists(temp_path):
                os.remove(temp_path)
                
            break
            
        elif tecla == 27: # ESC
            cliente_encontrado = {"status": "cancelado"}
            break

    cap.release()
    cv2.destroyAllWindows()
    
    return cliente_encontrado

if __name__ == "__main__":
    resultado = reconhecer_cliente()
    print("Resultado do reconhecimento:", resultado)
