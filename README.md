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

Si quisiéramos obtener todos los contratos asociados a los términos 
```plataforma``` o ```nube``` deberíamos revisar manualmente cada año y cada 
url. Esto es claramente imposible. 

El software en este repositorio busca obtener todos los archivos con formato 
```pdf``` que contengan los términos  ```plataforma``` o ```nube```  
y que estén dentro del sitio web 
```https://corplascondes.cl/contenidos/transparencia/ley_de_transparencia/```

Este programa busca los mencionados términos en todos los enlaces del tipo:
```
https://corplascondes.cl/contenidos/transparencia/ley_de_transparencia/aaa.pdf
https://corplascondes.cl/contenidos/transparencia/ley_de_transparencia/aaa/bbb.pdf
...
https://corplascondes.cl/contenidos/transparencia/ley_de_transparencia/xxx/yyy/zzz.pdf
```

## Paso 1: Instalar dependencias

Para instalar las dependencias y crear un entorno virtual se debe ejecutar
```bash
chmod +x create_venv.sh 
./create_venv.sh
```

O en caso de asi quererlo se pueden instalar las dependencias de manera manual
```bash
pip install scrapy
pip install extruct
pip install jsonlines
pip install wget
pip install PyPDF2
pip install bs4
pip install requests
```

## Paso 2: Obtener todas las url de interés

Esta parte está 100% basada en las instrucciones de 
https://www.scrapingbee.com/blog/crawling-python/ para usar Scrapy. Un respaldo
de la página web está disponible en: 
https://raw.githubusercontent.com/toopazo/lorenzo_buscador/main/scrapingbee_crawling_python.pdf

Para empezar a usar Scrapy debemos ir dentro de la carpeta ``lorenzo_bsucador`` ejecutamos
```bash
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
```bash
scrapy crawl corplascondes --logfile corplascondes.log -o corplascondes.jl -t jsonlines
```
Esto creará el archivo ```spiders/corplascondes.log``` y ```spiders/corplascondes.jl```. El proceso toma unos 10 
minutos

## Paso 3: Refinar las url de interés

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
```bash
python url_search.py --baseurl https://www.corplascondes.cl/contenidos/transparencia/ley_de_transparencia/ --scrapyjl scrapy_crawler/scrapy_crawler/spiders/corplascondes.jl  --patterns 2020 .pdf --outfile output_2020_pdf.txt
```
Esto produce un archivo de texto ```output_2020_pdf.txt``` con los enlaces 
que buscamos. 

## Paso 4: Descargar los ```pdf``` y procesarlos

Finalmente debemos descargar los archivos ```pdf``` y leerlos con la librería 
```PyPDF2``` en búsqueda de ```plataforma``` o ```nube```. Esto es en sí una tarea difícil 
dentro del mundo de la programación. El método más simple y efectivo que probé 
fue convertir todo el texto leído por el OCR a minúsculas y quitar los espacios
en blanco.

El módulo usado para todo esto es ```url_process.py```, se ejecuta usando
```bash
python url_process.py --urlfile output_2020_pdf.txt  --patterns plataforma nube --outfile output_2020_ocr.txt
```
Donde los términos ```plataforma``` o ```nube``` (siempre en minúscula) serán 
buscados dentro de cada ```pdf```. Si alguno de ellos está presente el enlace 
respectivo se guardará en el archivo ```output_2020_ocr.txt```. Este proceso 
toma entre 1 a 15 minutos dependiendo de la cantidad de enlaces a revisar.

## Paso 5: Automatizar todo lo anterior
El archivo ```batch_process.sh``` contiene un ejemplo con el uso de todos los 
comandos anteriores. 

```bash
scrapy startproject scrapy_crawler
cd scrapy_crawler/scrapy_crawler/spiders
scrapy crawl corplascondes --logfile corplascondes.log -o corplascondes.jl -t jsonlines
cd ../../..

python url_search.py --baseurl https://www.corplascondes.cl/contenidos/transparencia/ley_de_transparencia/ --scrapyjl scrapy_crawler/scrapy_crawler/spiders/corplascondes.jl  --patterns 2018 .pdf --outfile output_2018_pdf.txt
python url_search.py --baseurl https://www.corplascondes.cl/contenidos/transparencia/ley_de_transparencia/ --scrapyjl scrapy_crawler/scrapy_crawler/spiders/corplascondes.jl  --patterns 2019 .pdf --outfile output_2019_pdf.txt
python url_search.py --baseurl https://www.corplascondes.cl/contenidos/transparencia/ley_de_transparencia/ --scrapyjl scrapy_crawler/scrapy_crawler/spiders/corplascondes.jl  --patterns 2020 .pdf --outfile output_2020_pdf.txt
python url_search.py --baseurl https://www.corplascondes.cl/contenidos/transparencia/ley_de_transparencia/ --scrapyjl scrapy_crawler/scrapy_crawler/spiders/corplascondes.jl  --patterns 2021 .pdf --outfile output_2021_pdf.txt
python url_search.py --baseurl https://www.corplascondes.cl/contenidos/transparencia/ley_de_transparencia/ --scrapyjl scrapy_crawler/scrapy_crawler/spiders/corplascondes.jl  --patterns 2022 .pdf --outfile output_2022_pdf.txt

python url_process.py --urlfile output_2018_pdf.txt  --patterns plataforma nube --outfile output_2018_ocr.txt
python url_process.py --urlfile output_2019_pdf.txt  --patterns plataforma nube --outfile output_2019_ocr.txt
python url_process.py --urlfile output_2020_pdf.txt  --patterns plataforma nube --outfile output_2020_ocr.txt
python url_process.py --urlfile output_2021_pdf.txt  --patterns plataforma nube --outfile output_2021_ocr.txt
python url_process.py --urlfile output_2022_pdf.txt  --patterns plataforma nube --outfile output_2022_ocr.txt
```
Las primeras líneas de este script asumen que estamos parados en la carpeta 
```lorenzo_buscador``` y que no hay nada aún dentro de ella. Las primeras 
líneas son el trabajo de Scrapy y solo necesitan ser ejecutados una vez.

Las siguientes líneas corresponden a los módulos de Python que refinan la 
búsqueda de url y que leen cada ```pdf``` encontrado.

Fin.