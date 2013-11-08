/*

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

*/

# PRÁCTICA 2 : Aislamiento de una aplicación web usando

La segunda práctica de la asignatura consiste en crear un sistema mínimo en el que tener una
aplicación y enjaular a un usuario. En mi caso, voy a usar un sistema mínimo ubuntu 13.10 amd64
en el que instalaré lo necesario para poder usar una base de datos mongoDB y una aplicación en 
python con el framework web.py.

## Explicación de la aplicación: Aplicación web para gestionar una cafeteria y sus usuarios

Con el fin de aprovechar la práctica para mejorar también los conocimientos en diseño web,
he decidido crear una aplicación en python usando web.py y mako.py (plantillas html) con 
una base de datos mongoDB intentado diseñarla con el modelo vista-controlador. La aplicación
en si solo permite mostrar una página de gestión de una cafeteria en al que podemos facilmente
cambiar el contenido de toda la página simplemente cambiando ciertas variables. También
usamos la base de datos para gestionar usuarios. Para esta práctica, el contenido es genérico.

## Creación de la jaula

Para poder aislar la aplicación web, lo primero es tener una jaula chroot. Para ello, uso
sudo debootstrap --arch=amd64 saucy /home/jaulas/saucy/ http://archive.ubuntu.com/ubuntu.
Previamente creo la carpeta y cambio el propietario a root.

