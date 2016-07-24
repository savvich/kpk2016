import turtle
turtle.color("red")
k=50
for i in range(5):
    k=k+20
    turtle.penup()
    turtle.goto(0,0)
    turtle.goto(k/2, k/2)
    turtle.right(90) # Повернуть курсор на 90 градусов вправо
    turtle.pendown()
    turtle.forward(k) # Пройти вперед расстояние k, если курсор опущен, то будет нарисована линия по пути слоедования
    turtle.right(90)
    turtle.forward(k)
    turtle.right(90)
    turtle.forward(k)
    turtle.right(90)
    turtle.forward(k)

turtle.done()