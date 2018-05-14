
from __future__ import print_function
from Tkinter import *
from tkFileDialog import askopenfilename
from functools import partial
import insertar_cliente
import get_client
import get_data
import re
from pprint import pprint
import tweepy
import json
from pymongo import *


##CLASSES
MONGO_HOST = "mongodb+srv://aegistk14104:aegistk14104@cc3040alv14104-dawge.mongodb.net/test?retryWrites=true"

WORDS = ["#Celebridade"]

class StreamListener(tweepy.StreamListener):    
    #This is a class provided by tweepy to access the Twitter Streaming API. 

    def on_connect(self):
        # Called initially to connect to the Streaming API
        print("You are now connected to the streaming API.")
 
    def on_error(self, status_code):
        # On error - if an error occurs, display the error / status code
        print('An Error has occured: ' + repr(status_code))
        return False
 
    def on_data(self, data):
        #This is the meat of the script...it connects to your mongoDB and stores the tweet
        try:
            client = MongoClient(MONGO_HOST)
            
            # Use twitterdb database. If it doesn't exist, it will be created.
            db = client.twitterdb
    
            # Decode the JSON from Twitter
            datajson = json.loads(data)
            
            #grab the 'created_at' data from the Tweet to use for display
            created_at = datajson['created_at']

            #print out a message to the screen that we have collected a tweet
            print("Tweet collected at " + str(created_at))
            
            #insert the data into the mongoDB into a collection called twitter_search
            #if twitter_search doesn't exist, it will be created.
            db.twitter_search.insert(datajson)
        except Exception as e:
           print(e)



#Set up the listener. The 'wait_on_rate_limit=True' is needed to help with Twitter API rate limiting.


filterList = []
lastTable = ["cliente"]
clientesIdList = get_data.get_data(""" SELECT "ID" FROM public."Cliente" ORDER BY "ID" ASC """)

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
	if len(filterList) ==0:
		sql = """SELECT * FROM public."Cliente" ORDER BY "ID" ASC """
	else:
		sql = filterList[0]
	dListboxRows.delete(0, END)
	data = get_data.get_data(sql)
	for item in get_data.get_data(sql):
		dListboxRows.insert(END, item)


def fSelect():
	##Toplevel
	fsSelectWindow = Toplevel()
	fsSelectWindow.title("Agregar filtro")

	##Funciones internas
	def fsApply():
		filtro = """SELECT nombre, apellido, telefono, direccion, correo, "fecha de nacimiento", nacionalidad, empresa, "codigo foto", "ID"
	FROM public."Cliente"
	WHERE {0} {1} {2} """.format(fsVariableCampo1.get(), fsVariableCond1.get(), fsEntryCondicion.get())

		filterList.append(filtro)
		print (filterList)

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


		dataString = """INSERT INTO public."Cliente"(
	nombre, apellido, telefono, direccion, correo, "fecha de nacimiento", nacionalidad, empresa, "codigo foto")
	VALUES ('{}', '{}', {}, '{}', '{}', '{}', '{}', '{}', '{}');""".format(sendData[0], sendData[1],sendData[2], sendData[3],sendData[4], sendData[5],sendData[6], sendData[7],sendData[8])

		print (dataString)
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
			print (photoFileName)
		else:
			##ErrorPopup
			print ("lol")



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

	clienteid = cVariable.get()
	clienteid = re.sub("\D", "", clienteid)
	clientData = get_client.get_client(clienteid)
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


		dataString = """UPDATE public."Cliente"
	SET nombre='{}', apellido='{}', telefono={}, direccion='{}', correo='{}', "fecha de nacimiento"='{}', nacionalidad='{}', empresa='{}', "codigo foto"='{}'
	WHERE "ID" = {}; """.format(sendData[0], sendData[1],sendData[2], sendData[3],sendData[4], sendData[5],sendData[6], sendData[7],sendData[8], clienteid)
		insertar_cliente.insert_client(dataString)


	def caCerrar():
		caCreateWindow.destroy()

	def caChoosePhoto():
		filename = askopenfilename()
		if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
			photoFileName = filename
			caHiddenPhotoEntry.insert(0, photoFileName)
		else:
			##ErrorPopup
			pass


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
		caEntryNombre.insert(0, clientData[0])
		
		caEntryApellido = Entry(caInputFrame)
		caEntryApellido.insert(0, clientData[1])	
		
		caEntryTel = Entry(caInputFrame, text = "Telefono")
		caEntryTel.insert(0, clientData[2])	
		
		caEntryAddress = Entry(caInputFrame, text = "Direccion")
		caEntryAddress.insert(0, clientData[3])	

		caEntryMail = Entry(caInputFrame)
		caEntryMail.insert(0, clientData[4])	

		caEntryDate = Entry(caInputFrameLower)
		caEntryDate.insert(0, clientData[5])

		caEntryNation = Entry(caInputFrameLower)
		caEntryNation.insert(0, clientData[6])	
		
		caEntryEmpresa = Entry(caInputFrameLower)
		caEntryEmpresa.insert(0, clientData[7])	
		
		caHiddenPhotoEntry = Entry(caInputFrameLower)
		caHiddenPhotoEntry.insert(0, clientData[8])	


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
	clienteid = cVariable.get()
	clienteid = re.sub("\D", "", clienteid)
	ceAlertWindow = Toplevel()
	ceAlertWindow.title("Eliminar?")

	
	def ceDelete():
		sql = """DELETE FROM public."Cliente"
	WHERE public."Cliente"."ID" = {} """.format(clienteid)
		insertar_cliente.insert_client(sql)
		ceAlertWindow.destroy()

	def ceDestroy():
		ceAlertWindow.destroy()

	##Labels
	ceEliminarLabel = Label(ceAlertWindow, text="Seguro que desea eliminar a {}?".format(clienteid))

	ceBotonSi = Button(ceAlertWindow, text="Si", command=ceDelete)
	ceBotonNo = Button(ceAlertWindow, text="No", command=ceDestroy)

	ceEliminarLabel.pack(side=TOP)

	ceBotonSi.pack(side=BOTTOM)
	ceBotonNo.pack(side=BOTTOM)
	

