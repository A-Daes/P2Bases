from Tkinter import *
from functools import partial


''' 
TO-DO: 
Full focus de ventanas, ie no dejar que me ponga en otra ventana mientras estoy editando algo
'''

'''
FUNCTIONS
(Functions exclusive to the GUI, aka button commands and hotkeys.)

Functions related to actual inner workings are imported from their respective libraries
'''

#Abrir ventana para elegir filtros y mostrar filas

def fShow():
	#Muestra en dListboxRows las filas basadas en el filtro seleccionado
	pass


def fSelect():
	##Toplevel
	fsSelectWindow = Toplevel()
	fsSelectWindow.title("Agregar filtro")

	##Funciones internas
	def fsApply():
		##Hacer filtro
		fsSelectWindow.destroy()

	##Labels

	fsLabel1 = Label(fsSelectWindow, text="Condicion:")

	##Variables
	fsVariableCampo1 = StringVar(fsSelectWindow)
	fsVariableCampo1.set("ID") # default value

	fsVariableCond1 = StringVar(fsSelectWindow)
	fsVariableCond1.set("Igual a:")

	##Entry

	fsEntryCondicion = Entry(fsSelectWindow)

	##OptionMenus
	fsMenuFilterCampo1 = OptionMenu(fsSelectWindow, fsVariableCampo1, "ID", "NOMBRE", "TELEFONO", "DIRECCION")
	fsMenuFilterCond1 = OptionMenu(fsSelectWindow, fsVariableCond1, "Igual a:", "Menor a:", "Mayor a:", "Distinto a:", "Contiene: ")

	##Buttons

	fsBotonApply = Button(fsSelectWindow, text = "Aplicar", command = fsApply)


	##Packing

	fsLabel1.pack(side=TOP)
	fsMenuFilterCampo1.pack(side=LEFT)
	fsMenuFilterCond1.pack(side=LEFT)
	fsEntryCondicion.pack(side=LEFT)
	fsBotonApply.pack()


def fDelete():
	##TopLevel

	fdDeleteWindow = Toplevel()
	fdDeleteWindow.title("Eliminar Filtro")

	##Funciones internas
	def fdApply():
		pass
		#Eliminar filtro seleccionado

	def fdClose():
		fdDeleteWindow.destroy()

	##Labels
	fdLabel = Label(fdDeleteWindow, text="Filtro:")

	##Variables
	fdVariableFilter = StringVar(fdDeleteWindow)
	fdVariableFilter.set("Filtro 1: ID > X") #Default value

	##OptionMenus

	fdMenuFilter = OptionMenu(fdDeleteWindow, fdVariableFilter, "Filtro 1: ID > X", "Filtro 2: NUMERO CONTAINS A")

	##Buttons

	fdButtonDelete = Button(fdDeleteWindow, text = "Eliminar", command=fdApply)
	fdButtonClose = Button(fdDeleteWindow, text = "OK", command=fdClose)

	##Packing
	fdLabel.pack(side=LEFT)
	fdMenuFilter.pack(side=LEFT)
	fdButtonDelete.pack(side=LEFT)
	fdButtonClose.pack(side=BOTTOM)

	#eliminar filtro


def cCrear():
	#Abrir ventana para crear nuevo cliente
	##TopLevel
	ccCreateWindow = Toplevel()
	ccCreateWindow.title("Crear cliente")

	##Funciones internas

	
def cActualizar():
	#Abrir ventana para actualizar cliente
	pass

def cEliminar():
	#Verificar si se quiere eliminar a cliente en cMenuEliminar
	pass

def aAgregar():
	#Agregar a la base de datos el campo segun los datos en aTextNombre, aMenuTipo y mostrar una ventana para pedir restricciones
	pass


'''
WINDOW
Main window and all its components
'''


### ROOT 

root = Tk()
root.title("Aegis CRM")

### FRAMES

