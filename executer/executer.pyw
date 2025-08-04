import subprocess
import os
import tkinter as tk
from tkinter.ttk import Combobox

janela = tk.Tk()
janela.geometry('1250x950')
janela.resizable(False, False)
janela.title("Executer")


def execute(input, code):
    with open("code/script.py", "w", encoding="utf-8") as file:
        file.write(code)

    proc = subprocess.Popen(["python", "code/script.py"],stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    try:
        scriptInput = input
        if scriptInput != "":
            stdout, stderr = proc.communicate(input=scriptInput, timeout=2)
        else:
            stdout, stderr = proc.communicate(timeout=2)
        
        if stderr != "":
            stderr = str(stderr)
            index = stderr.index("line ")
            stderr = stderr[index:]

        return (str(stdout) + str(stderr))
    except:
        proc.terminate()
        return ("Erro de timeout.")
    
def explain(problem):
    with open(f"code/{problem}/premissa.txt", "r", encoding="utf-8") as file:
        return(str(file.read()))
    
def solve(problem, code):
    pa = f"code/{problem}/in"
    casos = len([f for f in os.listdir(pa) if os.path.isfile(os.path.join(pa, f))])
    
    for t in range(0, casos):
        input = ""
        gabarito = ""
        with open(f"code/{problem}/in/{t}.txt", "r", encoding="utf-8") as file:
            input = str(file.read())
        with open(f"code/{problem}/out/{t}.txt", "r", encoding="utf-8") as file:
            gabarito = str(file.read())

        result = execute(input, code)
        if result == "Erro de timeout.":
            return(f"{result} Casos teste passados: {t}/{casos}.\n")
        elif result != gabarito:
            return(f"Erro! Casos teste passados: {t}/{casos}.\nSeu output:\n{result}\n\nEsperado:\n{gabarito}")
        
    return(f"Problema resolvido! --> {problem}")

def problemas():
    pa = "code/"

    answer = ""
    for f in os.listdir(pa):
        if not os.path.isfile(os.path.join(pa, f)):
            answer += str(f)
        
    return(answer)


# print(problemas())

# print(explain("Matematica Basica"))

# code = ""
# with open("submit.txt", "r", encoding="utf-8") as file:
#     code = str(file.read())

# print(solve("Matematica Basica", code))


def atualizar(*args):
    pass

def atualizarProblemaPremissa(*args):
    global listaProblemas
    problemaPremissa.config(state=tk.NORMAL)
    problemaPremissa.delete("1.0", tk.END)
    problemaPremissa.insert(tk.END, explain(listaProblemas[dropdown.current()]))
    problemaPremissa.config(state=tk.DISABLED)
    pass

def rodarCodigo(*args):
    executado = "Por favor, selecione um problema."
    if dropdown.current() != -1:
        codigo = input.get("1.0", tk.END).strip()
        executado = solve(listaProblemas[dropdown.current()], codigo)
        
    resultado.config(state=tk.NORMAL)
    resultado.delete("1.0", tk.END)
    resultado.insert(tk.END, executado)
    resultado.config(state=tk.DISABLED)
    pass

problemaTexto = tk.Label(janela, text="Escolha o problema:")
problemaTexto.grid(row=0, column=1, padx=10, pady=10,sticky="w")

listaProblemas = [f for f in os.listdir("code/") if os.path.isdir(f"code/{f}")]
problemaSelecionado = tk.StringVar
dropdown = Combobox(janela, textvariable=problemaSelecionado)
dropdown.configure(width=50)
dropdown['values'] = listaProblemas
dropdown.current() 
dropdown.grid(row=0, column=2, padx=10, pady=10, sticky="e")
dropdown.bind("<<ComboboxSelected>>", atualizarProblemaPremissa)


problemaPremissa = tk.Text(janela, height=25, width=153, state=tk.DISABLED)
problemaPremissa.grid(row=1, column=1, columnspan=2, padx=10, pady=10)


textoInput = tk.Label(janela, text="Escreva seu código aqui:")
textoInput.grid(row=2, column=1, padx=10, pady=10, sticky="w")
input = tk.Text(janela, height=25, width=75)
input.grid(row=3, column=1, padx=10, pady=10)
input.bind("<Return>", atualizar)
executarBotao = tk.Button(janela, text="Executar código", command=rodarCodigo, width=40, height=2)
executarBotao.grid(row=2, column=1, sticky="e",padx=10)


textoResultado = tk.Label(janela, text="Resultado:")
textoResultado.grid(row=2, column=2, padx=10, pady=10, sticky="w")
resultado = tk.Text(janela, height=25, width=75, state=tk.DISABLED)
resultado.grid(row=3, column=2, padx=10, pady=10)


janela.mainloop()