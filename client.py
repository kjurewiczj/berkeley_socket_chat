import socket
import threading
import tkinter
import customtkinter

customtkinter.set_appearance_mode('System')
customtkinter.set_default_color_theme('dark-blue')

class Client:
    def __init__(self):
        self.app = customtkinter.CTk()
        self.app.title('Czat')
        self.app.geometry('1024x480')

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(('127.0.0.1', 5555))

        self.label = customtkinter.CTkLabel(master=self.app, text='Podaj swoją nazwe')
        self.label.pack(pady=12, padx=10)

        self.nickname_entry = customtkinter.CTkEntry(master=self.app, placeholder_text='Nazwa')
        self.nickname_entry.pack(pady=12, padx=10)

        self.name_button = customtkinter.CTkButton(master=self.app, text='Gotowe', command=self.setNickname)
        self.name_button.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    def setNickname(self):
        self.label.pack_forget()
        self.nickname_entry.pack_forget()
        self.name_button.pack_forget()

        recieve_thread = threading.Thread(target=self.recieve)
        recieve_thread.start()

        write_thread = threading.Thread(target=self.write)
        write_thread.start()

    def recieve(self):
        self.messages = customtkinter.CTkTextbox(master=self.app, width=500)
        self.messages.pack(pady=12, padx=10)
        while True:
            try:
                message = self.client.recv(1024).decode('utf-8')
                if message == 'NICK':
                    self.client.send(self.nickname_entry.get().encode('utf-8'))
                else:
                    self.messages.insert(customtkinter.END, message + "\n")
            except:
                print('Wystapil blad')
                self.client.close()
                break

    def write(self):
        message_frame = tkinter.Frame(master=self.app, bg="#333333")
        message_frame.pack()

        message_content = customtkinter.CTkEntry(master=message_frame, placeholder_text='Twoja wiadomość')
        message_content.pack(side=tkinter.LEFT, pady=12, padx=12)

        message_button = customtkinter.CTkButton(master=message_frame, text='Wyslij', command=lambda: self.sendMessage(f'{self.nickname_entry.get()}: {message_content.get()}'))
        message_button.pack(side=tkinter.LEFT, pady=12, padx=12)

    def sendMessage(self, message):
        self.client.send(message.encode('utf-8'))

    def run(self):
        self.app.mainloop()


if __name__ == '__main__':
    app = Client()
    app.run()