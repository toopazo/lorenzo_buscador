import argparse
import wget
import PyPDF2
import os
import urllib


class UrlProcess:
    def __init__(self):
        pass

    @staticmethod
    def process(urlfile, patterns, outfile):
        fd = open(urlfile, 'r')
        urls = fd.readlines()
        fd.close()

        results = []
        for url in urls:
            if '.pdf' in url:
                url = url.strip()
                result = UrlProcess.download_check_delete(url, patterns)
                results.append(result)

        fd = open(outfile, 'w')
        fd.writelines(results)
        fd.close()

    @staticmethod
    def download_check_delete(url, patterns):
        print('---------')
        print(f'[download_check_delete] url {url}')
        try:
            filename = wget.download(url)
        except urllib.error.HTTPError:
            print(f'[download_check_delete] urllib.error.HTTPError')
            return ''

        result = UrlProcess.search_in_pdf(filename, patterns)
        os.remove(filename)

        if result:
            # return f"{url},{result}\n"
            return f"{url}\n"
        else:
            return ''

    @staticmethod
    def search_in_pdf(filename, patterns):
        # https://medium.com/analytics-vidhya/how-to-extract-texts-from-pdf-
        # file-and-search-keywords-from-extracted-text-in-python-c5f3d4841f20
        pdffd = open(filename, 'rb')
        try:
            pdfreader = PyPDF2.PdfFileReader(pdffd)
        except PyPDF2.errors.PdfReadError:
            return False

        npages = len(pdfreader.pages)
        print(f'[search_in_pdf] npages {npages}')

        for np in range(0, npages):
            pageobj = pdfreader.pages[np]
            try:
                text = (pageobj.extractText())
            except TypeError:
                return False
            except KeyError:
                return False

            # Modify text to make it easy to read
            # text = text.split(",")
            text = text.strip()
            text = text.replace(' ', '')
            text = text.lower()

            # print(f'[search_in_pdf] text {text}')
            # if 'cecilia' in text:
            #     print('bingooooooooo')

            # Check if any of the patterns are present in the text
            all_good = False
            for pattern in patterns:
                if pattern in text:
                    all_good = True
            if all_good:
                return True

        # If nothing is detected report a negative result
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Arguments for search_inside_url')
    parser.add_argument('--urlfile', action='store', required=True,
                        help='Archivo con url a procesar')
    parser.add_argument('--patterns', action='store', nargs='+', required=True,
                        help='Lista de patrones para filtrar')
    parser.add_argument('--outfile', action='store', required=True,
                        help='Archivo con las url con resultado positivo')

    args = parser.parse_args()
    print(f'urlfile {args.urlfile}')
    print(f'patterns {args.patterns}')
    print(f'outfile {args.outfile}')
    UrlProcess.process(args.urlfile, args.patterns, args.outfile)

    # python url_process.py --urlfile output_2021_pdf.txt  \
    # --patterns plataforma nube --outfile output_2021_ocr.txt                                                                                                   "tethys" 20:18 23-May-22
