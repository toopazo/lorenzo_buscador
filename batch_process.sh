
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
