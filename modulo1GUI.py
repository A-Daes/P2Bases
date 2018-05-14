from Tkinter import *
from tkFileDialog import askopenfilename
from functools import partial
import insertar_cliente
import get_client
import get_data

filterList = []
lastTable = ["cliente"]
''' 
TO-DO: 
Full focus de ventanas, ie no dejar que me ponga en otra ventana mientras estoy editando algo
Faltan todo lo interno. Tengo que leer mas de psycopg, para poder hacerlas NECESITO hacer las tablas.
'''

'''
FUNCTIONS
(Functions exclusive to the GUI, aka button commands and hotkeys.)

Functions related to actual inner workings are imported from their respective libraries
'''

#Abrir ventana para elegir filtros y mostrar filas

def fShow():
	sql = filterList[0]
	dListboxRows.delete(0, END)
	for item in get_data.get_data(sql):
		dListboxRows.insert(END, item)


def fSelect():
	##Toplevel
	fsSelectWindow = Toplevel()
	fsSelectWindow.title("Agregar filtro")

	##Funciones internas
	def fsApply():
		filtro = "SELECT * FROM  " + lastTable[len(lastTable) - 1] + " WHERE " + fsVariableCampo1.get() + " " + fsVariableCond1.get() + " " + fsEntryCondicion.get()
		filterList.append(filtro)
		print filterList

		if len(filterList) > 0:
			fBotonEliminar.configure(state = NORMAL)
		else:
			fBotonEliminar.configure(state = DISABLED)
		fsSelectWindow.destroy()

	##Labels

	fsLabel1 = Label(fsSelectWindow, text="Condicion:")

	##Variables
	fsVariableCampo1 = StringVar(fsSelectWindow)
	fsVariableCampo1.set("ID") # default value

	fsVariableCond1 = StringVar(fsSelectWindow)
	fsVariableCond1.set("=")

	##Entry

	fsEntryCondicion = Entry(fsSelectWindow)

	##OptionMenus
	fsMenuFilterCampo1 = OptionMenu(fsSelectWindow, fsVariableCampo1, "ID", "NOMBRE", "APELLIDO", "TELEFONO", "DIRECCION", "CORREO", "FECHA DE NACIMIENTO", "NACIONALIDAD", "EMPRESA")
	fsMenuFilterCond1 = OptionMenu(fsSelectWindow, fsVariableCond1, "=", "<", ">", "NOT", "LIKE")

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
		filterList.remove(fdVariableFilter.get())
		if (len(filterList) == 0):
			fBotonEliminar.configure(state=DISABLED)
			fdDeleteWindow.destroy()
		else:
			pass

	def fdClose():
		fdDeleteWindow.destroy()

	##Labels
	fdLabel = Label(fdDeleteWindow, text="Filtro:")

	##Variables
	fdVariableFilter = StringVar(fdDeleteWindow)
	fdVariableFilter.set(filterList[0]) #Default value

	##OptionMenus

	fdMenuFilter = OptionMenu(fdDeleteWindow, fdVariableFilter, *filterList)

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
	photoFileName = ""




	##Funciones internas

	def ccAgregar():

		##Add data to a default insert string
		sendData = []
		sendData.append(ccEntryNombre.get())
		sendData.append(ccEntryApellido.get())
		sendData.append(ccEntryTel.get())
		sendData.append(ccEntryAddress.get())
		sendData.append(ccEntryMail.get())
		sendData.append(ccEntryDate.get())
		sendData.append(ccEntryNation.get())
		sendData.append(ccEntryAddress.get())
		sendData.append(ccHiddenPhotoEntry.get())

		print sendData

		dataString = "INSERT INTO Cliente VALUES('" + sendData[0] + "','" + sendData[1] + "'," + sendData[2] + ",'" + sendData[3] + "','" + sendData[4] + "'," + sendData[5] + ",'" + sendData[6] + ",'" + sendData[7] + "'," + sendData[8] + ")"

		insertar_cliente.insert_client(dataString)


	def ccCerrar():
		ccCreateWindow.destroy()

	def ccEmptyCallback(event):
		if (ccEntryDate.get() == "DD/MM/YYYY"):
			ccEntryDate.delete(0, "end")
			ccFirstTime = False
			return None
		else:
			return None

	def ccChoosePhoto():
		filename = askopenfilename()
		if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
			photoFileName = filename
			ccHiddenPhotoEntry.insert(0, photoFileName)
			print photoFileName
		else:
			##ErrorPopup
			print "lol"



	##Frames

	ccInputFrame = Frame(ccCreateWindow)
	ccInputFrameLower = Frame(ccCreateWindow)
	ccBotonesFrame = Frame(ccCreateWindow)

	##Labels

	ccInfoLabel = Label(ccInputFrame, text = "Datos")
	ccNombreLabel = Label(ccInputFrame, text = "Nombre:")
	ccApellidoLabel = Label(ccInputFrame, text = "Apellido:")
	ccTelLabel = Label(ccInputFrame, text="Telefono:")
	ccAddressLabel = Label(ccInputFrame, text="Direccion:")
	ccMailLabel = Label(ccInputFrame, text="Correo:")
	ccBirthLabel = Label(ccInputFrameLower, text = "Fecha de Nacimiento: ")
	ccNationLabel = Label(ccInputFrameLower, text = "Nacionalidad:")
	ccEmpresaLabel = Label(ccInputFrameLower, text = "Empresa:")
	ccFotoLabel = Label(ccInputFrameLower, text = "Foto:")

	##TextEntry

	ccEntryNombre = Entry(ccInputFrame)
	ccEntryApellido = Entry(ccInputFrame, text = "Apellido")
	ccEntryTel = Entry(ccInputFrame, text = "Telefono")
	ccEntryAddress = Entry(ccInputFrame, text = "Direccion")
	ccEntryMail = Entry(ccInputFrame)
	ccEntryDate = Entry(ccInputFrameLower)
	ccEntryDate.bind("<Button-1>", ccEmptyCallback)
	ccEntryDate.insert(0, "DD/MM/YYYY")
	ccEntryNation = Entry(ccInputFrameLower)
	ccEntryEmpresa = Entry(ccInputFrameLower)
	ccHiddenPhotoEntry = Entry(ccInputFrameLower)


	##Botones

	ccBotonFoto = Button(ccInputFrameLower, text ="Elegir foto...", command = ccChoosePhoto)
	ccBotonAgregar = Button(ccBotonesFrame, text = "Agregar", command=ccAgregar)
	ccBotonCerrar = Button(ccBotonesFrame, text = "Cerrar", command=ccCerrar)

	##Packing

	ccInfoLabel.pack(side=TOP)
	ccNombreLabel.pack(side=LEFT)
	ccEntryNombre.pack(side=LEFT)
	ccApellidoLabel.pack(side=LEFT)
	ccEntryApellido.pack(side=LEFT)
	ccTelLabel.pack(side=LEFT)
	ccEntryTel.pack(side=LEFT)
	ccAddressLabel.pack(side=LEFT)
	ccEntryAddress.pack(side=LEFT)
	ccMailLabel.pack(side=LEFT)
	ccEntryMail.pack(side=LEFT)
	ccBirthLabel.pack(side=LEFT)
	ccEntryDate.pack(side=LEFT)
	ccNationLabel.pack(side=LEFT)
	ccEntryNation.pack(side=LEFT)
	ccEmpresaLabel.pack(side=LEFT)
	ccEntryEmpresa.pack(side=LEFT)
	ccFotoLabel.pack(side=LEFT)
	ccBotonFoto.pack(side=LEFT)
	ccBotonAgregar.pack(side=RIGHT)
	ccBotonCerrar.pack(side=RIGHT)


	ccInputFrame.pack(side=TOP)
	ccInputFrameLower.pack(side=TOP)
	ccBotonesFrame.pack(side=BOTTOM)

	
