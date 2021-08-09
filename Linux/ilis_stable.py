from sys import *
import math
tokens = []
num_stack = []
symbols = {}
libraries = [0, 0, 0]
todelete = []
def open_file(filename):
    if str(filename)[-3:] == "lis":
        data = open(filename, "r").read()
        data += "<EOF>"
    return data

def lex(filecontent):
    tok = ""
    state = 0
    filecontents = list(filecontent)
    string = ""
    expr = ""
    varStarted = 0
    var = ""
    isexpr = 0
    n = ""
    for char in filecontents:
        tok += char
        if tok == " ":
            if var != "":
                tokens.append("VAR: " + var[4:])
                var = ""
                varStarted = 0
            if state == 0:
                tok = ""
            else:
                tok = " "
        elif tok == "\t":
            if state == 0:
                tok = ""
            else:
                tok = "\t"
        elif tok == ":INICIO-LIS":
            tokens.append("INIC")
            tok = ""
        elif tok == ":INICIO-MAT":
            libraries[0] = 1
            tok = ""
        elif tok == "DOB:":
            if libraries[0] == 1:
                tokens.append("DOB")
            else:
                print("ERROR: NO SE HA ENCONTRADO ESA FUNCIÓN EN LAS LIBRERÍAS DISPONIBLES.")
            tok = ""
        elif tok == "RAIZ:":
            if libraries[0] == 1:
                tokens.append("RAIZ")
            else:
                print("ERROR: NO SE HA ENCONTRADO ESA FUNCIÓN EN LAS LIBRERÍAS DISPONIBLES.")
            tok = ""
        elif tok == "POT:":
            if libraries[0] == 1:
                tokens.append("POT")
            else:
                print("ERROR: NO SE HA ENCONTRADO ESA FUNCIÓN EN LAS LIBRERÍAS DISPONIBLES.")
            tok = ""
        elif tok == "LOG:":
            if libraries[0] == 1:
                tokens.append("LOG")
            else:
                print("ERROR: NO SE HA ENCONTRADO ESA FUNCIÓN EN LAS LIBRERÍAS DISPONIBLES.")
            tok = ""
        elif tok == "LN:":
            if libraries[0] == 1:
                tokens.append("LN")
            else:
                print("ERROR: NO SE HA ENCONTRADO ESA FUNCIÓN EN LAS LIBRERÍAS DISPONIBLES.")
            tok = ""
        elif tok == "\n" or tok == "<EOF>":
            if expr != "" and isexpr == 1:
                tokens.append("EXPR: " + expr)
                expr = ""
            elif expr != "" and isexpr == 0:
                tokens.append("NUM: " + expr)
                expr = ""
            elif var != "":
                tokens.append("VAR: " + var[4:])
                var = ""
                varStarted = 0
            tok = ""
        elif tok == "=" and state == 0:
            if expr != "" and isexpr == 0:
                tokens.append("NUM: " + expr)
                expr = ""
            elif expr != "" and isexpr == 1:
                tokens.append("EXPR: " + expr)
                expr = ""
            if var != "":
                tokens.append("VAR: " + var[4:])
                var = ""
                varStarted = 0
            if tokens[-1] == "IGUAL":
                tokens[-1] = "IGIG"
            else:
                tokens.append("IGUAL")
            tok = ""
        elif tok == "," and state == 0:
            if expr != "" and isexpr == 1:
                tokens.append("EXPR: " + expr)
                expr = ""
            elif expr != "" and isexpr == 0:
                tokens.append("NUM: " + expr)
                expr = ""
            elif var != "":
                tokens.append("VAR: " + var[4:])
                var = ""
                varStarted = 0
            tokens.append("AGS")
            tok = ""
        elif tok == "VAR:" and state == 0:
            varStarted = 1
            var += tok
            tok = ""
        elif varStarted == 1:
            if tok == "<" or tok == ">":
                if var != "":
                    tokens.append("VAR: " + var[4:])
                    var = ""
                    varStarted = 0
            var += tok
            tok = ""
        elif(tok == "0" or tok == "1" or tok == "2" or tok == "3" or tok == "4" or tok == "5" or tok == "6" or tok == "7" or tok == "8" or tok == "9" or tok == ".") and (state == 0):
            expr += tok
            tok = ""
        elif (tok == "+" or tok == "-" or tok == "*" or tok == "/" or tok == "**" or tok == "%" or tok == "(" or tok == ")") and (state == 0):
            isexpr = 1
            expr += tok
            tok = ""
        elif tok == "IMP:":
            tokens.append("IMP")
            tok = ""
        elif tok == "ENT:":
            tokens.append("INPUT")
            tok = ""
        elif tok == "IMPF:":
            tokens.append("IMPF")
            tok = ""
        elif tok == "SI":
            tokens.append("IF")
            tok = ""
        elif tok == "{":
            if expr != "" and isexpr == 0:
                tokens.append("NUM: " + expr)
                expr = ""
            elif expr != "" and isexpr == 1:
                tokens.append("EXPR: " + expr)
                expr = ""
            tokens.append("THEN")
            tok = ""
        elif tok == "}":
            tokens.append("FIN")
            tok = ""
        elif tok == "\"" or tok == " \"" or tok == "<EOF>":
            if state == 0:
                state = 1
            elif state == 1:
                tokens.append("STRING: " + string + "\"")
                string = ""
                state = 0
                tok = ""
        elif state == 1:
            string += tok
            tok = ""
    print(tokens)
    #return ''
    return tokens

