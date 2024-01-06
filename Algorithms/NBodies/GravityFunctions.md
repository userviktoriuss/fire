# Функции гравитации

## gravity()
Просто гравитация по закону всемирного тяготения двух тел с массой 1 кг.
![](pics/gravity.png)

## cut_gravity()
Гравитация, обрезанная константой по порогу _STOP_RADIUS_
![](pics/cut_gravity.png)

## gravity_with_sign()
Гравитация, отражённая относительно Ox по порогу _STOP_RADIUS_. Мотивация в том, чтобы тела останавливались относительно друг друга на расстоянии _STOP_RADIUS_
![](pics/gravity_with_sign.png)

## cut_gravity_with_sign()
Гравитация, обрезанная константой, причём константная часть отрицательная. Это ещё одна попытка заставить тела останавливаться на расстоянии _STOP_RADIUS_.
![](pics/cut_gravity_with_sign.png)

## zeroed_gravity()
Гравитация, обрезанная нулем по _STOP_RADIUS_.
![](pics/zeroed_gravity.png)

## smooth_gravity_with_sign()
Если расстояние больше _STOP_RADIUS_, то обычная гравитация. Иначе зелёная парабола с рисунка. 
![](pics/smooth_gravity_with_sign.png)