def cActualizar():
#Abrir ventana para crear nuevo cliente
	##TopLevel

	clientData = ["DefaultID", "Default", "Last", "num", "Address", "Mail", "1/1/1", "Default", "Default", "C:"]
	caCreateWindow = Toplevel()
	caCreateWindow.title("Actualizar cliente")
	photoFileName = ""


	##Funciones internas

	def caActualizar():

		##Add data to a default insert string
		sendData = []
		sendData.append(caEntryNombre.get())
		sendData.append(caEntryApellido.get())
		sendData.append(caEntryTel.get())
		sendData.append(caEntryAddress.get())
		sendData.append(caEntryMail.get())
		sendData.append(caEntryDate.get())
		sendData.append(caEntryNation.get())
		sendData.append(caEntryAddress.get())
		sendData.append(caHiddenPhotoEntry.get())

		print sendData

		dataString = "INSERT INTO Cliente VALUES('" + sendData[0] + "','" + sendData[1] + "'," + sendData[2] + ",'" + sendData[3] + "','" + sendData[4] + "'," + sendData[5] + ",'" + sendData[6] + ",'" + sendData[7] + "'," + sendData[8] + ")"

		insertar_cliente.insert_client(dataString)


	def caCerrar():
		ccCreateWindow.destroy()

	def caChoosePhoto():
		filename = askopenfilename()
		if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
			photoFileName = filename
			caHiddenPhotoEntry.insert(0, photoFileName)
			print photoFileName
		else:
			##ErrorPopup
			print "lol"



	##Frames

	caInputFrame = Frame(caCreateWindow)
	caInputFrameLower = Frame(caCreateWindow)
	caBotonesFrame = Frame(caCreateWindow)

	##Labels

	caInfoLabel = Label(caInputFrame, text = "Datos")
	caNombreLabel = Label(caInputFrame, text = "Nombre:")
	caApellidoLabel = Label(caInputFrame, text = "Apellido:")
	caTelLabel = Label(caInputFrame, text="Telefono:")
	caAddressLabel = Label(caInputFrame, text="Direcaion:")
	caMailLabel = Label(caInputFrame, text="Correo:")
	caBirthLabel = Label(caInputFrameLower, text = "Fecha de Nacimiento: ")
	caNationLabel = Label(caInputFrameLower, text = "Nacionalidad:")
	caEmpresaLabel = Label(caInputFrameLower, text = "Empresa:")
	caFotoLabel = Label(caInputFrameLower, text = "Foto:")

	##TextEntry

	caEntryNombre = Entry(caInputFrame)
	caEntryNombre.insert(0, clientData[1])
	
	caEntryApellido = Entry(caInputFrame)
	caEntryApellido.insert(0, clientData[2])	
	
	caEntryTel = Entry(caInputFrame, text = "Telefono")
	caEntryTel.insert(0, clientData[3])	
	
	caEntryAddress = Entry(caInputFrame, text = "Direccion")
	caEntryAddress.insert(0, clientData[4])	

	caEntryMail = Entry(caInputFrame)
	caEntryMail.insert(0, clientData[5])	

	caEntryDate = Entry(caInputFrameLower)
	caEntryDate.insert(0, clientData[6])

	caEntryNation = Entry(caInputFrameLower)
	caEntryNation.insert(0, clientData[7])	
	
	caEntryEmpresa = Entry(caInputFrameLower)
	caEntryEmpresa.insert(0, clientData[8])	
	
	caHiddenPhotoEntry = Entry(caInputFrameLower)
	caHiddenPhotoEntry.insert(0, clientData[9])	


	##Botones

	caBotonFoto = Button(caInputFrameLower, text ="Elegir foto...", command = caChoosePhoto)
	caBotonAgregar = Button(caBotonesFrame, text = "Actualizar", command=caActualizar)
	caBotonCerrar = Button(caBotonesFrame, text = "Cerrar", command=caCerrar)

	##Packing

	caInfoLabel.pack(side=TOP)
	caNombreLabel.pack(side=LEFT)
	caEntryNombre.pack(side=LEFT)
	caApellidoLabel.pack(side=LEFT)
	caEntryApellido.pack(side=LEFT)
	caTelLabel.pack(side=LEFT)
	caEntryTel.pack(side=LEFT)
	caAddressLabel.pack(side=LEFT)
	caEntryAddress.pack(side=LEFT)
	caMailLabel.pack(side=LEFT)
	caEntryMail.pack(side=LEFT)
	caBirthLabel.pack(side=LEFT)
	caEntryDate.pack(side=LEFT)
	caNationLabel.pack(side=LEFT)
	caEntryNation.pack(side=LEFT)
	caEmpresaLabel.pack(side=LEFT)
	caEntryEmpresa.pack(side=LEFT)
	caFotoLabel.pack(side=LEFT)
	caBotonFoto.pack(side=LEFT)
	caBotonAgregar.pack(side=RIGHT)
	caBotonCerrar.pack(side=RIGHT)


	caInputFrame.pack(side=TOP)
	caInputFrameLower.pack(side=TOP)
	caBotonesFrame.pack(side=BOTTOM)


