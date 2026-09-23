import tkinter as tk
from tkinter import messagebox
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

def executar_reconhecimento_gui(label_status):
    label_status.config(text="Status: Abrindo a câmera...", fg="blue")
    root.update()
    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        messagebox.showerror("Erro", "Não foi possível acessar a webcam.")
        label_status.config(text="Status: Erro na câmera", fg="red")
        return

    cliente_encontrado = None
    messagebox.showinfo("Aviso", "Olhe para a câmera.\nPressione 'ESPAÇO' para confirmar ou 'ESC' para cancelar.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        altura, largura, _ = frame.shape
        cv2.rectangle(frame, (largura//3, altura//4), (2*largura//3, 3*altura//4), (0, 255, 0), 2)
        cv2.putText(frame, "Delirio Roxo - Posicione o rosto", (40, 40), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        cv2.imshow('Delirio Roxo - GUI', frame)
        tecla = cv2.waitKey(1) & 0xFF
        
        if tecla == 32: # ESPAÇO
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

    # Tratando o resultado na GUI
    if cliente_encontrado["status"] == "encontrado":
        msg = f"Bem-vindo de volta, {cliente_encontrado['nome']}!\nAçaí preferido: {cliente_encontrado['acai_preferido']}"
        messagebox.showinfo("Cliente Reconhecido!", msg)
        label_status.config(text=f"Status: Cliente {cliente_encontrado['nome']} identificado!", fg="green")
    elif cliente_encontrado["status"] == "novo_cliente":
        messagebox.showinfo("Novo Cliente", "Rosto não cadastrado. Redirecionando para cadastro!")
        label_status.config(text="Status: Novo cliente detectado", fg="orange")
    else:
        label_status.config(text="Status: Operação cancelada", fg="gray")

# Configuração da Janela Principal do Tkinter
root = tk.Tk()
root.title("Delírio Roxo - Sistema de Açaíteria")
root.geometry("400x300")
root.config(bg="#f3e5f5") # Tom roxo claro

titulo = tk.Label(root, text="🍇 Delírio Roxo 🍇", font=("Helvetica", 18, "bold"), bg="#f3e5f5", fg="#4a148c")
titulo.pack(pady=20)

status_label = tk.Label(root, text="Status: Aguardando ação...", font=("Helvetica", 10), bg="#f3e5f5", fg="#333")
status_label.pack(pady=10)

btn_reconhecer = tk.Button(root, text="Iniciar Reconhecimento Facial", font=("Helvetica", 12, "bold"), 
                           bg="#7b1fa2", fg="white", padx=10, pady=5, 
                           command=lambda: executar_reconhecimento_gui(status_label))
btn_reconhecer.pack(pady=20)

btn_sair = tk.Button(root, text="Sair", font=("Helvetica", 10), bg="#d32f2f", fg="white", width=10, command=root.quit)
btn_sair.pack(pady=5)

root.mainloop()
