#!/usr/bin/python
import os, sys

class parsing:
    def __init__(self,flWrite):
        self.content = open(flWrite) # abre el contenido del archivo con programacion assembler 
        self.stop=True   #variable para para el proceso de traduccion 
        self.order = [""] #creamos una variable para almacenar el contenido 
        self.type = {     #definimos un diccionario para identifiar en que categoria encaja la orden 
        "sub" : "math",
        "add" : "math",
        "neg" : "math",
        "eq"  : "math",
        "gt"  : "math",
        "lt"  : "math",
        "and" : "math",
        "or"  : "math",
        "not" : "math",
        "push" : "push",
        "pop"  : "pop",
        "EOF"  : "EOF",
        }
    
    def whenStop(self):
        location = self.content. #retorna la pocicion en la que esta el curso en el archivo  
        self.step() #metodo de verificacion de comentarios y camio de la variable de detenida
        self.content.seek(location) #extrae el contenido que se encuentra en esa posicion 
        return  self.stop

    def step(self):
        thisLine = self.content.readline() #definicion de una cadena decaracteres de la pocicion actual 
        if thisLine == '':# verificacion de si existe codigo para traducir o no 
            self.stop = False # variable sentinela para la detencion del codigo 
        else:
            splitLine = thisLine.split("/")[0].strip() #separa la cadena de caracteres al encontrar "/" ya que despues de ese simbolo son comentarios y remueve los espacion del principio y del final 
            if splitLine == '': # verifica si es un comentario sin ningun codigo 
                self.step()
            else:
                self.order = splitLine.split() #crea un vectos unicamente con la linea de codigo 

    def orderType(self):
     return self.type.get(self.order[0], "invalid Type") #verifica que es una accion permitida 

    def arg1(self):
        return self.order[1] #separa el tipo del codigo

    def arg2(self):
        return self.order[2] #separa el subcontenido del codigo 

