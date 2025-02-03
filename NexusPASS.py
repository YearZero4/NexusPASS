from prettytable import PrettyTable
import mysql.connector, os, pyfiglet, time, sys
from colorama import Fore, init, Style
init(autoreset=True)

GREEN=f'{Fore.GREEN}{Style.BRIGHT}'
WHITE=f'{Fore.WHITE}{Style.BRIGHT}'
RED=f'{Fore.RED}{Style.BRIGHT}'

def showinfo(phrase, color):
 for letter in phrase:
  sys.stdout.write(color + letter)
  sys.stdout.flush()
  time.sleep(0.03)

def clear():
 os.system('cls' if os.name == 'nt' else 'clear')

def banner():
 banner=pyfiglet.figlet_format("NexusPASS")
 print(banner)

def security():
 banner()
 user=os.getlogin()
 rfolder=os.path.join('C:\\', 'Users', user, 'AppData', 'Local', 'NexusPASS')
 rpass=os.path.join(rfolder, 'password.txt')
 if not os.path.exists(rfolder):
  os.makedirs(rfolder)

 if not os.path.exists(rpass):
  pass0=input('[+] INTRODUZCA CLAVE PARA ACCEDER A TUS DATOS => ' + GREEN)
  with open(rpass, 'w') as f:
   f.write(pass0)
   f.close()
  showinfo(f'[+] SEGURIDAD APLICADA CON EXITO', GREEN)
  time.sleep(3)
  os.system('cls')
  security()
 else:
  pass0=input(GREEN + '[+]' + WHITE + ' CLAVE DE ACCESO => ' + GREEN)
  with open(rpass, 'r') as f:
   pass1=f.read()
   if pass0 == pass1:
    showinfo('Ingresastes exitosamente', GREEN)
   else:
    showinfo(f'Clave invalida, por favor intente de nuevo', RED)
    time.sleep(3)
    clear()
    security()

clear()
security()

def inputs():
    return [input('[+] Correo o Usuario => '), input('[+] Clave de cuenta => ')]

def start():
 table=PrettyTable()
 table.field_names=['ID', 'PLATAFORMA', 'USUARIO O EMAIL', 'PASSWORD']
 conexion = mysql.connector.connect(
  host='localhost',
  user='root',
  password='',
  database='bdpython'
 )
 cursor = conexion.cursor()
 def ver_datos():
  cursor.execute("SELECT * FROM datos")
  resultados = cursor.fetchall()
  if not resultados:
   print("No se encontraron datos.")
  else:
   for fila in resultados:
    table.add_row([f"{GREEN}[{fila[0]}]{WHITE}", fila[1], fila[2], fila[3]])
   print(table)

 def all_delete():
  id0=[]
  cursor.execute("SELECT * FROM datos")
  resultados = cursor.fetchall()
  for fila in resultados:
   id0.append(fila[0])
  print('TODOS LOS DATOS ELIMINADOS CON EXITO')
  return id0
 def agregar_dato(platform, usmail, pass0):
  cursor.execute("INSERT INTO datos (PLATAFORMA, EMAIL_USER, PASSWORD) VALUES (%s, %s, %s)", (platform, usmail, pass0))
  conexion.commit()
  print(f"\n{GREEN}Se Agregaron Nuevos Datos")

 def editar_dato(id, usmail, pass0):
  cursor.execute("UPDATE datos SET EMAIL_USER = %s, PASSWORD = %s WHERE id = %s", (usmail, pass0, id))
  conexion.commit()
  print(f"\n{GREEN}Se modificaron los datos")

 def eliminar_dato(id):
  cursor.execute("DELETE FROM datos WHERE id = %s", (id,))
  conexion.commit()
  print(f"\n{GREEN}Dato eliminado exitosamente")

 print(f''' \n----> SISTEMA DE CONTROL DE CUENTAS <---- \n
\t{GREEN}[1]{WHITE} VER TODOS LOS DATOS ALMACEMADOS
\t{GREEN}[2]{WHITE} AGREGAR DATOS NUEVOS
\t{GREEN}[3]{WHITE} EDITAR DATOS GUARDADOS
\t{GREEN}[4]{WHITE} BORRAR 1 FILA DE LA BASE DE DATOS
\t{GREEN}[5]{WHITE} BORRAR TODO DE LA BASE DE DATOS
 ''')
 opc=input('[+] Seleccionar Opcion => ')
 print('')
 acciones = {
 "1": ver_datos,
 "2": lambda: agregar_dato(input('[+] Plataforma => '), *inputs()),
 "3": lambda: editar_dato(input('[+] Dime el ID que deseas modificar => '), *inputs()),
 "4": lambda: eliminar_dato(input('[+] Dime el ID que deseas modificar => ')),
 "5": lambda: [eliminar_dato(i) for i in all_delete()]
 }
 accion = acciones.get(opc)
 if accion:
  accion()
 input(f'\n{GREEN}Presione [ENTER] Para Continuar...{WHITE}')
 clear()
 banner()
 start()
try:
 start()
except mysql.connector.errors.InterfaceError:
 print('Error al conectarse a base de datos MYSQL')


