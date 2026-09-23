import tkinter as tk
from tkinter import messagebox
from src.camera import reconhecer_cliente

def executar_sistema(label_status):
    label_status.config(text="Status: Câmera aberta, aguardando biometria...", fg="blue")
    root.update()
    
    # Chama a função de reconhecimento que criamos no camera.py
    resultado = reconhecer_cliente()
    
    if resultado["status"] == "encontrado":
        msg = f"Bem-vindo de volta, {resultado['nome']}!\nAçaí favorito: {resultado['acai_preferido']}"
        messagebox.showinfo("Cliente Reconhecido!", msg)
        label_status.config(text=f"Status: {resultado['nome']} identificado com sucesso!", fg="green")
    elif resultado["status"] == "novo_cliente":
        messagebox.showinfo("Novo Cliente", "Rosto não encontrado no sistema. Por favor, faça o cadastro!")
        label_status.config(text="Status: Direcionando para cadastro", fg="orange")
    elif resultado["status"] == "cancelado":
        label_status.config(text="Status: Operação cancelada pelo operador", fg="gray")
    else:
        label_status.config(text=f"Status: Erro - {resultado.get('mensagem', 'Desconhecido')}", fg="red")

# Configuração da Interface Gráfica principal
root = tk.Tk()
root.title("Delírio Roxo - Sistema de Reconhecimento Facial")
root.geometry("450x320")
root.config(bg="#f3e5f5")

titulo = tk.Label(root, text="🍇 Delírio Roxo - Açaíteria 🍇", font=("Helvetica", 16, "bold"), bg="#f3e5f5", fg="#4a148c")
titulo.pack(pady=20)

status_label = tk.Label(root, text="Status: Pronto para iniciar", font=("Helvetica", 10), bg="#f3e5f5", fg="#333")
status_label.pack(pady=10)

btn_iniciar = tk.Button(root, text="Iniciar Reconhecimento Facial", font=("Helvetica", 12, "bold"), 
                        bg="#7b1fa2", fg="white", padx=10, pady=8, 
                        command=lambda: executar_sistema(status_label))
btn_iniciar.pack(pady=20)

btn_sair = tk.Button(root, text="Sair", font=("Helvetica", 10), bg="#d32f2f", fg="white", width=12, command=root.quit)
btn_sair.pack(pady=5)

root.mainloop()
