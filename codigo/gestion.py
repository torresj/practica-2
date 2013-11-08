# -*- coding: utf-8 -*-

"""

  Esta archivo pertenece a la aplicación "practica 2" bajo licencia GPLv2.
  Copyright (C) 2013 Jaime Torres Benavente.

  Este programa es software libre. Puede redistribuirlo y/o modificarlo bajo los términos 
  de la Licencia Pública General de GNU según es publicada por la Free Software Foundation, 
  bien de la versión 2 de dicha Licencia o bien (según su elección) de cualquier versión 
  posterior.

  Este programa se distribuye con la esperanza de que sea útil, pero SIN NINGUNA GARANTÍA, 
  incluso sin la garantía MERCANTIL implícita o sin garantizar la CONVENIENCIA PARA UN 
  PROPÓSITO PARTICULAR. Véase la Licencia Pública General de GNU para más detalles.

  Debería haber recibido una copia de la Licencia Pública General junto con este programa. 
  Si no ha sido así, escriba a la Free Software Foundation, Inc., en 675 Mass Ave, Cambridge, 
  MA 02139, EEUU.

"""


"""
Created on Sun Nov  3 13:07:55 2013

@author: jaime
"""
import web
from web.contrib.template import render_mako
from web import form

import pymongo

render = render_mako(
        directories=['plantillas'],
        input_encoding='utf-8',
        output_encoding='utf-8',
        )


# funciones para usar como listas de dias meses y años
def dias():
    x=[];
    for n in range(1,32):
        x.append(n)
    return x
    
def meses():
    x=[];
    for n in range(1,13):
        x.append(n)
    return x   

def anios():
    x=[];
    for n in range(1940,2014):
        x.append(n)
    return x

meses31=['1','3','4','7','8','10','12']
meses30=['5','6','9','11']

#Validadores
vpass=form.regexp(r'.{7,20}$',"La contrasenia debe tener mas de 7 caracteres")
vemail=form.regexp(r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}\b',"Introduzca una direccion de correo valida")

#Formulario Para el login
formul = form.Form( 
    form.Textbox("user",form.notnull,description = "Usuario:"),
    form.Password("password",form.notnull,vpass,description = "Contraseña:"),
    form.Button("Login")
)

#Formulario para el registro

formul2 = form.Form( 
    form.Textbox("nombre",form.notnull,description = "Nombre:"),
    form.Textbox("apellidos",form.notnull, description = "Apellidos:"),
    form.Textbox("email",form.notnull,vemail, description = "Email:"),
    form.Dropdown("dia",dias(),pre="D&iacute;a ",description="Fecha de nacimiento"),
    form.Dropdown("mes",meses(),pre="Mes ",description="Fecha de nacimiento"),
    form.Dropdown("anio",anios(),pre="A&ntilde;o ",description="Fecha de nacimiento"),
    form.Textarea("direccion",form.notnull,description = "Direccion:"),
    form.Textbox("user",form.notnull,description = "Usuario:"),
    form.Password("password",vpass,description = "Contraseña:"),
    form.Password("password2",description = "Repita la contraseña:"),
    form.Button("Actualizar"),
    validators = [
        form.Validator("No coinciden las contraseña", lambda i: i.password == i.password2),
        form.Validator("Fecha incorrecta",lambda k: (k.mes in meses31) or ((k.mes in meses30) and int(k.dia)<31) or ((int(k.mes) == 2) and int(k.dia)<29) or ((int(k.mes) == 2) and int(k.dia)<30 and int(k.anio)%4==0))
        ]
)



