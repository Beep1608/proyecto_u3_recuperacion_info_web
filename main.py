import PyPDF2
import os
class Nlp:
    filename = None
    lector = None
    output_dir = None
    def __init__(self):
        self.filename = input("Ingrese el nombre del archivo PDF: ")


    def run(self):
        self.output_dir = self.make__dirs(self.filename)
        self.lector = self.get_lector_pdf(self.filename)
        self.save_pages(self.lector, 5, self.output_dir)
        self.close_pdf(self.lector)

    def make__dirs(name_file):
        base_name = name_file.replace(".pdf", "")
        output_dir = os.path.join(base_name, "pages")
        os.makedirs(output_dir, exist_ok=True)
        return output_dir

    def get_lector_pdf(filename):
        if not os.path.exists(filename):
            print(f"El archivo '{filename}' no existe.")
            return None
        pdf = open(filename, "rb")
        lector = PyPDF2.PdfReader(pdf)

        return lector
    def close_pdf(pdf):
        pdf.close()


    # Verificar que el numbero de paginas no sea mayor al total de paginas del pdf
    def save_pages (lector, number_pages, output_dir):
    
        n = len(lector.pages)
        if(n>number_pages):
            n = number_pages
        pages_created = 0
        for x in range(n):
            pagina = lector.pages[x]
            texto = pagina.extract_text()
            if texto and texto.strip():  
                output_filename = os.path.join(output_dir, f"page{x}.txt")
                with open(output_filename, "w", encoding="utf-8") as archivo:
                    archivo.write(texto)
                    pages_created += 1
        print(f"Se han creado {pages_created} archivos de texto en '{output_dir}'.")

#Main
Nlp().run()