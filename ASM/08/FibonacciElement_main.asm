
///Iniciando...FibonacciElement_main.asm

///Traduciendo:FibonacciElement_main.vm

///function no se encuentra

@0
D=A
@ARG
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
@SP
A=M-1
D=M-D
M=-1
@ltTrue0
D;JLT
@SP
A=M-1
M=0
(ltTrue0)

///if-goto no se encuentra


///goto no se encuentra


///label no se encuentra

@0
D=A
@ARG
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1

///return no se encuentra


///label no se encuentra

@0
D=A
@ARG
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
@SP
A=M-1
M=M-D

///call no se encuentra

@0
D=A
@ARG
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
@SP
A=M-1
M=M-D

///call no se encuentra

@SP
AM=M-1
D=M
@SP
A=M-1
M=M+D

///return no se encuentra

