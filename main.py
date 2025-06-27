calificaciones = []
nota = 1
notas = 0

while nota <= 5:
    try:
        notas = float(input(f"Ingrese la nota {nota}: "))
        if notas < 0 or notas > 5:
            print(f"La calificacion {notas} no es valida")
        else:
            calificaciones.append(notas)
            nota += 1
    except:
        print("ERROR")

final = sum(calificaciones) / 5

if final < 3:
    print(f"El estudinate a perdido con {final}")
else:
    print(f"El estudiante aprobo con {final}")