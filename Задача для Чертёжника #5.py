from turtle import *
color('red', 'yellow')
begin_fill()
while True:
    forward(50)
    left(45)
    if abs(pos()) < 1:
        break
end_fill()
done()