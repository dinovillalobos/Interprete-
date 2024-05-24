def obtenerPrioridadOperador(o):
    return {'(': 1, ')': 2, '+': 3, '-': 3, '*': 4, '/': 4, '^': 5, 'sin': 6, 'cos': 6, 'tan': 6}.get(o, 0)

def obtenerListaInfija(cadena_infija):
    infija = []
    cad = ''
    i = 0
    while i < len(cadena_infija):
        if cadena_infija[i:i+3] in ['sin', 'cos', 'tan']:
            if cad != '':
                infija.append(cad)
                cad = ''
            infija.append(cadena_infija[i:i+3])
            i += 3
        elif cadena_infija[i] in ['+', '-', '*', '/', '(', ')', '^']:
            if cad != '':
                infija.append(cad)
                cad = ''
            infija.append(cadena_infija[i])
            i += 1
        elif cadena_infija[i] == chr(32):  # Si es un espacio.
            i += 1
            continue
        else:
            cad += cadena_infija[i]
            i += 1
    if cad != '':
        infija.append(cad)
    return infija

def convertirInfijaAPostfija(expresion_infija):
    infija = obtenerListaInfija(expresion_infija)
    pila = []
    salida = []
    for e in infija:
        if e == '(':
            pila.append(e)
        elif e == ')':
            while pila and pila[-1] != '(':
                salida.append(pila.pop())
            pila.pop()
        elif e in ['+', '-', '*', '/', '^', 'sin', 'cos', 'tan']:
            while (pila and obtenerPrioridadOperador(e) <= obtenerPrioridadOperador(pila[-1])):
                salida.append(pila.pop())
            pila.append(e)
        else:
            salida.append(e)
    while pila:
        salida.append(pila.pop())
    return salida

def evaluarPostfija(expresion_posfija):
    pila = []
    for i in expresion_posfija:
        if i not in ['+', '-', '*', '/', '^', 'sin', 'cos', 'tan']:
            pila.append(float(i))
        else:
            if i in ['sin', 'cos', 'tan']:
                op = pila.pop()
                if i == 'sin':
                    pila.append(math.sin(op))
                elif i == 'cos':
                    pila.append(math.cos(op))
                elif i == 'tan':
                    pila.append(math.tan(op))
            else:
                op2 = pila.pop()
                op1 = pila.pop()
                if i == '+':
                    pila.append(op1 + op2)
                elif i == '-':
                    pila.append(op1 - op2)
                elif i == '*':
                    pila.append(op1 * op2)
                elif i == '/':
                    pila.append(op1 / op2)
                elif i == '^':
                    pila.append(op1 ** op2)
    return pila.pop()

class Variable:
    def __init__(self, nombre, tipo, valor=None):
        self.nombre = nombre
        self.tipo = tipo
        self.valor = valor

def agrega_var(tabla_var, nombre, tipo, valor=None):
    if existe_var(tabla_var, nombre):
        print(f"Error: La variable '{nombre}' ya está declarada.")
    else:
        tabla_var.append(Variable(nombre, tipo, valor))

def existe_var(tabla_var, nombre):
    for v in tabla_var:
        if v.nombre == nombre:
            return True
    return False

def get_var(tabla_var, nombre):
    for v in tabla_var:
        if v.nombre == nombre:
            return v.valor
    return None

def reemplazarVariables(expresion, tabla_var):
    tokens = obtenerListaInfija(expresion)
    for i in range(len(tokens)):
        if es_id(tokens[i]) and not es_funcion(tokens[i]):
            valor = get_var(tabla_var, tokens[i])
            if valor is not None:
                tokens[i] = str(valor)
    return " ".join(tokens)

def set_var(tabla_var, nombre, valor):
    if existe_var(tabla_var, nombre):
        for v in tabla_var:
            if v.nombre == nombre:
                try:
                    if any(op in valor for op in "+-*/^()sincostan"):
                        valor_reemplazado = reemplazarVariables(valor, tabla_var)
                        expresion_posfija = convertirInfijaAPostfija(valor_reemplazado)
                        resultado = evaluarPostfija(expresion_posfija)
                        if resultado.is_integer():
                            v.tipo = 'int'
                            v.valor = int(resultado)
                        else:
                            v.tipo = 'real'
                            v.valor = resultado
                    else:
                        if valor.isdigit() or (valor.replace('.', '', 1).isdigit() and valor.count('.') < 2):
                            if '.' in valor:
                                v.tipo = 'real'
                                v.valor = float(valor)
                            else:
                                v.tipo = 'int'
                                v.valor = int(valor)
                        else:
                            v.tipo = 'string'
                            v.valor = valor
                except Exception as e:
                    print(f"Error al evaluar la expresión: {e}")
                    v.valor = valor
    else:
        print(f"Error: La variable '{nombre}' no ha sido declarada")

def imprime_tabla_var(tabla_var):
    print()
    print('   Tabla de variables')
    print('nombre\t\ttipo\t\tvalor')
    for v in tabla_var:
        print(v.nombre, '\t\t', v.tipo, '\t\t', v.valor)

