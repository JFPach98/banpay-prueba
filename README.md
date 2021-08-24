# banpay-prueba

Este repositorio contiene varios archivos necesarios para correr la aplicación de Django, solicitado en el ejercicio 9 de este google colab: https://colab.research.google.com/drive/164XHxQhUyahZbtVU9e8z7m44SxtW5GdR?usp=sharing.

Se incluye el ambiente virtual, el cual es activado con el comando (ejecutado en un directorio superior al del repositorio):
```
.\banpay\Scripts\activate
```

Para instalar las librerías, se generó un archivo requirements.txt. Para instalarlas, se ejecuta el siguiente comando:
```
pip install -r requirements.txt
```

El repositorio también contiene una copia del google colab, en forma de jupyter notebook. Tanto el google colab como el jupyter notebook requieren un archivo 'token.json' que contiene las credenciales para poder acceder a la API de google sheets; el archivo es generado directamente del panel de control de google developer y se debe de insertar en el mismo directorio en el que se encuentra el jupyter notebook (en google colab, basta con subir el archivo al directorio en el que se está trabajando).

Para correr la aplicación de Django, se tiene que ingresar al directorio del repositorio y ejecutar el siguiente comando (después de runserver se introduce el número de puerto de su preferencia):
```
python manage.py runserver
```

En home, aparecerá el primer dataframe, que contiene la información general, ordenada alfabéticamente. Para acceder al dataframe del penúltimo ejercicio, se tiene que ingresar a la siguiente dirección:

```
http://127.0.0.1:[número de puerto]/asia/
```

Debido a las requests que se hacen a la api de Rest Countries, esta página tarda un cierto tiempo en renderizar.

Cualquier duda sobre algún ejercicio del google colab o sobre la aplicación, favor de contactar el siguiente correo:

pacocheco7@gmail.com