#clase para gestionar los datos del usuario
class Gestion:
    def GET(self):
        s=web.ctx.session
        try:
            if s.usuario!='':
                log=True
                user=s.usuario
            else:
                log=False
                user=''
        except AttributeError:
            s.usuario=''
            log=False
            user=''
        
        #Variables para rellenar la pagina web
        login=formul()
        registro=formul2()
        titulo="CAFE DEL MAR"
        subtitulo1="Oferta de cafes"
        cafes=[["Cafe1","Descripcion del cafe 1"],["Cafe2","Descripcion del cafe 2"],["Cafe3","Descripcion del cafe 3"],["Cafe4","Descripcion del cafe 4"]]
        cafeEspecial=["Cafe especial de la casa","Descripcion cafe especial de la casa"]
        piepagina="Copyright &copy; 2013 Jaime Torres Benavente"
        subtitulo2="Datos del usuario"
        cuerpo="Hay que iniciar sesion para poder ver los datos"
        subtitulo3=""
        subtitulo4=""
        servicios=[]
        reg=False
        modo="gestion"
        actualizar=False
        error=''
        if log==True:
            conn=pymongo.MongoClient()
            db=conn.mydb
            usuarios=db.usuarios
            us=usuarios.find_one({"user":s.usuario})
            conn.close()
            nombre=us[u'nombre']
            apell=us[u'apellidos']
            dia=us[u'dia']
            mes=us[u'mes']
            anio=us[u'anio']
            email=us[u'email']
            direc=us[u'direccion']
            return render.plantilla(
                titulo=titulo,
                login=login,
                log=log,
                user=user,
                subtitulo1=subtitulo1,
                cafes=cafes,
                cafeEspecial=cafeEspecial,
                subtitulo2=subtitulo2,
                cuerpo=cuerpo,
                registro=registro,
                subtitulo3=subtitulo3,
                subtitulo4=subtitulo4,
                servicios=servicios,
                piepagina=piepagina,
                reg=reg,
                modo=modo,
                error=error,
                nombre=nombre,
                apell=apell,
                dia=dia,
                mes=mes,
                anio=anio,
                email=email,
                direc=direc,
                actualizar=actualizar)
        else:
            return render.plantilla(
                titulo=titulo,
                login=login,
                log=log,
                user=user,
                subtitulo1=subtitulo1,
                cafes=cafes,
                cafeEspecial=cafeEspecial,
                subtitulo2=subtitulo2,
                cuerpo=cuerpo,
                registro=registro,
                subtitulo3=subtitulo3,
                subtitulo4=subtitulo4,
                servicios=servicios,
                piepagina=piepagina,
                reg=reg,
                modo=modo,
                error=error,
                actualizar=actualizar)

    def POST(self): 
        login=formul()
        registro=formul2()
        titulo="CAFE DEL MAR"
        subtitulo1="Oferta de cafes"
        cafes=[["Cafe1","Descripcion del cafe 1"],["Cafe2","Descripcion del cafe 2"],["Cafe3","Descripcion del cafe 3"],["Cafe4","Descripcion del cafe 4"]]
        cafeEspecial=["Cafe especial de la casa","Descripcion cafe especial de la casa"]
        piepagina="Copyright &copy; 2013 Jaime Torres Benavente"
        subtitulo2="Datos del usuario"
        cuerpo="Hay que iniciar sesion para poder ver los datos"
        subtitulo3=""
        subtitulo4=""
        servicios=[]
        reg=False
        modo="gestion"
        error=''
        actualizar=False

        if not login.validates():
            log=False
            user=''
            return render.plantilla(
            titulo=titulo,
            login=login,
            log=log,
            user=user,
            subtitulo1=subtitulo1,
            cafes=cafes,
            cafeEspecial=cafeEspecial,
            subtitulo2=subtitulo2,
            cuerpo=cuerpo,
            registro=registro,
            subtitulo3=subtitulo3,
            subtitulo4=subtitulo4,
            servicios=servicios,
            piepagina=piepagina,
            reg=reg,
            modo=modo,
            error=error,
            actualizar=actualizar)

        else:
            s=web.ctx.session

            #buscamos al usuario en la base de datos
            conn=pymongo.MongoClient()
            db=conn.mydb
            usuarios=db.usuarios
            us=usuarios.find_one({"user":login['user'].value})
            conn.close()
            try:
                if login['password'].value==us[u'pass']:
                    log=True
                    user=login['user'].value
                    s.usuario=user
                else:
                    log=False
                    user=''
                    error='contras&ntilde;a erronea'
            except TypeError:
                log=False;
                user=''
                error='El usuario no existe'
           
            if log==True:
                conn=pymongo.MongoClient()
                db=conn.mydb
                usuarios=db.usuarios
                us=usuarios.find_one({"user":s.usuario})
                conn.close()
                nombre=us[u'nombre']
                apell=us[u'apellidos']
                dia=us[u'dia']
                mes=us[u'mes']
                anio=us[u'anio']
                email=us[u'email']
                direc=us[u'direccion']
                return render.plantilla(
                titulo=titulo,
                login=login,
                log=log,
                user=user,
                subtitulo1=subtitulo1,
                cafes=cafes,
                cafeEspecial=cafeEspecial,
                subtitulo2=subtitulo2,
                cuerpo=cuerpo,
                registro=registro,
                subtitulo3=subtitulo3,
                subtitulo4=subtitulo4,
                servicios=servicios,
                piepagina=piepagina,
                reg=reg,
                modo=modo,
                error=error,
                nombre=nombre,
                apell=apell,
                dia=dia,
                mes=mes,
                anio=anio,
                email=email,
                direc=direc,
                actualizar=actualizar)
            else:
                return render.plantilla(
                titulo=titulo,
                login=login,
                log=log,
                user=user,
                subtitulo1=subtitulo1,
                cafes=cafes,
                cafeEspecial=cafeEspecial,
                subtitulo2=subtitulo2,
                cuerpo=cuerpo,
                registro=registro,
                subtitulo3=subtitulo3,
                subtitulo4=subtitulo4,
                servicios=servicios,
                piepagina=piepagina,
                reg=reg,
                modo=modo,
                error=error,
                actualizar=actualizar)