def es_simbolo_esp(caracter):
    return caracter in "+-*;,.:!#=%&/(){}[]<><=>=="

def es_separador(caracter):
    return caracter in " \n\t"

def es_id(cad):
    return (cad[0] in "_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")

def es_funcion(cad):
    return cad in ['sin', 'cos', 'tan']

def es_pal_res(cad):
    palres = ["int", "real", "string", 'print', 'read', 'tabla', "float"]
    return (cad in palres)

def es_tipo(cad):
    tipos = ["int", "real", "string", "float"]
    return (cad in tipos)

def separa_tokens(linea):
    if len(linea) < 3:
        return []
    else:
        tokens = []
        tokens2 = []
        dentro = False
        for l in linea:
            if l == ';':
                continue
            if es_simbolo_esp(l) and not dentro:
                tokens.append(l)
            if (es_simbolo_esp(l) or es_separador(l)) and dentro:
                tokens.append(cad)
                dentro = False
                if es_simbolo_esp(l):
                    tokens.append(l)
            if not es_simbolo_esp(l) and not es_separador(l) and not dentro:
                dentro = True
                cad = ""
            if not es_simbolo_esp(l) and not es_separador(l) and dentro:
                cad += l
        if dentro:
            tokens.append(cad)
        compuesto = False
        for c in range(len(tokens) - 1):
            if compuesto:
                compuesto = False
                continue
            if tokens[c] in "=<>!" and tokens[c + 1] == "=":
                tokens2.append(tokens[c] + "=")
                compuesto = True
            else:
                tokens2.append(tokens[c])
        tokens2.append(tokens[-1])
        for c in range(1, len(tokens2) - 1):
            if tokens2[c] == "." and esEntero(tokens2[c - 1]) and esEntero(tokens2[c + 1]):
                tokens2[c] = tokens2[c - 1] + tokens2[c] + tokens2[c + 1]
                tokens2[c - 1] = "borrar"
                tokens2[c + 1] = "borrar"
        porBorrar = tokens2.count("borrar")
        for c in range(porBorrar):
            tokens2.remove("borrar")
        tokens = []
        dentroCad = False
        cadena = ""
        for t in tokens2:
            if dentroCad:
                if t[-1] == '"':
                    cadena = cadena + " " + t
                    tokens.append(cadena[1:-1])
                    dentroCad = False
                else:
                    cadena += " " + t
            elif t[0] == '"':
                cadena = t
                dentroCad = True
            else:
                tokens.append(t)
    return tokens

def esEntero(cad):
    try:
        int(cad)
        return True
    except ValueError:
        return False

def quitaComentarios(cad):
    # estados: A, B, C, Z
    estado ="Z"    
    #cad = "a=b/c;"
    cad2 =""
    for c in cad:
        if (estado=="Z"):
            if (c=="/"):
                estado = "A"
            else:
                cad2 = cad2 + c
        elif (estado=="A"):
            if (c=="*"):
                estado="B"
            else:
                estado = "Z"
                cad2=cad2+"/"+c
        elif (estado=="B"):
            if (c=="*"):
                estado = "C"
        elif(estado=="C"):
            if (c=="/"):
                estado="Z"
            else:
                estado="B"
    return cad2

tabla_var = []
ren = ""
while ren != 'end;':
    ren = input('$:')
    ren = quitaComentarios(ren)
    if not ren.endswith(';'):
        print("Error: La entrada debe terminar con un punto y coma ';'")
        continue
    tokens = separa_tokens(ren)
    if len(tokens) == 0:
        continue
    if es_id(tokens[0]):
        if es_pal_res(tokens[0]):
            if es_tipo(tokens[0]):
                if es_id(tokens[1]):
                    agrega_var(tabla_var, tokens[1], tokens[0])
            elif tokens[0] == 'read':
                if tokens[1] == '(' and es_id(tokens[2]) and tokens[3] == ')':
                    leido = input()
                    set_var(tabla_var, tokens[2], leido)
            elif tokens[0] == 'tabla':
                imprime_tabla_var(tabla_var)
            elif tokens[0] == 'print':
                if tokens[1] == '(' and es_id(tokens[2]) and tokens[3] == ')':
                    print(get_var(tabla_var, tokens[2]))
        elif tokens[1] == '=':
            if existe_var(tabla_var, tokens[0]):
                expresion = " ".join(tokens[2:])
                set_var(tabla_var, tokens[0], expresion)
            else:
                print(f"Error: La variable '{tokens[0]}' no ha sido declarada")
    else:
        try:
            resultado = evaluarPostfija(convertirInfijaAPostfija(ren))
            if resultado.is_integer():
                agrega_var(tabla_var, ren, 'int', int(resultado))
            else:
                agrega_var(tabla_var, ren, 'real', resultado)
        except Exception as e:
            print(f"Error en la expresión: {e}")
