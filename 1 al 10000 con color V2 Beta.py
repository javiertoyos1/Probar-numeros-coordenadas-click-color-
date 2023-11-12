import pyautogui
import time
import keyboard
from PIL import ImageColor

# Definir el nombre del archivo donde se guardarán las coordenadas
coordenadas_file = 'coordenadas.txt'
ultimo_numero_file = 'ultimo_numero.txt'
color_file = 'color.txt'

# Preguntar si se desea continuar por el último número utilizado
use_last_number = pyautogui.confirm('¿Desea continuar por el último número utilizado?', buttons=['Sí', 'No'])
if use_last_number == 'Sí':
    try:
        with open(ultimo_numero_file, 'r') as f:
            ultimo_numero_str = f.readline().strip()
            i = int(ultimo_numero_str)
            
            # Leer las coordenadas guardadas del archivo
            with open(coordenadas_file, 'r') as f:
                coordenadas1_str = f.readline().strip()
                coordenadas2_str = f.readline().strip()
                coordenadas1 = tuple(map(int, coordenadas1_str.split(',')))
                coordenadas2 = tuple(map(int, coordenadas2_str.split(',')))
    except:
        i = 0
else:
    i = 0
    # Guardar el número 0 en el archivo
    with open(ultimo_numero_file, 'w') as f:
        f.write('0')

    # Preguntar si se desean utilizar las coordenadas guardadas o unas nuevas
    use_saved_coords = pyautogui.confirm('¿Desea utilizar las coordenadas guardadas?', buttons=['Sí', 'No'])
    if use_saved_coords == 'No':
        # Mostrar un cuadro de diálogo para que el usuario haga clic en la pantalla y establezca las coordenadas de la primera zona
        pyautogui.alert(text='Presiona Enter para establecer las coordenadas de la primera zona', title='Establecer coordenadas', button='OK')
        coordenadas1 = pyautogui.position()

        # Guardar las coordenadas en el archivo
        with open(coordenadas_file, 'w') as f:
            f.write(f"{coordenadas1[0]},{coordenadas1[1]}\n")

        # Mostrar otro cuadro de diálogo para que el usuario haga clic en la pantalla y establezca las coordenadas de la segunda zona
        pyautogui.alert(text='Presiona Enter para establecer las coordenadas de la segunda zona', title='Establecer coordenadas', button='OK')
        coordenadas2 = pyautogui.position()
        
        # Guardar las coordenadas en el archivo
        with open(coordenadas_file, 'a') as f:
            f.write(f"{coordenadas2[0]},{coordenadas2[1]}\n")
            
        pyautogui.moveTo(500, 500)
        # time.sleep(0.5)
        
        # Obtener y guardar el color del píxel en las coordenadas especificadas
        color = pyautogui.screenshot().getpixel(coordenadas2)
        with open(color_file, 'w') as f:
            f.write(f"{color[0]},{color[1]},{color[2]}")
            print(f"sssssaaaavvvveeedddddddd {color[0]},{color[1]},{color[2]}")

    else:
        # Leer las coordenadas guardadas del archivo
        with open(coordenadas_file, 'r') as f:
            coordenadas1_str = f.readline().strip()
            coordenadas2_str = f.readline().strip()
            coordenadas1 = tuple(map(int, coordenadas1_str.split(',')))
            coordenadas2 = tuple(map(int, coordenadas2_str.split(',')))

# Función para calcular la diferencia porcentual de los colores
def color_difference(color1, color2):
    return [abs((a - b) / ((a + b) / 2) * 100) if (a + b) / 2 != 0 else 0 for a, b in zip(color1, color2)]
    
# Ejecutar el bucle principal
with open(color_file, 'r') as f:
    saved_color_str = f.readline().strip()
    saved_color = tuple(map(int, saved_color_str.split(',')))
print('El color guardado es', saved_color)
for i in range(i, 10000):
    # Convertir i a una cadena de 4 caracteres rellenando con ceros a la izquierda
    num_str = str(i).zfill(4)

    # Pegar el número en las coordenadas de la primera zona especificada por el usuario
    pyautogui.doubleClick(coordenadas1)
    pyautogui.typewrite(num_str)

    # Hacer clic en la zona x, y deseada y esperar un segundo
    pyautogui.click(coordenadas2)
    pyautogui.moveTo(500, 500)
    # time.sleep(0.01)
    # Comprobar si el color del píxel en las coordenadas sigue siendo el mismo
    current_color = pyautogui.screenshot().getpixel(coordenadas2)
    print("current color: ", current_color)
    # with open(color_file, 'r') as f:
    #     saved_color_str = f.readline().strip()
    #     saved_color = tuple(map(int, saved_color_str.split(',')))
    color_diff = color_difference(current_color, saved_color)
    if any(diff > 20 for diff in color_diff):  # Si alguna diferencia es mayor que 10%, romper el bucle        
        print("diferencia es mayor que 10%, romper el bucle:",saved_color, "current:", current_color)
        print("dif es:", color_diff)
        with open(ultimo_numero_file, 'w') as f:
            f.write(str(i))
            print('el ultimo numero ha sido', i)
        break

    if keyboard.is_pressed('p'):  # HAY QUE MANTENER PULSADO PARA PARARLO
        pyautogui.alert('Presiona ENTER para continuar.')
    if keyboard.is_pressed('q'):  # HAY QUE MANTENER PULSADO PARA PARARLO
        with open(ultimo_numero_file, 'w') as f:
            f.write(str(i))
        break
