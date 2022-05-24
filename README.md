# lorenzo_buscador
Programa (Python) para buscar palabras clave en documentos ```pdf``` dentro de 
un sitio web. 

## ¿Qué problema resuelve este repositorio?
Para responder a esta pregunta usaremos el siguiente ejemplo.

El sitio web ```https://corplascondes.cl``` contiene -entre otras cosas- todos 
los contratos efectuados con terceras partes por conceptos de su operación 
como corporación municipal. 

Un ejemplo de contrato se puede ver en el enlace:
```https://corplascondes.cl/contenidos/transparencia/ley_de_transparencia/2020/08agosto/compras-adquisiciones/T-152-B-2020.pdf```

Si quisiéramos obtener todos los contratos asociados a una determinada persona
llamada```Juan Perez``` deberíamos revisar manualmente cada año y cada link. 
Esto es claramente imposible. 

El software en este repositorio busca obtener todos 
los archivos con formato ```pdf``` que contengan el nombre de ```Juan Perez``` 
y que estén dentro del sitio web 
```https://corplascondes.cl/contenidos/transparencia/ley_de_transparencia/```

Este programa busca a ```Juan Perez``` en todos los enlaces del tipo:
```
https://corplascondes.cl/contenidos/transparencia/ley_de_transparencia/aaa.pdf
https://corplascondes.cl/contenidos/transparencia/ley_de_transparencia/aaa/bbb.pdf
...
https://corplascondes.cl/contenidos/transparencia/ley_de_transparencia/xxx/yyy/zzz.pdf
```

## Paso 0: Instalar dependencias

Idealmente instalarlas en un entorno virtual (virtual environment)
```commandline
pip install scrapy
pip install extruct
pip install jsonlines
pip install wget
pip install PyPDF2
pip install bs4
pip install requests
```

## Paso 1: Obtener todas las url de interés
Esta parte está 100% basada en las instrucciones de 
https://www.scrapingbee.com/blog/crawling-python/ para usar Scrapy. Un respaldo
de la página web está disponible en: 
https://raw.githubusercontent.com/toopazo/lorenzo_buscador/main/scrapingbee_crawling_python.pdf

Para empezar a usar Scrapy debemos ir dentro de la carpeta ``lorenzo_bsucador`` ejecutamos
```commandline
scrapy startproject scrapy_crawler
```
Al ejecutar este comando la respuesta debería ser similar a la siguiente
```
New Scrapy project 'scrapy_crawler', using template directory 'lorenzo_buscador/venv/lib/python3.9/site-packages/scrapy/templates/project', created in:
    lorenzo_buscador/scrapy_crawler

You can start your first spider with:
    cd scrapy_crawler
    scrapy genspider example example.com
```
Ahora nos movemos a la carpeta spider 
```
cd scrapy_crawler/scrapy_crawler/spiders
```
El siguiente paso es crear el archivo de configuración ``corplascondes.py``. 
Este archivo debe estar ubicado en 
```lorenzo_buscador/scrapy_crawler/scrapy_crawler/spiders/corplascondes.py```
Dentro de él pondremos los datos de las url que queremos buscar. En nuestro caso
```
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class CorpLasCondesCrawler(CrawlSpider):
    name = 'corplascondes'
    allowed_domains = ['www.corplascondes.cl']
    start_urls = ['https://corplascondes.cl/contenidos/transparencia/ley_de_transparencia']
    rules = (Rule(LinkExtractor()),)
```
Finalmente empezamos la búsqueda con el comando
```commandline
scrapy crawl corplascondes --logfile corplascondes.log -o corplascondes.jl -t jsonlines
```
Esto creará el archivo ```spiders/corplascondes.log``` y ```spiders/corplascondes.jl```. El proceso toma unos 10 
minutos

## Paso 2: Refinar las url de interés
Existe un problema con los resultados de Scrapy, usando la configuración de más
arriba solo las url terminadas en ```.html``` son reportadas. Esto quiere decir
que los archivos ```pdf``` del tipo 
```
https://www.corplascondes.cl/contenidos/transparencia/ley_de_transparencia/2020/06junio/compras-adquisiciones/plantilla_contrataciones_a_terceros.pdf
https://www.corplascondes.cl/contenidos/transparencia/ley_de_transparencia/2020/06junio/compras-adquisiciones/T-141-2020.pdf
```
no son detectados. Esto es un problema.

Por ello tuve que usar las librerías ```request``` y ```bs4```. En particular el 
módulo ```url_search.py``` se encarga de leer el log producido por Scrapy
y generar la lista de url que son subconjunto exclusivo y que además cumplan 
tener otros patrones como los términos ```2020``` y ```.pdf``` en el ejemplo de
más abajo
```commandline
python url_search.py --baseurl https://www.corplascondes.cl/contenidos/transparencia/ley_de_transparencia/ --scrapyjl scrapy_crawler/scrapy_crawler/spiders/corplascondes.jl  --patterns 2020 .pdf --outfile output_2020_pdf.txt
```
Esto produce un archivo de texto ```output_2020_pdf.txt``` con los enlaces 
que buscamos. 

## Paso 3: Descargar los ```pdf``` y procesarlas

Finalmente debemos descargar los archivos ```pdf``` y leerlos con la librería 
```PyPDF2``` en búsqueda de ```Juan Perez```. Esto es en sí una tarea difícil 
dentro del mundo de la programación. El método más simple y efectivo que probé 
fue convertir todo el texto leído por el OCR a minúsculas y quitar los espacios
en blanco.

El módulo usado para todo esto es ```url_process.py```, se ejecuta usando
```commandline
python url_process.py --urlfile output_2020_pdf.txt  --patterns plataforma nube --outfile output_2020_ocr.txt
```
Donde los términos ```plataforma``` y ```nube``` (siempre en minúscula) serán 
buscados dentro de cada ```pdf```. El resultado se guarda en el archivo 
```output_2020_ocr.txt```

