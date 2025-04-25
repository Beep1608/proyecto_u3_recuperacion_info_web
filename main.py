import PyPDF2
import os
import spacy
class Nlp:
    filename = None
    lector = None
    output_dir = None
    def __init__(self):
        self.filename = input("Ingrese el nombre del archivo PDF: ")


    def run(self, extraccion_info):
        print("file name: ", self.filename)
        self.output_dir = self.make__dirs(self)
        self.lector = self.get_lector_pdf(self.filename)
        self.save_pages(self.lector, 15, self.output_dir)
  
        extraccion_info.mostrar_entidades(self.read_pages(self.lector, 15))

    def make__dirs(self, filename):
        base_name = self.filename.replace(".pdf", "")
        output_dir = os.path.join(base_name, "pages")
        os.makedirs(output_dir, exist_ok=True)
        return output_dir

    def get_lector_pdf(self, filename):
        if not os.path.exists(filename):
            print(f"El archivo '{filename}' no existe.")
            return None
        pdf = open(filename, "rb")
        lector = PyPDF2.PdfReader(pdf)

        return lector
    



    # Verificar que el numbero de paginas no sea mayor al total de paginas del pdf
    def save_pages (self,lector, number_pages, output_dir):
    
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
    
    def read_pages (self,lector, number_pages):
        texto = ""
        n = len(lector.pages)
        if(n>number_pages):
            n = number_pages
        pages_created = 0
        for x in range(n):
            pagina = lector.pages[x]
            texto = pagina.extract_text()
            if texto and texto.strip():  
                print(f"Texto de la página {x}:\n{texto}\n")
                pages_created += 1
        print(f"Se han leído {pages_created} páginas del PDF.")
        return texto
    

    class ExtraccionInformacion:
        model = None
        tipos_validos = {'personas': 'PER', 'lugares': 'LOC', 'fechas': 'DATE', 'organizaciones': 'ORG'}
   
        def __init__(self, model):
            self.model = spacy.load(model)

        def mostrar_entidades(self, texto):
            doc = self.model(texto)
            for entidad in doc.ents:
                print(f"Texto: {entidad.text}, Tipo: {entidad.label_}")

        def responder_pregunta(self, texto, pregunta):
            doc_pregunta = self.model(pregunta)
            palabras_clave = [entidad.text.lower() for entidad in doc_pregunta.ents ]
            respuesta = "No puedo responder a esa pregunta."
            #Agregar codigo faltante despues de esta linea 
          
               
                    
       


#Main
Nlp().run(Nlp.ExtraccionInformacion("en_core_web_sm"))