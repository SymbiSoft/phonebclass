__help__ = """
	Il file class_pb contiene la classe phonebook.
	Nella classe va richiamata la funzione get(multi=0) dove il multi sta per multiselezione
	1 per si e 0 per no.
	La funzione restituisce un array composto da 2 variabili di cui la prima può essere a sua volta un array e
	la seconda è un numero (0 o 1). Se 1 non è stata scelta la multiselezione e quindi la prima variabile contiene 1
	nome e 1 numero, se diversa da 1, la prima variabile sarà un array che conterrà più nomi e più numeri.

	Es.:
	import class_pb
	mphone = class_pb.phonebook()
	dati=mphone.get(multi=1)
	"""

import class_pb,appuifw,e32

def exit_key_handler():
    app_lock.signal()

def pb(mlt=0):
	mphone = class_pb.phonebook()
	dati=mphone.get(multi=mlt)
	testo.set(unicode(dati))

app_lock = e32.Ao_lock()

testo=appuifw.Text()
testo.add(u'prova classe Rubrica')
appuifw.app.body=testo
appuifw.app.title = u'Prova Rubrica'
appuifw.app.menu=[(u"Rubrica", pb),(u"Rubrica multi", lambda:pb(1)),(u"Esci", exit_key_handler)]
appuifw.app.exit_key_handler = exit_key_handler
app_lock.wait()