from turtle import *
#Введите количество квадратов
kol=int(input())
p=100
color('red', 'yellow')
begin_fill()
n=0
while n<kol:
 n=n+1
 p=p+100
 penup()
 goto(-p/2,-p/2)
 pendown()
 k=0
 while k<4:
     k=k+1
     forward(p)
     left(90)
end_fill()
done()