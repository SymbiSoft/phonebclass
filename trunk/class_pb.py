__title__ = u'Rubrica'
__version__ = u'v1.2 S60-IT'

class phonebook:
	def __init__(s):
		import appuifw, contacts
		try:
			import appuifw2
		except:
			s.appuifw2disponibile = 0
		else:
			s.appuifw2disponibile = 1
			s.appuifw2 = appuifw2
		s.appuifw,s.contacts = appuifw, contacts
		s.oldscreen = s.appuifw.app.screen
		s.oldbody = s.appuifw.app.body
		s.oldexitkeyhandler = s.appuifw.app.exit_key_handler
		s.oldmenu = s.appuifw.app.menu
		s.oldtitle = s.appuifw.app.title
		try:
			s.oldorientation = s.appuifw.app.orientation
			s.appuifw.app.orientation = False
		except:
			pass
		try:
			s.oldfocus = s.appuifw.app.body.focus
			s.appuifw.app.body.focus = False
		except:
			pass
		if s.appuifw2disponibile:
			s.oldnavi_text = s.appuifw2.app.navi_text

	def ___check(s,x):
		try:
			x[0].encode('latin').replace(' ','').decode('hex')
		except:
			return 1
		else:
			return 0

	def ___singolo(s):
		s.appuifw.app.title = __title__
		if s.appuifw2disponibile:
			s.appuifw2.app.navi_text = u'%s' % __version__
		s.db_rubr=s.contacts.ContactsDb()
		s.nomi_r=[]
		s.nomi_posizione=[]
		for i in s.db_rubr:
			s.nomi_posizione.append((s.db_rubr[i].title,i))
		s.nomi_posizione.sort()
		s.nomi_posizione=filter(s.___check,s.nomi_posizione)
		s.nomi_r=map(lambda x:x[0],s.nomi_posizione)
		s.i=s.appuifw.selection_list(s.nomi_r,search_field=1)
		if s.i!=None:
			s.num_trovati=[]
			s.i_contatto=s.nomi_posizione[s.i][1]
			for linea in s.db_rubr[s.i_contatto].as_vcard().splitlines():
				if linea.find('TEL;')==0 and linea.find(':')!=-1:
					s.num_trovati.append(linea.split(':')[1].decode('latin'))
			if len(s.num_trovati)==0:
				return None 
			elif len(s.num_trovati)==1:
				s.destinatario=s.num_trovati[0]
			else:
				s.indice=s.appuifw.popup_menu(s.num_trovati,s.nomi_r[s.i])
				if s.indice!=None:
					s.destinatario=s.num_trovati[s.indice]
				else:
					return None
			return s.nomi_r[s.i],s.destinatario
		else:
			return None

	def ___multiplo(s):
		s.appuifw.app.title = __title__ + u' (scelta multipla)'
		if s.appuifw2disponibile:
			s.appuifw2.app.navi_text = u'%s' % __version__
		s.db_rubr=s.contacts.ContactsDb()
		s.nomi_r=[]
		s.nomi_posizione=[]
		for i in s.db_rubr:
			s.nomi_posizione.append((s.db_rubr[i].title,i))
		s.nomi_posizione.sort()
		s.nomi_posizione=filter(s.___check,s.nomi_posizione)
		s.nomi_r=map(lambda x:x[0],s.nomi_posizione)
		s.i=s.appuifw.multi_selection_list(s.nomi_r,search_field=1)
		if len(s.i):
			s.lista_finale=[]
			for i_scelto in s.i:
				s.num_trovati=[]
				s.i_contatto=s.nomi_posizione[i_scelto][1]
				for linea in s.db_rubr[s.i_contatto].as_vcard().splitlines():
					if linea.find('TEL;')==0 and linea.find(':')!=-1:
						s.num_trovati.append(linea.split(':')[1].decode('latin'))
				if len(s.num_trovati)==0:
					return None
				elif len(s.num_trovati)==1:
					s.lista_finale.append((s.nomi_r[i_scelto],s.num_trovati[0]))
				else:
					s.indice=s.appuifw.popup_menu(s.num_trovati,s.nomi_r[i_scelto])
					if s.indice!=None:
						s.lista_finale.append((s.nomi_r[i_scelto],s.num_trovati[s.indice]))
			if s.lista_finale:
				return s.lista_finale
			else:
				return None
		else:
			return None

	def ___giveback(s):
		s.appuifw.app.body = s.oldbody
		s.appuifw.app.screen = s.oldscreen
		s.appuifw.app.exit_key_handler = s.oldexitkeyhandler
		s.appuifw.app.menu = s.oldmenu
		s.appuifw.app.title = s.oldtitle
		try:
			s.appuifw.app.body.focus = s.oldfocus
		except:
			pass
		try:
			s.appuifw.app.orientation = s.oldorientation
		except:
			pass
		if s.appuifw2disponibile:
			s.appuifw2.app.navi_text = s.oldnavi_text

	def get(s, multi=0):
		if multi == 1:
			s.data = s.___multiplo()
		else:
			s.data = s.___singolo()
		s.___giveback()
		return s.data