'''
Modulo 1:
- Mostrar filas con filtros [show: [Button: X, Function: ] , select filter: [newWindow: X, function: 1/2, delete: [Window: x, function: ]] ]
- Crear cliente nuevo [Button: X, Window: , Function: ]
- Actualizar datos cliente [Butoon: X, Window: , Function: ]
- Eliminar cliente (verificacion) [Button: X, AlertBox: , Function: ]
- Creacion de campos adicionales (desde PostgreSQL y desde el programa en si) [Boton: X, RestrictionWindow: , Function: ]
'''

Modulo1Frame = Frame(root)

FiltrosBFrame = Frame(Modulo1Frame)
ClientesFrame = Frame(Modulo1Frame)
CamposFrame = Frame(Modulo1Frame)
DisplayFrame = Frame(Modulo1Frame)


'''
Modulo 2:
WIP
'''


## LABELS
fLabel = Label(FiltrosBFrame, text="Filtros y Filas")
cLabel = Label(ClientesFrame, text="Opciones de Cliente")
aLabel = Label(CamposFrame, text="Agregar Campo")
aLabelNombre = Label(CamposFrame, text="Nombre de campo")
aLabelTipo = Label(CamposFrame, text="Tipo de Campo")
dLabel = Label(DisplayFrame, text="Filas")

##TEXT ENTRY

aTextNombre = Entry(CamposFrame)

### BUTTONS

fBotonShow = Button(FiltrosBFrame, text="Mostrar Filas", command = fShow)
fBotonSelect= Button(FiltrosBFrame, text="Agregar filtro", command = fSelect)
fBotonEliminar = Button(FiltrosBFrame, text="Eliminar filtro", command= fDelete)

cBotonCrear = Button(ClientesFrame, text="Crear Cliente", command = cCrear)
cBotonActualizar = Button(ClientesFrame, text="Actualizar cliente", command = cActualizar)
cBotonEliminar = Button(ClientesFrame, text="Eliminar cliente", command = cEliminar)

aBotonAgregar = Button(CamposFrame, text="Agregar Nuevo campo", command = aAgregar)

### VARIABLES

cVariable = StringVar(ClientesFrame)
cVariable.set("ID0") # default value

aVariableTipo = StringVar(CamposFrame)
aVariableTipo.set("int") # default value

### OPTIONMENUS

cMenuEliminar = OptionMenu(ClientesFrame, cVariable, "ID0", "ID1", "ID2")
aMenuTipo = OptionMenu(CamposFrame, aVariableTipo, "int", "date", "string", "char", "...")

### LISTBOXES

dScrollbar = Scrollbar(DisplayFrame, orient=VERTICAL)
dListboxRows = Listbox(DisplayFrame, yscrollcommand=dScrollbar.set)
dScrollbar.configure(command=dListboxRows.yview)


### PACKING

fLabel.pack(side=TOP)
fBotonShow.pack(side=LEFT)
fBotonSelect.pack(side=RIGHT)
fBotonEliminar.pack(side=RIGHT)

cLabel.pack(side=TOP)
cBotonCrear.pack(side=LEFT)
cBotonActualizar.pack(side=LEFT)
cBotonEliminar.pack(side=RIGHT)
cMenuEliminar.pack(side=RIGHT)

aLabel.pack(side=TOP)
aBotonAgregar.pack(side=RIGHT)
aMenuTipo.pack(side=RIGHT)
aLabelTipo.pack(side=RIGHT)
aTextNombre.pack(side=RIGHT)
aLabelNombre.pack(side=RIGHT)

dLabel.pack(side=TOP)
dListboxRows.pack(side=LEFT, fill=BOTH, expand=1)
dScrollbar.pack(side=RIGHT, fill=Y)


##FRAMES

Modulo1Frame.pack(fill=BOTH, expand=1)
FiltrosBFrame.pack(side=TOP,fill=X)
ClientesFrame.pack(side=TOP, fill=X)
CamposFrame.pack(fill=X)
DisplayFrame.pack(side=BOTTOM,fill=BOTH, expand=1)


###MAINLOOP
root.mainloop()