import tkinter as tk
import pyttsx3
import PyPDF2
from tkinter import messagebox
import speech_recognition as sr
import time
import pyautogui
import os
import pygame, random
from pygame.locals import *
class App(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        master.title("Selecione uma ferramenta")

        tk.Button(master, text="Calculadora", command=self.calculadora).grid(row=2, column=1)
        tk.Button(master, text="Pesquisa por fala", command=self.pesquisa_por_fala).grid(row=1, column=1)
        tk.Button(master, text="Jogo da cobrinha", command=self.Jogo_da_cobrinha).grid(row=2, column=0)
        tk.Button(master, text="Leitor de PDF", command=self.leitor_pdf).grid(row=1, column=0)

#########   CALCULADORA   ########
    def calculadora(self):
        # Display #######################################################
        class Calculator:
            def __init__(self, master):
                self.master = master
                master.title("Calculator")

                self.display = tk.Entry(master, width=25, justify="right")
                self.display.grid(row=0, column=0, columnspan=4, pady=5)

                button_list = [
                    "7", "8", "9", "/",
                    "4", "5", "6", "*",
                    "1", "2", "3", "-",
                    "0", "=", "C", "+"
                ]

                row = 1
                col = 0
                for button_text in button_list:
                    button = tk.Button(master, text=button_text, width=5, height=2,
                                       command=lambda text=button_text: self.button_click(text))
                    button.grid(row=row, column=col, padx=2, pady=2)
                    col += 1
                    if col > 3:
                        col = 0
                        row += 1

            # Funcoes ################################################
            def button_click(self, text):
                if text == "C":
                    self.display.delete(0, tk.END)
                elif text == "=":
                    try:
                        result = eval(self.display.get())
                        self.display.delete(0, tk.END)
                        self.display.insert(0, str(result))
                    except:
                        self.display.delete(0, tk.END)
                        self.display.insert(0, "Error")
                else:
                    self.display.insert(tk.END, text)

        root = tk.Tk()
        calculator = Calculator(root)
        root.mainloop()

############### LEITOR DE PDF ######################################################
    def leitor_pdf(self):
        def exibir_mensagem():
            messagebox.showinfo("!AVISO!",
                                "PARA ULTILIZAR O LEITOR DE PDF CORRETAMENTE É PRECISO COLOCAR NO ARQUIVO PDF NA MESMA PASTA DO ARQUIVO main.py E ESCREVER O NOME DELE + .PDF PARA QUE O PROGRAMA FUNCIONE DA MANEIRA CORRETA")
            janela_de_mensagem.destroy()  # Fecha a janela de mensagem
            janela.deiconify()  # Exibe a janela principal

        # Cria uma janela principal
        janela = tk.Tk()

        # Cria um botão "OK" na janela principal
        botao_ok = tk.Button(janela, text="Clique aqui para continuar", command=exibir_mensagem)

        # Posiciona o botão "OK" na janela principal
        botao_ok.pack(),

        # Esconde a janela principal
        janela.withdraw()

        # Cria uma janela de mensagem
        janela_de_mensagem = tk.Toplevel(janela)

        # Cria um botão "OK" na janela de mensagem
        botao_ok_mensagem = tk.Button(janela_de_mensagem, text="CLIQUE AQUI PARA CONTINUAR", command=exibir_mensagem)

        # Posiciona o botão "OK" na janela de mensagem
        botao_ok_mensagem.pack()

        ################# LEITOR DE PDF ##############################
        def ler_pdf():
            # Obtém o nome do arquivo digitado pelo usuário
            nome_arquivo = entrada.get()

            # Abre o arquivo PDF
            Livro = open(nome_arquivo, 'rb')
            pdfReader = PyPDF2.PdfFileReader(Livro)
            paginas = pdfReader.numPages
            print(paginas)
            speaker = pyttsx3.init()
            for num in range(0, paginas):
                page = pdfReader.getPage(num)
                texto = page.extractText()
                speaker.say(texto)
                speaker.runAndWait()

        ####### JANELA DE PERGUNTA DO NOME DO LIVRO #########

        janela = tk.Tk()

        # Cria um widget Entry na janela
        entrada = tk.Entry(janela)

        # Posiciona o widget Entry na janela
        entrada.pack()

        # Cria um botão "Ler PDF" na janela
        botao_ler_pdf = tk.Button(janela, text="Ler PDF", command=ler_pdf)

        # Posiciona o botão "Ler PDF" na janela
        botao_ler_pdf.pack()

        # Inicia o loop principal da janela
        janela.mainloop()


        pass

    def pesquisa_por_fala(self):

        # Define a variável 'palavra' como global
        palavra = ""

        ###################### RECONHECE A FALA
        def reconhecer_fala():
            global palavra  # Define a variável 'palavra' como global
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print("Diga algo!")
                audio = r.listen(source)
                palavra = r.recognize_google(audio, language='pt-BR')
            try:
                palavra = r.recognize_google(audio, language='pt-BR')
                print("Você disse: " + palavra)
                # faça aqui o que desejar com a variável 'palavra'
            except sr.UnknownValueError:
                print("Não foi possível entender o áudio.")
            except sr.RequestError as e:
                print("Não foi possível obter resultados; {0}".format(e))

        ########################### CAIXA DE MENSAGEM
        def exibir_mensagem():
            messagebox.showinfo("!AVISO!",
                                "PARA ULTILIZAR A BUSCA COM FALA VOCÊ PRECISARÁ DIZER ALGUMA PALAVRA OU TEXTO DE SEU INTERESSE QUE O PROGRAMA FARÁ A BUSCA POR ELA NO NAVEGADOR, E TAMBÉM É MUITO IMPORTANTE QUE VOCÊ NÃO CLIQUE EM NADA POIS PODE ATRAPALHAR O FUNCIONAMENTO DO PROGRAMA ")
            janela_de_mensagem.destroy()  # Fecha a janela de mensagem
            janela.deiconify()  # Exibe a janela principal

        ################## BUSCA
        def buscar_palavra():
            global palavra
            reconhecer_fala()
            time.sleep(2)
            os.system("start chrome")
            time.sleep(2)
            pyautogui.write(palavra)
            pyautogui.press('enter')

        ############################ JANELINHA
        janela = tk.Tk()

        janela.withdraw()

        janela_de_mensagem = tk.Toplevel(janela)

        botao_ok_mensagem = tk.Button(janela_de_mensagem, text="CLIQUE AQUI PRIMEIRO PARA CONTINUAR",
                                      command=exibir_mensagem)
        botao_ok_mensagem.pack()

        janela = tk.Tk()

        botao = tk.Button(janela, text="Clique aqui para começar a busca", command=buscar_palavra)
        botao.pack()

        janela.mainloop()

        pass

    def Jogo_da_cobrinha(self):

        def on_grid_random():
            x = random.randint(0, 590)
            y = random.randint(0, 590)
            return (x // 10 * 10, y // 10 * 10)

        def collision(c1, c2):
            return (c1[0] == c2[0]) and (c1[1] == c2[1])

        CIMA = 0
        DIREITA = 1
        BAIXO = 2
        ESQUERDA = 3

        pygame.init()
        screen = pygame.display.set_mode((500, 500))
        pygame.display.set_caption('Snake')

        # cobra
        cobra = [(200, 200), (210, 200), (220, 200)]
        snake_skin = pygame.Surface((10, 10))
        snake_skin.fill((0, 255, 0))

        # fruta
        fruta_pos = on_grid_random()
        fruta = pygame.Surface((10, 10))
        fruta.fill((255, 0, 0))

        my_direction = ESQUERDA

        clock = pygame.time.Clock()

        # Controles e saída
        while True:
            clock.tick(10)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()

                if event.type == KEYDOWN:
                    if event.key == K_UP:
                        my_direction = CIMA
                    if event.key == K_DOWN:
                        my_direction = BAIXO
                    if event.key == K_LEFT:
                        my_direction = ESQUERDA
                    if event.key == K_RIGHT:
                        my_direction = DIREITA

            # colisao e aumento de tamanho
            if collision(cobra[0], fruta_pos):
                fruta_pos = on_grid_random()
                cobra.append(cobra[-1])

            # Direçoes/Movimentos
            for i in range(len(cobra) - 1, 0, -1):
                cobra[i] = (cobra[i - 1][0], cobra[i - 1][1])

            if my_direction == CIMA:
                cobra[0] = (cobra[0][0], cobra[0][1] - 10)
            if my_direction == BAIXO:
                cobra[0] = (cobra[0][0], cobra[0][1] + 10)
            if my_direction == DIREITA:
                cobra[0] = (cobra[0][0] + 10, cobra[0][1])
            if my_direction == ESQUERDA:
                cobra[0] = (cobra[0][0] - 10, cobra[0][1])

            screen.fill((0, 0, 0))
            screen.blit(fruta, fruta_pos)
            for pos in cobra:
                screen.blit(snake_skin, pos)

            pygame.display.update()
        pass


root = tk.Tk()
app = App(root)
root.mainloop()