![captura1](https://dl.dropboxusercontent.com/u/17453375/captura1b.png)


## Instalación de paquetes y bibliotecas necesarias para la aplicación 

Una vez que tenemos el sistema mínimo, tenemos que instalar todo lo necesario para que nuestra
aplicación funcione. Entramos en la jaula con la orden chroot.

![captura2](https://dl.dropboxusercontent.com/u/17453375/captura2b.png)

### Python 2.7, Web.py, Mako.py y PyMongo.py

Una vez dentro de la jaula compruebo que viene instalado python3 pero no python2.7. Para instalarlo
uso apt-get como se muestra en la imagen.

![captura3](https://dl.dropboxusercontent.com/u/17453375/captura3b.png)

Con python funcionando, el siguiente paso es descargar el framework 'web.py', descomprimir el paquete
y copiarlo al directorio home de la jaula. Desde la jaula entramos en la carpeta web.py-0.37 y 
ejecutamos el setup.py para instalar 'web.py'.

![captura4](https://dl.dropboxusercontent.com/u/17453375/captura4.png)

Para implementar el modelo vista controlador necesitamos usar plantillas, para ello uso una biblioteca
muy potente para python llamada 'mako'. Igual que 'web.py', descargamos 'mako' de su pagina oficial,
descomprimimos el archivo, lo copiamos en el home de la jaula, entramos a la jaula y ejecutamos el
setup con python.

Por ultimo necesitamos una interfaz para gestionar la base de datos mongoDB. La biblioteca pymongo es
una API para python y mongoDB. El proceso es idéntico a los anteriores. Descargarlo, descomprimirlo y
lanzar setup.py con python.

*NOTA1: Dado que el proceso para añadir bibliotecas a python es siempre igual solo pongo una captura.

*NOTA2: Para evitar ciertos errores, hay que montar el sistema virtual de archivos /proc y el paquete
de español 'apt-get install language-pack-es'

### MongoDB

MongoDB es un sistema de base de datos NoSQL orientado a documentos, desarrollado bajo código abierto.
Para usarla solo tenemos que descargar de la pagina oficial de mongoDB el paquete para linux 64 y 
descomprimirlo. Podemos copiar esta carpeta en el home de la jaula y asi poder lanzarla desde la jaula.
Hay que tener ciertas precauciones con mongoDB. Puede ocurrir que aunque cerremos la base de datos en 
la terminal con control+c , no se cierre, por lo que debemos usar kill -9 para cerrarla. Además, si
esto ocurre, la siguiente vez que lancemos la base de datos nos dará un error. Para evitarlo hay que
borrar el archivo 'mongod.lock' dentro de la carpeta de mongoDB.

## Crear y enjaular un usuario

Con la jaula preparada para nuestra aplicación, el siguiente paso es crear un usuario, que hará las veces
de administrador de la aplicación, y enjaularlo para que solo tenga acceso a la jaula y no a todo el
sistema. Además estará limitado a ciertas carpetas (las de la aplicación).

En primer lugar creamos al usuario, establecemos su home en el interior de la jaula y creamos su contraseña.

  sudo useradd -s /bin/bash -m -d /home/jaulas/server/./home/admin -c "Administrador de la aplicacion" -g users admin
  sudo passwd admin

Con este comando ya podemos acceder a la jaula con 'ssh admin@localhost' pero el usuario 'admin' podrá
moverse por todo el arbol de ficheros del sistema, saliendo de la jaula y pudiendo ver el resto de archivos.
Ya que nos interesa que este usuario no pueda interferir en el resto del sistema, necesitamos asegurarnos
de que no puede salir de la jaula. Podemos limitar este acceso editando el archivo de configuración del
servicio ssh que se encuentra en '/etc/ssh/sshd_config'. Hay que añadir justo al final una serie de lineas
como se muestran en la imagen.

![captura5](https://dl.dropboxusercontent.com/u/17453375/captura5.png)

Las ultimas lineas no comentadas lo que hacen es dar permiso al usuario admin y si se conecta establecer 
su directorio dentro de la jaula 'ChrootDirectory /home/jaulas/server'. Despues de guardar los cambios
reiniciamos el servicio con 'sudo service ssh restart' y volvemos a conectarnos con ssh.

![captura6](https://dl.dropboxusercontent.com/u/17453375/captura6.png)

Como podemos apreciar en la imagen, no podemos salir de la jaula, además este usuario no tiene permisos
en la carpeta del sistema de la jaula, por ello solo puede crear o borrar archivos en el home.

![captura7](https://dl.dropboxusercontent.com/u/17453375/captura7.png)

## Lanzar y acceder a traves del navegador a la aplicacion

Con la jaula y el usuario configurados solo nos queda poner los archivos de la aplicación en el 
directorio que tenga permisos para el usuario admin, y lanzarlos. Podemos hacerlo copiandolos
en la jaula con el sistema anfitrión, o desde dentro de la jaula, por ejemplo, instalando git
y descargando el proyecto en el que se encuentran.

Mi aplicación tiene dos partes, por un lado los archivos python que hacen de servidor web y por
otro lado la base de datos MongoDB

En primer lugar entramos con el servicio ssh con el usuario admin, nos movemos la carpeta 
mongoDB y dentro ejecutamos:
  
  ./bin/mongod --dbpath . --nojournal

Este comando lanza la base de datos y se queda esperando peticiones. Como se ve en la parte 
izquierda de la imagen que hay mas abajo,  cualquier peticion a la base de datos se mostrará
en la terminal.

Ahora necesitamos lanzar la aplicación web, para ello solo hay que abrir otra conexion nueva
con ssh y movernos a la carpeta en la que están los archivos python para lanzar main.py. 
web.py lanza un servidor web en el que gestionara las peticiones del navegador en 
http://localhost:8080/cafe (si no ponemos /cafe nos informará de que la página no existe)

![captura8](https://dl.dropboxusercontent.com/u/17453375/captura8.png)

Ya tenemos la aplicacion funcionando. Se trata simplemente de una serie de archivos python
que usando templates sirven páginas web usando web.py. Podemos navegar por las páginas,
loguearnos, modificar nuestros datos o borrar al usuario. Dado que tampoco es objetivo de esta
práctica, no comento el código para no alargar innecesariamente el documento.

En las siguientes capturas podemos ver algunas imagenes que muestran la aplicacion.

![captura9](https://dl.dropboxusercontent.com/u/17453375/captura9.png)

![captura10](https://dl.dropboxusercontent.com/u/17453375/captura10.png)

![captura11](https://dl.dropboxusercontent.com/u/17453375/captura11.png)

![captura12](https://dl.dropboxusercontent.com/u/17453375/captura12.png)

Por ultimo muestro como queda las terminales despues de moverse por la aplicación

![captura13](https://dl.dropboxusercontent.com/u/17453375/captura13.png)

*Nota: En las imagenes no se aprecia, pero hay en un enlace al final que nos indica de donde
he obtenido la plantilla y las imagenes que en ella aparecen

## Direccion de la aplicacion en github

* Practica: [https://github.com/torresj/practica-2](https://github.com/torresj/practica-2)
* Documentación: [https://github.com/torresj/practica-2/blob/master/documentacion/documentacion.md](https://github.com/torresj/practica-2/blob/master/documentacion/documentacion.md)

##Biliografía
  
* [http://www.techrepublic.com/blog/linux-and-open-source/chroot-users-with-openssh-an-easier-way-to-confine-users-to-their-home-directories/](http://www.techrepublic.com/blog/linux-and-open-source/chroot-users-with-openssh-an-easier-way-to-confine-users-to-their-home-directories/)
* [http://webpy.org/](http://webpy.org/)
* [http://www.makotemplates.org/](http://www.makotemplates.org/)
* [http://api.mongodb.org/python/current/](http://api.mongodb.org/python/current/)
* [http://www.mongodb.org/](http://www.mongodb.org/)
