#!/usr/bin/python
import sys, os


def funcionmt2(cc):
  operador = operadores.get(cc[0], cc[0] + "no se encuentra ")
  asig = "M=M" + operador + "D\n"
  return popD + getM + asig

def funcionmt1(cc):
  operador = operadores.get(cc[0], cc[0] + "no se encuentra ")
  asig = "M=" + operador + "M\n"
  return getM + asig

def funcionbool(cc):
  global gtcont
  global ltcont
  global eqcont

  if cc[0] == "gt":
    name = "gtTrue" + str(gtcont)
    test = "@" + name + "\nD;JGT\n"
    gtcont += 1
  if cc[0] == "eq":
    name = "eqTrue" + str(eqcont)
    test = "@" + name + "\nD;JEQ\n"
    eqcont += 1
  if cc[0] == "lt":
    name = "ltTrue" + str(ltcont)
    test = "@" + name + "\nD;JLT\n"
    ltcont += 1
  
  label = "(" + name + ")\n"

  return popD + getM + diffTrue + test + makeFalse + label


def funcionpush(cc):
  sentencia = cc[1]
  index = cc[2]

  if sentencia == "constant":
    value = "@" + index + "\nD=A\n"
  elif sentencia == "static":
    value = "@" + fileName + "." + index + "\nD=M\n"
  else:
    if sentencia == "temp" or sentencia == "pointer":
      tpA = "A"
    else:
      tpA = "M"
    pointer = segPointers.get(sentencia, "Sentencia invalida: " + sentencia + "\n")
    indexD = "@" + index + "\nD=A\n"
    valueD = "@" + pointer + "\nA=" + tpA + "+D\nD=M\n"
    value = indexD + valueD

  return value + push

def funcionpop(cc):
  sentencia = cc[1]
  index = cc[2]

  if sentencia == "static":
    pointer = "@" + fileName + "." + index + "\n"
    return popD + pointer + "M=D\n"
  
  if sentencia == "temp" or sentencia == "pointer":
    tpA = "A"
  else:
    tpA = "M"
  pointer = segPointers.get(sentencia, "Sentencia invalida " + sentencia + "\n")
  indexD = "@" + index + "\nD=A\n"
  addressR13 = "@" + pointer + "\nD=" + tpA + "+D\n@R13\nM=D\n"
  change = "@R13\nA=M\nM=D\n"

  return indexD + addressR13 + popD + change


def initialize(file):
  file.write("\n///Iniciando..." + file.name + "\n") 


def translate(line):
  cc = line.split('/')[0].strip().split()
  if cc == []:
    return ''
  else:
    f = translations.get(cc[0], lambda x: "\n///" + cc[0] + " no se encuentra\n\n")
    return f(cc)
  

def main():
  arg = sys.argv[1]
  infiles = []

  if os.path.isfile(arg):
    path = os.path.dirname(arg)
    base = os.path.basename(arg)[:-3]
    infiles.append(base + ".vm") 
  elif os.path.isdir(arg):
    path = arg
    base = os.path.basename(arg)
    for file in os.listdir(arg):
      if file[-3:] == ".vm":
        infiles.append(file)

  outfile = open(os.path.join(path, base) + ".asm", "w")
  initialize(outfile)

  for f in infiles:
    global fileName 
    fileName = f[:-3]
    outfile.write("\n///Traduciendo:" + f + "\n")
    infile = open(os.path.join(path, f))
    for line in infile:
      outfile.write(translate(line))
    

translations = {
    "add": funcionmt2,
    "sub": funcionmt2,
    "or" : funcionmt2,
    "and": funcionmt2,
    "neg": funcionmt1,
    "not": funcionmt1,
    "eq" : funcionbool,
    "gt" : funcionbool,
    "lt" : funcionbool,
    "push" : funcionpush,
    "pop"  : funcionpop,
    }

gtcont = 0
ltcont = 0
eqcont = 0

popD = "@SP\nAM=M-1\nD=M\n"
getM = "@SP\nA=M-1\n"
diffTrue = "D=M-D\nM=-1\n"
makeFalse = "@SP\nA=M-1\nM=0\n"
push = "@SP\nA=M\nM=D\n@SP\nM=M+1\n"

operadores = {
    "sub" : "-",
    "add" : "+",
    "and" : "&",
    "or"  : "|",
    "neg" : "-",
    "not" : "!",
    }

segPointers = {
    "argument" : "ARG",
    "this" : "THIS",
    "that" : "THAT",
    "local" : "LCL",
    "temp" : "5",
    "pointer" : "3"
    }



if __name__ == "__main__":
  main()