def imprimir(toPrint, lineend):
    if  toPrint[0:6] == "STRING":
        toPrint = toPrint[9:-1]
        toPrint = "\033[1;36m" + toPrint
    elif toPrint[0:3] == "NUM":
        #os.system("color 0b")
        toPrint = toPrint[5:]
        toPrint = "\033[1;31m" + toPrint
        #os.system("color 0f")
    elif toPrint[0:4] == "EXPR":
        #os.system("color 04")
        toPrint = evaluar_expr(toPrint[6:])
        toPrint = "\033[1;31m" + toPrint
        #os.system("color 0f")
    if lineend == 0:
        print(toPrint, end = ' ')
    elif lineend == 1:
        print(toPrint)

def checknum(n):
    check = 0
    n = list(n)
    for i in range(len(n)):
        if n[i] != "-" and n[i] != "0" and n[i] != "1" and n[i] != "2" and n[i] != "3" and n[i] != "4" and n[i] != "5" and n[i] != "6" and n[i] != "7" and n[i] != "8" and n[i] != "9" and n[i] != "+" and n[i] != "-" and n[i] != "*" and n[i] != "**" and n[i] != "/" and n[i] != "(" and n[i] != ")" and n[i] != "%" and n[i] != ".":
            check = 1
    return check

def asignar(nombre, valor):
    symbols[nombre[4:]] = valor

def llamar(variable):
    variable = variable[4:]
    if variable in symbols:
        return symbols[variable]
    else:
        return "ERROR: VARIABLE NO DECLARADA."
        exit()

def leerentrada(string, variable):
    i = input("\033[1;32m" + string)
    check = checknum(i)
    if check == 1:
        symbols[variable] = "STRING: \"" + i + "\""
    elif check == 0:
        symbols[variable] = evaluar_expr(i)

def evaluar_expr(expr):
    return "NUM: "+ str(eval(expr))

#funciones de cálculo
def num(n):
    type = ""
    if n[0:3] == "NUM":
        n = n[4:]
    elif n[0:4] == "EXPR":
        n = n[5:]
    elif n[0:6] == "STRING":
        type = "str"
        n = n[9:-1]
    elif n[0:3] == "VAR":
        n = llamar(n)
        if n[0:3] == "NUM":
            n = n[4:]
        elif n[0:4] == "EXPR":
            n = n[5:]
        elif n[0:6] == "STRING":
            type = "str"
            n = n[9:-1]
    if type == "str":
        return n
    else:
        return eval(n)

def doblar(n):
    vuelta = num(n) * 2
    return str(vuelta)

def potencia(base, exponente):
    base = num(base)
    exponente = num(exponente)
    vuelta = base ** exponente
    return str(vuelta)

def raiz(radicando, indice):
    radicando = num(radicando)
    indice = 1/num(indice)
    vuelta = radicando ** indice
    return str(vuelta)

def ln(n):
    base = math.exp(1)
    #print(base)
    #print(num(n))
    vuelta = math.log(num(n), base)
    return str(vuelta)