def aAgregar():
	#Agregar a la base de datos el campo segun los datos en aTextNombre, aMenuTipo y mostrar una ventana para pedir restricciones
	pass


def tShowWindow():
	tsShowWindow = Toplevel()
	tsShowWindow.title("Ver Tweets")
	tsShowWindow.geometry("600x400")

	tsFilterFrame = Frame(tsShowWindow)

	def getTweets():
		MONGO_HOST = MongoClient("mongodb+srv://aegistk14104:aegistk14104@cc3040alv14104-dawge.mongodb.net/test?retryWrites=true")
		db = MONGO_HOST.twitterdb
		tweets = db.twitter_search
		nameEntry = tsFilterNameEntry.get()
		print (nameEntry)
		tstextEntry = tsFilterTextEntry.get()
		print (tstextEntry)
		if ((nameEntry == "") and (tstextEntry == "")):
			posts  = tweets.find()
		elif (nameEntry != "") and (tstextEntry == ""):
			posts = tweets.find({"user": {"name": "{}".format(nameEntry)}})
		elif (nameEntry == "") and (tstextEntry != ""):
			posts = tweets.find({"text":"/{}/".format(tstextEntry)})
		else:
			posts = tweets.find({"user": {"name": "{}".format(nameEntry)}, "text":"/{}/".format(tstextEntry)})


		tsListboxRows.delete(0, END)
		for post in posts:
			parsedString = post["text"] + ": " + post["user"]["name"]
			tsListboxRows.insert(END, parsedString)



	tsGetButton = Button(tsFilterFrame, text ="Armar lista", command=getTweets)
	tsFilterNameLabel = Label(tsFilterFrame, text="Por nombre:")
	tsFilterNameEntry = Entry(tsFilterFrame)
	tsFilterTextLabel = Label(tsFilterFrame, text="Por Texto:")
	tsFilterTextEntry = Entry(tsFilterFrame)

	tsScrollbar = Scrollbar(tsShowWindow, orient=VERTICAL)
	tsListboxRows = Listbox(tsShowWindow, yscrollcommand=tsScrollbar.set)
	tsScrollbar.configure(command=tsListboxRows.yview)

	tsGetButton.pack(side=RIGHT)
	tsFilterNameLabel.pack(side=LEFT)
	tsFilterNameEntry.pack(side=LEFT)
	tsFilterTextLabel.pack(side=LEFT)
	tsFilterTextEntry.pack(side=LEFT)
	tsScrollbar.pack(side=RIGHT, fill=Y)
	tsListboxRows.pack(side=BOTTOM, fill=BOTH, expand=1)

	tsFilterFrame.pack(side=TOP)


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
TwitterFrame = Frame(root)


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

tBotonModuloTwitter = Button(TwitterFrame, text="Ver tweets", command = tShowWindow)

### VARIABLES

cVariable = StringVar(ClientesFrame)
cVariable.set(clientesIdList[0]) # default value

aVariableTipo = StringVar(CamposFrame)
aVariableTipo.set("int") # default value

### OPTIONMENUS

cMenuEliminaroActualizar = OptionMenu(ClientesFrame, cVariable, *clientesIdList)
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

tBotonModuloTwitter.pack(side=LEFT)


##FRAMES

Modulo1Frame.pack(fill=BOTH, expand=1)
FiltrosBFrame.pack(side=TOP,fill=X)
ClientesFrame.pack(side=TOP, fill=X)
CamposFrame.pack(fill=X)
DisplayFrame.pack(side=BOTTOM,fill=BOTH, expand=1)
TwitterFrame.pack(side=BOTTOM)

###MAINLOOP
root.mainloop()
