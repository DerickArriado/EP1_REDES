import tkinter as tk

class ChatWidget:
    def __init__(self, parent):
        self.parent = parent
        self.chat_messages = []
        self.setup_chat_interface()

    def setup_chat_interface(self):
        """Configura a interface do chat"""
        # Frame do chat no canto inferior esquerdo
        self.chat_frame = tk.Frame(self.parent, bg='lightgray', relief=tk.RAISED, bd=2)
        self.chat_frame.place(x=10, y=480, width=320, height=110)

        # Área de exibição das mensagens
        self.chat_display = tk.Text(self.chat_frame, height=5, width=38, state=tk.DISABLED)
        self.chat_display.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=2)

        # Frame para entrada de mensagem
        self.chat_input_frame = tk.Frame(self.chat_frame)
        self.chat_input_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=2)

        # Entrada de texto
        self.chat_entry = tk.Entry(self.chat_input_frame, width=25)
        self.chat_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.chat_entry.bind("<Return>", self.send_chat_message)

        # Botão de enviar
        self.chat_send_btn = tk.Button(self.chat_input_frame, text="Send", 
                                      command=self.send_chat_message, bg="#90EE90")
        self.chat_send_btn.pack(side=tk.RIGHT, padx=(5,0))

    def send_chat_message(self, event=None):
        """Envia uma mensagem no chat"""
        message = self.chat_entry.get().strip()
        if message:
            self.chat_messages.append(message)
            
            # Atualiza a exibição
            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.insert(tk.END, f"You: {message}\n")
            self.chat_display.config(state=tk.DISABLED)
            
            # Rola para a mensagem mais recente
            self.chat_display.see(tk.END)
            
            # Limpa o campo
            self.chat_entry.delete(0, tk.END)
            
            print(f"Chat message: {message}")