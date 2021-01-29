// push constant111
@111
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant333
@333
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant888
@888
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop static8
@SP
AM=M-1
D=M
@StaticTest.8
M=D
// pop static3
@SP
AM=M-1
D=M
@StaticTest.3
M=D
// pop static1
@SP
AM=M-1
D=M
@StaticTest.1
M=D
// push static3
@StaticTest.3
D=M
@SP
A=M
M=D
@SP
M=M+1
// push static1
@StaticTest.1
D=M
@SP
A=M
M=D
@SP
M=M+1
// sub
@SP
AM=M-1
D=M
@SP
AM=M-1
M=M-D
@SP
M=M+1
// push static8
@StaticTest.8
D=M
@SP
A=M
M=D
@SP
M=M+1
// add
@SP
AM=M-1
D=M
@SP
AM=M-1
M=D+M
@SP
M=M+1
