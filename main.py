import time
import util
from parametros import URL, PATH, WAIT_TIME  

periodo = util.get_date() 

print("[1] Descargar cartera " + periodo)
print("[2] Seleccionar periodo para descargar") 

a = input("Seleccione una opción: ")

while a not in {'1', '2'}:
    input("Por favor, seleccione una opción válida: ") 

if a == '2':
    periodo = input("Ingrese el periodo a descargar (formato: YYYYMM ej: 202209): ") 

success = False
message = f'La Cartera agregada para el periodo {periodo[:4]}-{periodo[4:]} aún no se encuentra disponible'

while not success:
    try:
        df = util.scrap_SP(URL.format(periodo))
        success = True
    except AttributeError:
        print('\b'*len(message) + message, end='', flush=True)
        time.sleep(WAIT_TIME)

df.to_excel(PATH.format(periodo), index=False, sheet_name='Hoja1')

print('Se procesó la cartera')