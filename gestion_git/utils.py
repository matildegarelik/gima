import fitz
from .models import Patente, Seccion
import datetime

def leer_patentes(file,seccion=83):
    #doc = fitz.open(file)
    doc= fitz.open(stream=file.read(), filetype="pdf")
    cont=0
    for page in doc:
        dominio=False

        page = doc[cont]
        words = page.get_text("words")
        cont_words=0
        cont_reg=0
        while(cont_words< len(words)):
            if not dominio and words[cont_words][4]=="Dominio.":
                dominio = words[cont_words+1][4]
            if words[cont_words][4]=="TITULAR.":
                #nuevo registro
                titular= ''
                cont_words=cont_words+1
                while words[cont_words][4]!="DOCUMENTO.":
                    if titular:
                        titular=titular+' '
                    titular= titular + words[cont_words][4]
                    cont_words=cont_words+1
                
                cuit= ''
                while words[cont_words][4]!="CUIT.":
                    cont_words=cont_words+1
                cont_words=cont_words+1
                cuit=words[cont_words][4]
                
                direccion =''
                cont_words=cont_words+2
                while words[cont_words][4]!="Localidad.":
                    if direccion:
                        direccion=direccion+' '
                    direccion= direccion + words[cont_words][4]
                    cont_words=cont_words+1
                
                localidad =''
                cont_words=cont_words+1
                while words[cont_words][4]!="Provincia.":
                    if localidad:
                        localidad=localidad+' '
                    localidad= localidad + words[cont_words][4]
                    cont_words=cont_words+1
                
                provincia =''
                cont_words=cont_words+1
                while words[cont_words][4]!="CPA.":
                    if provincia:
                        provincia=provincia+' '
                    provincia= provincia + words[cont_words][4]
                    cont_words=cont_words+1
                
                cont_words=cont_words+1
                cpa = words[cont_words][4]

                vigente=False
                if words[cont_words+1][4]=='Dominio.*':
                    vigente=True

                while words[cont_words-1][4]!="Marca.":
                    cont_words=cont_words+1
                marca = ''
                while words[cont_words][4]!="Modelo.":
                    if marca !='':
                        marca=marca+' '
                    marca= marca + words[cont_words][4]
                    cont_words=cont_words+1
                    
                cont_words=cont_words+1
                modelo= ''
                while words[cont_words][4]!="R.S.Tit./Rad" and words[cont_words][4]!="R.S.Tit.":
                    if modelo!='':
                        modelo=modelo+' '
                    modelo= modelo + words[cont_words][4]
                    cont_words=cont_words+1

                cont_words=cont_words+1
                rad=''
                while words[cont_words][4]!="Pje.":
                    if rad!='':
                        rad=rad+' '
                    rad= rad + words[cont_words][4]
                    cont_words=cont_words+1

                cont_words=cont_words+2
                pje_tit=''
                while words[cont_words][4]!="Fecha":
                    if pje_tit!='':
                        pje_tit=pje_tit+' '
                    pje_tit= pje_tit + words[cont_words][4]
                    cont_words=cont_words+1
                
                cont_words=cont_words+2
                fecha=words[cont_words][4]
                if fecha!="SIN" and fecha !="SIN ":
                    fecha = fecha.split('/')[2]+'-'+fecha.split('/')[1]+'-'+fecha.split('/')[0]
                else:
                    fecha=None
                
                if len(Patente.objects.filter(dominio=dominio, fecha=fecha,cuit=cuit,pje_tit=float(pje_tit[:-1]), rad=rad,seccion_id=seccion)) >0:
                    continue
                
                patente = Patente(
                    seccion=Seccion.objects.get(seccion=seccion),
                    dominio = dominio,
                    vigente=vigente,
                    titular=titular,
                    cuit=cuit,
                    direccion=direccion,
                    localidad=localidad,
                    provincia=provincia,
                    cpa=cpa,
                    marca=marca,
                    modelo=modelo,
                    rad=rad,
                    pje_tit=float(pje_tit[:-1]),
                    fecha=fecha

                )
                patente.save()
                ''''
                print(cuit)
                print(titular)
                print(direccion)
                print(localidad)
                print(provincia)
                print(cpa)
                print(marca)
                print(modelo)
                print(rad)
                print(float(pje_tit[:-1]))
                print(fecha)
                print(vigente)
                '''
                cont_reg=cont_reg+1
            cont_words=cont_words+1
        #print(dominio)
        #print(cont_reg)
        cont=cont+1
        #if cont==2:
        #    break