class Actualizar:
    def GET(self):
        s=web.ctx.session
        try:
            if s.usuario!='':
                log=True
                user=s.usuario
            else:
                log=False
                user=''
        except AttributeError:
            s.usuario=''
            log=False
            user=''
        
        #Variables para rellenar la pagina web
        login=formul()
        registro=formul2()
        titulo="CAFE DEL MAR"
        subtitulo1="Oferta de cafes"
        cafes=[["Cafe1","Descripcion del cafe 1"],["Cafe2","Descripcion del cafe 2"],["Cafe3","Descripcion del cafe 3"],["Cafe4","Descripcion del cafe 4"]]
        cafeEspecial=["Cafe especial de la casa","Descripcion cafe especial de la casa"]
        piepagina="Copyright &copy; 2013 Jaime Torres Benavente"
        subtitulo2="Formulario para modificar los datos del usuario"
        cuerpo=""
        subtitulo3=""
        subtitulo4=""
        servicios=[]
        reg=False
        modo="gestion_ac"
        error=''
        if log==True:
            actualizar=True
            return render.plantilla(
                titulo=titulo,
                login=login,
                log=log,
                user=user,
                subtitulo1=subtitulo1,
                cafes=cafes,
                cafeEspecial=cafeEspecial,
                subtitulo2=subtitulo2,
                cuerpo=cuerpo,
                registro=registro,
                subtitulo3=subtitulo3,
                subtitulo4=subtitulo4,
                servicios=servicios,
                piepagina=piepagina,
                reg=reg,
                modo=modo,
                error=error,
                actualizar=actualizar)
        else:
            actualizar=False
            return render.plantilla(
                titulo=titulo,
                login=login,
                log=log,
                user=user,
                subtitulo1=subtitulo1,
                cafes=cafes,
                cafeEspecial=cafeEspecial,
                subtitulo2=subtitulo2,
                cuerpo="Debes iniciar sesion para poder modificar los datos",
                registro=registro,
                subtitulo3=subtitulo3,
                subtitulo4=subtitulo4,
                servicios=servicios,
                piepagina=piepagina,
                reg=reg,
                modo=modo,
                error=error,
                actualizar=actualizar)

    def POST(self):
        #Variables para rellenar la pagina web
        login=formul()
        registro=formul2()
        titulo="CAFE DEL MAR"
        subtitulo1="Oferta de cafes"
        cafes=[["Cafe1","Descripcion del cafe 1"],["Cafe2","Descripcion del cafe 2"],["Cafe3","Descripcion del cafe 3"],["Cafe4","Descripcion del cafe 4"]]
        cafeEspecial=["Cafe especial de la casa","Descripcion cafe especial de la casa"]
        piepagina="Copyright &copy; 2013 Jaime Torres Benavente"
        subtitulo2="Formulario para modificar los datos del usuario"
        cuerpo="Debes iniciar sesion para poder modificar los datos"
        subtitulo3=""
        subtitulo4=""
        servicios=[]
        reg=False
        modo="gestion"
        error=''

        s=web.ctx.session
        try:
            if s.usuario!='':
                log=True
                user=s.usuario
            else:
                log=False
                user=''
        except AttributeError:
            s.usuario=''
            log=False
            user=''
        #Procesamos el formulario de login    
        if log==False:
            if not login.validates():
                user=''
                return render.plantilla(
                titulo=titulo,
                login=login,
                log=log,
                user=user,
                subtitulo1=subtitulo1,
                cafes=cafes,
                cafeEspecial=cafeEspecial,
                subtitulo2=subtitulo2,
                cuerpo=cuerpo,
                registro=registro,
                subtitulo3=subtitulo3,
                subtitulo4=subtitulo4,
                servicios=servicios,
                piepagina=piepagina,
                reg=reg,
                modo=modo,
                error=error)
            else:
                #buscamos al usuario en la base de datos
                conn=pymongo.MongoClient()
                db=conn.mydb
                usuarios=db.usuarios
                us=usuarios.find_one({"user":login['user'].value})
                conn.close()
                try:
                    if login['password'].value==us[u'pass']:
                        log=True
                        user=login['user'].value
                        s.usuario=user
                    else:
                        log=False
                        user=''
                        error='contras&ntilde;a erronea'
                except TypeError:
                    log=False;
                    user=''
                    error='El usuario no existe'

                if log==True:
                    web.redirect('/cafe/gestion')
                else:
                    return render.plantilla(
                    titulo=titulo,
                    login=login,
                    log=log,
                    user=user,
                    subtitulo1=subtitulo1,
                    cafes=cafes,
                    cafeEspecial=cafeEspecial,
                    subtitulo2=subtitulo2,
                    cuerpo=cuerpo,
                    registro=registro,
                    subtitulo3=subtitulo3,
                    subtitulo4=subtitulo4,
                    servicios=servicios,
                    piepagina=piepagina,
                    reg=reg,
                    modo=modo,
                    error=error)
        #Procesamos el formulario para actualizar
        else:
            if not registro.validates():
                actualizar=True
                return render.plantilla(
                titulo=titulo,
                login=login,
                log=log,
                user=user,
                subtitulo1=subtitulo1,
                cafes=cafes,
                cafeEspecial=cafeEspecial,
                subtitulo2=subtitulo2,
                cuerpo=cuerpo,
                registro=registro,
                subtitulo3=subtitulo3,
                subtitulo4=subtitulo4,
                servicios=servicios,
                piepagina=piepagina,
                reg=reg,
                modo=modo,
                error=error,
                actualizar=actualizar)
            else:
                conn=pymongo.MongoClient()
                db=conn.mydb
                usuarios=db.usuarios            
                usuario={
                "user":registro['user'].value,
                "pass":registro['password'].value,
                "nombre":registro['nombre'].value,
                "apellidos":registro['apellidos'].value,
                "dia":registro['dia'].value,
                "mes":registro['mes'].value,
                "anio":registro['anio'].value,
                "email":registro['email'].value,
                "direccion":str(registro['direccion'].value)}
                usuarios.remove({"user":s.usuario})
                usuarios.insert(usuario)
                s.usuario=registro['user'].value
                conn.close()
                web.redirect('/cafe/gestion')


class Borrar:
    def GET(self):
        s=web.ctx.session
        if s.usuario!='':
            conn=pymongo.MongoClient()
            db=conn.mydb
            usuarios=db.usuarios
            usuarios.remove({"user":s.usuario})
            s.kill()
        web.redirect('/cafe') 
