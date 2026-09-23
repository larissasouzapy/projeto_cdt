import cv2
import sqlite3
import os
from deepface import DeepFace

DB_NAME = 'acaiteria.db'

def buscar_todos_clientes():
    if not os.path.exists(DB_NAME):
        return []
    conexao = sqlite3.connect(DB_NAME)
    cursor = conexao.cursor()
    cursor.execute("SELECT id, nome, acai_preferido, foto_path FROM clientes;")
    resultados = cursor.fetchall()
    conexao.close()
    return resultados

def reconhecer_cliente():
    print("\n[IA] Iniciando captura de vídeo (Webcam)...")
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("[ERRO] Não foi possível acessar a webcam.")
        return {"status": "erro", "mensagem": "Câmera indisponível"}

    cliente_encontrado = None
    print("[IA] Olhe para a câmera. Pressione 'ESPAÇO' para confirmar ou 'ESC' para sair.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        altura, largura, _ = frame.shape
        cv2.rectangle(frame, (largura//3, altura//4), (2*largura//3, 3*altura//4), (0, 255, 0), 2)
        cv2.putText(frame, "Delirio Roxo - Posicione o rosto", (40, 40), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        cv2.imshow('Delirio Roxo - CLI', frame)
        tecla = cv2.waitKey(1) & 0xFF
        
        if tecla == 32: # ESPAÇO
            print("[IA] Processando biometria...")
            temp_path = "temp_capture.jpg"
            cv2.imwrite(temp_path, frame)
            
            clientes = buscar_todos_clientes()
            if not clientes:
                cliente_encontrado = {"status": "novo_cliente"}
            else:
                match = False
                for cliente in clientes:
                    c_id, nome, acai, foto_path = cliente
                    if foto_path and os.path.exists(foto_path):
                        try:
                            res = DeepFace.verify(img1_path=temp_path, img2_path=foto_path, model_name="Facenet", enforce_detection=False)
                            if res["verified"]:
                                cliente_encontrado = {"status": "encontrado", "id": c_id, "nome": nome, "acai_preferido": acai}
                                match = True
                                break
                        except:
                            pass
                if not match:
                    cliente_encontrado = {"status": "novo_cliente"}
            
            if os.path.exists(temp_path):
                os.remove(temp_path)
            break
            
        elif tecla == 27: # ESC
            cliente_encontrado = {"status": "cancelado"}
            break

    cap.release()
    cv2.destroyAllWindows()
    return cliente_encontrado

def menu_cli():
    while True:
        print("\n--- DELÍRIO ROXO (CLI) ---")
        print("1. Iniciar Reconhecimento Facial")
        print("2. Sair")
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            resultado = reconhecer_cliente()
            print(f"Resultado: {resultado}")
        elif opcao == "2":
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    menu_cli()