def logaritmo(base, numero):
    vuelta = math.log(num(numero), num(base))
    return str(vuelta)

#ANALIZADOR
def analizar(arg):
    i = 1
    if arg[0] == "INIC":
        #imprimir("-*----ILIS-v1.0----*-", 1)
        while(i < len(arg)):
            if arg[i] == "FIN":
                i += 1
            elif arg[i] + " " + arg[i + 1][0:6] == "IMP STRING" or arg[i] + " " + arg[i + 1][0:3] == "IMP NUM" or arg[i] + " " + arg[i + 1][0:4] == "IMP EXPR" or arg[i] + " " + arg[i + 1][0:3] == "IMP VAR" or arg[i] + " " + arg[i + 1][0:3] == "IMP DOB" or arg[i] + " " + arg[i + 1][0:3] == "IMP POT" or arg[i] + " " + arg[i + 1][0:4] == "IMP RAIZ" or arg[i] + " " + arg[i + 1] == "IMP LOG" or arg[i] + " " + arg[i + 1] == "IMP LN":
                if arg[i + 1][0:6] == "STRING":
                    imprimir(arg[i + 1], 0)
                    i += 2
                elif arg[i + 1 ][0:3] == "NUM":
                    imprimir(arg[i + 1], 0)
                    i += 2
                elif arg[i + 1][0:4] == "EXPR":
                    imprimir(evaluar_expr(arg[i + 1][5:]), 0)
                    i += 2
                elif arg[i + 1][0:3] == "VAR":
                    imprimir(llamar(arg[i + 1]), 0)
                    i += 2
                #Calculos
                elif arg[i + 1][0:3] == "DOB":
                    imprimir("NUM: " + doblar(arg[i + 2]), 0)
                    i += 3
                elif arg[i + 1][0:3] == "POT":
                    imprimir("NUM: " + potencia(arg[i + 2], arg[i + 4]), 0)
                    i += 5
                elif arg[i + 1][0:4] == "RAIZ":
                    imprimir("NUM: " + raiz(arg[i + 2], arg[i + 4]), 0)
                    i += 5
                elif arg[i + 1][0:3] == "LOG":
                    imprimir("NUM: " + logaritmo(arg[i + 2], arg[i + 4]), 0)
                    i += 5
                elif arg[i + 1][0:2] == "LN":
                    imprimir("NUM: " + ln(arg[i + 2]), 0)
                    i += 3

            elif arg[i] + " " + arg[i + 1][0:6] == "IMPF STRING" or arg[i] + " " + arg[i + 1][0:3] == "IMPF NUM" or arg[i] + " " + arg[i + 1][0:4] == "IMPF EXPR" or arg[i] + " " + arg[i + 1][0:3] == "IMPF VAR" or arg[i] + " " + arg[i + 1][0:3] == "IMPF DOB" or arg[i] + " " + arg[i + 1][0:3] == "IMPF POT" or arg[i] + " " + arg[i + 1][0:4] == "IMPF RAIZ" or arg[i] + " " + arg[i + 1] == "IMPF LOG" or arg[i] + " " + arg[i + 1] == "IMPF LN":
                if arg[i + 1][0:6] == "STRING":
                    imprimir(arg[i + 1], 1)
                    i += 2
                elif arg[i + 1][0:3] == "NUM":
                    imprimir(arg[i + 1], 1)
                    i += 2
                elif arg[i + 1][0:4] == "EXPR":
                    imprimir(evaluar_expr(arg[i + 1][5:]), 1)
                    i += 2
                elif arg[i + 1][0:3] == "VAR":
                    imprimir(llamar(arg[i + 1]), 1)
                    i += 2
                #Calculos
                elif arg[i + 1][0:3] == "DOB":
                    imprimir("NUM: " + doblar(arg[i + 2]), 1)
                    i += 3
                elif arg[i + 1][0:3] == "POT":
                    imprimir("NUM: " + potencia(arg[i + 2], arg[i + 4]), 1)
                    i += 5
                elif arg[i + 1][0:4] == "RAIZ":
                    imprimir("NUM: " + raiz(arg[i + 2], arg[i + 4]), 1)
                    i += 5
                elif arg[i + 1][0:3] == "LOG":
                    imprimir("NUM: " + logaritmo(arg[i + 2], arg[i + 4]), 1)
                    i += 5
                elif arg[i + 1][0:2] == "LN":
                    imprimir("NUM: " + ln(arg[i + 2]), 1)
                    i += 3

            elif arg[i][0:3] + " " + arg[i + 1] + " " + arg[i + 2][0:6] == "VAR IGUAL STRING" or arg[i][0:3] + " " + arg[i + 1] + " " + arg[i + 2][0:3] == "VAR IGUAL NUM" or arg[i][0:3] + " " + arg[i + 1] + " " + arg[i + 2][0:4] == "VAR IGUAL EXPR" or arg[i][0:3] + " " + arg[i + 1] + " " + arg[i + 2][0:3] == "VAR IGUAL VAR" or arg[i][0:3] + " " + arg[i + 1] + " " + arg[i + 2] == "VAR IGUAL DOB" or arg[i][0:3] + " " + arg[i + 1] + " " + arg[i + 2][0:3] == "VAR IGUAL POT" or arg[i][0:3] + " " + arg[i + 1] + " " + arg[i + 2][0:4] == "VAR IGUAL RAIZ" or arg[i][0:3] + " " + arg[i + 1] + " " + arg[i + 2][0:3] == "VAR IGUAL LOG" or arg[i][0:3] + " " + arg[i + 1] + " " + arg[i + 2][0:2] == "VAR IGUAL LN":
                asignar(arg[i], arg[i + 2])
                if arg[i + 2][0:6] == "STRING":
                    asignar(arg[i], arg[i + 2])
                    i += 3
                elif arg[i + 2][0:3] == "NUM":
                    asignar(arg[i], arg[i + 2])
                    i += 3
                elif arg[i + 2][0:4] == "EXPR":
                    asignar(arg[i], str(evaluar_expr(arg[i + 2][5:])))
                    i += 3
                elif arg[i + 2][0:3] == "VAR":
                    asignar(arg[i], llamar(arg[i + 2]))
                    i += 3
                #Calculos
                elif arg[i + 2][0:3] == "DOB":
                    asignar(arg[i], "NUM: " + doblar(arg[i + 3]))
                    i += 4
                elif arg[i + 2][0:3] == "POT":
                    asignar(arg[i], "NUM: " + potencia(arg[i + 3], arg[i + 5]))
                    i += 6
                elif arg[i + 2][0:4] == "RAIZ":
                    asignar(arg[i], "NUM: " + raiz(arg[i + 3], arg[i + 5]))
                    i += 6
                elif arg[i + 2][0:3] == "LOG":
                    asignar(arg[i], "NUM: " + logaritmo(arg[i + 3], arg[i + 5]))
                    i += 6
                elif arg[i + 2][0:2] == "LN":
                    asignar(arg[i], "NUM: " + ln(arg[i + 3]))
                    i += 4
            elif arg[i] + " " + arg[i + 1][0:6] + " " + arg[i + 3][0:3] == "INPUT STRING VAR" or arg[i] + " " + arg[i + 1][0:3] + " " + arg[i + 3][0:3] == "INPUT VAR VAR":
                if arg[i + 1][0:6] == "STRING":
                    leerentrada(arg[i + 1][9:-1], arg[i + 3][4:])
                elif arg[i + 1][0:3] == "VAR":
                    leerentrada(str(llamar(arg[i + 1])[9:-1]), arg[i + 3][4:])
                i += 4
            elif arg[i] + " " + arg[i + 4] == "IF THEN":
                if arg[i + 2] == "IGIG":
                    if str(num(arg[i + 1])) == str(num(arg[i + 3])):
                        i += 5
                    else:
                        while arg[i] != "FIN":
                            todelete.append(arg[i])
                            i += 1
                        todelete.clear()
                        #print(rapelist(todelete))
                        #print(todelete)
                else:
                    i += 5
            else:
                imprimir("ERROR DE SINTAXIS: [ANALIZADOR.]", 1)
                input()
        #print(symbols)
    else:
        imprimir("ERROR: EL PROGRAMA NO SE HA INICIADO CORRECTAMENTE.")
        exit()

def run():
    #data = open_file(input(> ))
    data = open_file(argv[1])
    toks = lex(data)
    analizar(toks)
    print("\033[0m")
run()
#input()
