# lorenzo_buscador
Programa en python diseñado para buscar palabras clave en documentos pdf 
dentro de una pagina web. 

## ¿Que problema estamos resolviendo?
Para responder a esta pregunta usaremos el siguiente ejemplo.

El sitio web ```https://corplascondes.cl``` contiene -entre otras cosas- todos 
los contratos efectuados con terceras partes por conceptos de su operación 
como corporación municipal. 

Un ejemplo de contrato se puede ver en el enlace:
```https://corplascondes.cl/contenidos/transparencia/ley_de_transparencia/2020/08agosto/compras-adquisiciones/T-152-B-2020.pdf```

Si quisieramos obtener todos los contratos asociados a una determinada persona
llamada```Juan Perez``` deberiamos revisar manualmente cada año y cada link. 
Esto es claramente imposible. 

El software en este repositorio busca obtener todos 
los archivos con formato ```pdf``` que contengan el nombre de ```Juan Perez``` 
y que esten dentro del sitio web 
```https://corplascondes.cl/contenidos/transparencia/ley_de_transparencia/```

## Paso 1: Obtener todas las url de interes
Esta parte esta 100% basada en la instrucciones de 
https://www.scrapingbee.com/blog/crawling-python/

Por ello hay que partir instalando ```scrapy```
```commandline
pip install scrapy
```

Luego, dentro de la carpeta ``lorenzo_bsucador`` ejecutamos
```commandline
scrapy startproject scrapy_crawler
```
Al ejecutar este comando la respuesta deberia ser similar a la siguiente
```
New Scrapy project 'scrapy_crawler', using template directory '/home/tzo4/Dropbox/tomas/trabajosVarios/lorenzo_buscador/venv/lib/python3.9/site-packages/scrapy/templates/project', created in:
    /home/tzo4/Dropbox/tomas/trabajosVarios/lorenzo_buscador/scrapy_crawler

You can start your first spider with:
    cd scrapy_crawler
    scrapy genspider example example.com
```
Ahora nos dirijimos a la carpeta spider 
```
cd scrapy_crawler/scrapy_crawler/spiders
```
El siguiente paso es crear el archivo de configuración ``corplascondes.py``. 
Este archivo debe estar ubicado en 
```lorenzo_buscador/scrapy_crawler/scrapy_crawler/spiders/corplascondes.py```
Dentro de él pondremos los datos de las url que queremos buscar.
```
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class CorpLasCondesCrawler(CrawlSpider):
    name = 'corplascondes'
    allowed_domains = ['www.corplascondes.cl']
    start_urls = ['https://corplascondes.cl/contenidos/transparencia/ley_de_transparencia']
    rules = (Rule(LinkExtractor()),)
```
Finalmente empezamos la busqueda con el comando
```commandline
scrapy crawl corplascondes --logfile corplascondes.log
```
Esto creará el archivo ```spiders/corplascondes.log```. El proceso toma unos 10 
minutos

## Paso 2: Procesar las url de interes
Scrapy permite añadir un metodo para procesar cada url obtenida. Esto es mucho 
más limpio y elegante desde un punto de vista de programación. Sin embargo por
temás de tiempo acá aremos algo mas simple: crear un modulo de python que lea 
cada url desde el archivo ```spiders/corplascondes.log``` y haga el 
procesamiento de manera separada. 

El problema detectado es que Scrapy no reporta las url que apuntan a archivos ```pdf``` como
```
https://www.corplascondes.cl/contenidos/transparencia/ley_de_transparencia/2020/06junio/compras-adquisiciones/plantilla_contrataciones_a_terceros.pdf
https://corplascondes.cl/contenidos/transparencia/ley_de_transparencia/2020/06junio/compras-adquisiciones/T-141-2020.pdf
```

Por ello tuve que usar las libreria ```request``` y ```bs4``` 
```commandline
pip install requests
pip install bs4
```
El modulo ```url_search.py``` se encarga de leer el log producido por el Scrapy
y generar la lista de links que son subconjunto exclusivo y que ademas cumplan 
tener otros patrones en su url
```commandline
python url_search.py \
--baseurl https://www.corplascondes.cl/contenidos/transparencia/ley_de_transparencia/ \
--scrapy_log scrapy_crawler/scrapy_crawler/spiders/corplascondes.log \
--patterns 2019 .pdf --outfile output_2019_pdf.txt
```
Esto produce archivos de texto con los enlaces que buscamos. 

## Paso 3: Descargar los ```pdf``` y procesarlos

Finalmente debemos descargar los archivos ```pdf``` y leerlos con un OCR en busqueda 
de ```Juan Perez```

En desarrollo ..