class traslator:
  def __init__(self, dest):
    self.nameFile = dest[:-4].split('/')[-1]
    self.outfile = open(dest, "w")
    self.nextLabel = 0

  def setFileName(self, source):
    self.fileName = source[:-3]

  def writeArithmetic(self, command): #Definicion de traduccion de operaciones aritmeticas 
    result = ""
    if command == "add":
      result += "@SP\n" + "AM=M-1\n" + "D=M\n"  + "@SP\n"  + "AM=M-1\n"  + "M=D+M\n" + "@SP\n" + "M=M+1\n" 
    elif command == "sub":
      result += "@SP\n" + "AM=M-1\n"+ "D=M\n" + "@SP\n" + "AM=M-1\n" + "M=M-D\n"+ "@SP\n"+ "M=M+1\n" 
    elif command == "neg":
      result += "@SP\n" + "A=M-1\n" + "M=-M\n"
    elif command == "not":
       result += "@SP\n" + "A=M-1\n" + "M=!M\n" 
    elif command == "or":
      result += "@SP\n"+ "AM=M-1\n"+ "D=M\n" + "@SP\n" + "A=M-1\n"+ "M=D|M\n"
    elif command == "and":
      result += "@SP\n" + "AM=M-1\n"+ "D=M\n" + "@SP\n" + "A=M-1\n"+ "M=D&M\n" 
    elif command == "eq":
      label = str(self.nextLabel)
      self.nextLabel += 1
      result += "@SP\n" + "AM=M-1\n"+ "D=M\n" + "@SP\n" + "A=M-1\n"+ "D=M-D\n" + "M=-1\n" + "@eqTrue" + label + "\n" + "D;JEQ\n"+ "@SP\n" + "A=M-1\n"+ "M=0\n" + "(eqTrue" + label + ")\n"
    elif command == "gt":
      label = str(self.nextLabel)
      self.nextLabel += 1
      result += "@SP\n" + "AM=M-1\n"+ "D=M\n" + "@SP\n" + "A=M-1\n"+ "D=M-D\n" + "M=-1\n" + "@gtTrue" + label + "\n" + "D;JGT\n"+ "@SP\n" + "A=M-1\n"+ "M=0\n" + "(gtTrue" + label + ")\n"
    elif command == "lt":
      label = str(self.nextLabel)
      self.nextLabel += 1
      result += "@SP\n" + "AM=M-1\n"+ "D=M\n" + "@SP\n" + "A=M-1\n"+ "D=M-D\n" + "M=-1\n" + "@ltTrue" + label + "\n"+ "D;JLT\n"+ "@SP\n" + "A=M-1\n"+ "M=0\n" + "(ltTrue" + label + ")\n"
    else:
      result = command + " Aun no implementado\n"
    self.outfile.write("// " + command + "\n" + result)

  def writePushPop(self, command, segment, index): #metodo para accione push y pop
    result = ""
    if command == "push":
      result += "// push " + segment + index + "\n"
      if segment == "constant":
        result += "@" + index + "\n"   + "D=A\n"   + "@SP\n"   + "A=M\n"   + "M=D\n"   + "@SP\n" + "M=M+1\n" 
      elif segment == "static":
        result += "@" + self.nameFile + "." + index + "\n"  + "D=M\n"  + "@SP\n"   + "A=M\n"   + "M=D\n"  + "@SP\n"  + "M=M+1\n"
      elif segment == "this":
        result += "@" + index + "\n"   + "D=A\n"  + "@THIS\n"  + "A=M+D\n"   + "D=M\n"  + "@SP\n"   + "A=M\n"  + "M=D\n"  + "@SP\n"   + "M=M+1\n"
      elif segment == "that":
        result += "@" + index + "\n"   + "D=A\n"  + "@THAT\n"  + "A=M+D\n"   + "D=M\n"  + "@SP\n"   + "A=M\n"  + "M=D\n"  + "@SP\n"   + "M=M+1\n"
      elif segment == "argument":
       result += "@" + index + "\n"   + "D=A\n"  + "@ARG\n"  + "A=M+D\n"   + "D=M\n"  + "@SP\n"   + "A=M\n"  + "M=D\n"  + "@SP\n"   + "M=M+1\n"
      elif segment == "local":
        result += "@" + index + "\n"   + "D=A\n"  + "@LCL\n"  + "A=M+D\n"   + "D=M\n"  + "@SP\n"   + "A=M\n"  + "M=D\n"  + "@SP\n"   + "M=M+1\n"
      elif segment == "temp":
        result += "@" + index + "\n"   + "D=A\n"  + "@5\n"  + "A=A+D\n"   + "D=M\n"  + "@SP\n"   + "A=M\n"  + "M=D\n"  + "@SP\n"   + "M=M+1\n"
      elif segment == "pointer":
        result += "@" + index + "\n"  + "D=A\n"  + "@3\n"  + "A=A+D\n"   + "D=M\n"  + "@SP\n"  + "A=M\n"  + "M=D\n"  + "@SP\n"  + "M=M+1\n"
      else:
        result += segment + " Aun no implementado, no se puede hacer push\n"
    elif command == "pop":
      result += "// pop " + segment + index + "\n"
      if segment == "static":
        result += "@SP\n"   + "AM=M-1\n"  + "D=M\n"  + "@" + self.nameFile + "." + index + "\n"  + "M=D\n"
      elif segment == "this":
        result += "@" + index + "\n"   + "D=A\n"  + "@THIS\n"  + "D=M+D\n"   + "@R13\n"  + "M=D\n"  + "@SP\n"   + "AM=M-1\n"  + "D=M\n"  + "@R13\n"   + "A=M\n"  + "M=D\n"
      elif segment == "that":
         result += "@" + index + "\n"   + "D=A\n"  + "@THAT\n"  + "D=M+D\n"   + "@R13\n"  + "M=D\n"  + "@SP\n"   + "AM=M-1\n"  + "D=M\n"  + "@R13\n"   + "A=M\n"  + "M=D\n"
      elif segment == "argument":
        result += "@" + index + "\n"   + "D=A\n"  + "@ARG\n"  + "D=M+D\n"   + "@R13\n"  + "M=D\n"  + "@SP\n"   + "AM=M-1\n"  + "D=M\n"  + "@R13\n"   + "A=M\n"  + "M=D\n"
      elif segment == "local":
        result += "@" + index + "\n"   + "D=A\n"  + "@LCL\n"  + "D=M+D\n"   + "@R13\n"  + "M=D\n"  + "@SP\n"   + "AM=M-1\n"  + "D=M\n"  + "@R13\n"   + "A=M\n"  + "M=D\n"
      elif segment == "pointer":
        result += "@" + index + "\n"   + "D=A\n"  + "@3\n"  + "D=A+D\n"   + "@R13\n"  + "M=D\n"  + "@SP\n"   + "AM=M-1\n"  + "D=M\n"  + "@R13\n"   + "A=M\n"  + "M=D\n"
      elif segment == "temp":
       result += "@" + index + "\n"   + "D=A\n"  + "@5\n"  + "D=A+D\n"   + "@R13\n"  + "M=D\n"  + "@SP\n"   + "AM=M-1\n"  + "D=M\n"  + "@R13\n"   + "A=M\n"  + "M=D\n"
      else:
        result += segment + " Aun no implementado, no se puede hacer pop\n"
    self.outfile.write(result)

  def writeError(self):
    self.outfile.write("Comando no reconocido!!\n")
    


def main():
  nameFile = sys.argv[1] #cargamos el nombre del archivo a traducir 
  normalize = parsing(nameFile + ".vm") #ejecutamos el metodo parsing para definir el tipo de operacion a realizar en condigo de maquina virtual 
  writer = traslator(nameFile + ".asm")#se pasa el nombre del archivo nuevo al metodo de traduccion 
  
  while normalize.whenStop():# el metodo .whenStop() retorna un booleano para detener el ciclo en el momento que no encuentre ninguna otra linea de codigo 
    normalize.step() #llamamos el metodo que verifica la existencia de comentarios y extrae solo el codigo traducible 
    type = normalize.orderType() #variable que refiere a el tipo de operacion a tealizar 
    if type == "push" or type == "pop": #ejecucion de la operacion de Push Pop en el metodo correspondiente 
      writer.writePushPop(type, normalize.arg1(), normalize.arg2())
    elif type == "math": # ejecucion de el metodo para operaciones aritmeticas 
      writer.writeArithmetic(normalize.order[0])
    else:
      writer.writeError()

if __name__ == "__main__":
  main()