def cEliminar():
	#Verificar si se quiere eliminar a cliente en cMenuEliminar
	ceAlertWindow = Toplevel()
	ceAlertWindow.title("Eliminar?")

	
	def ceDelete():
		pass 
		##delete_client

	##Labels
	ceEliminarLabel = Label(ceAlertWindow, text="Seguro que desea eliminar a []?")

	ceBotonSi = Button(ceAlertWindow, text="Si")
	ceBotonNo = Button(ceAlertWindow, text="No")

	ceEliminarLabel.pack(side=TOP)

	ceBotonSi.pack(side=BOTTOM)
	ceBotonNo.pack(side=BOTTOM)
	

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
- Mostrar filas con filtros [show:X [Button: X, Function: ] , select filter: [newWindow: X, function: X, delete: [Window: x, function:X ]] ]
- Crear cliente nuevo [Button: X, Window:X , Function: X]
- Actualizar datos cliente [Butoon: X, Window:X , Function: X]
- Eliminar cliente (verificacion) [Button: X, AlertBox: , Function: ]
- Creacion de campos adicionales (desde PostgreSQL y desde el programa en si) [Boton: X, RestrictionWindow:X , Function:X ]
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

cMenuEliminaroActualizar = OptionMenu(ClientesFrame, cVariable, "ID0", "ID1", "ID2")
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
if len(filterList) ==0:
	fBotonEliminar.configure(state=DISABLED)
else:
	pass

cLabel.pack(side=TOP)
cBotonCrear.pack(side=LEFT)
cBotonEliminar.pack(side=RIGHT)
cBotonActualizar.pack(side=RIGHT)
cMenuEliminaroActualizar.pack(side=RIGHT)

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
