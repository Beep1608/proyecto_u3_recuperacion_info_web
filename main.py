import PyPDF2


filename = input("Ingrese el nombre del archivo PDF: ")


pdf = open(filename, "rb")
lector = PyPDF2.PdfReader(pdf)
n = len(lector.pages)
if(n>10):
    n = 10

for x in range(n):
  pagina = lector.pages[x]
  texto = pagina.extract_text()


  output_filename = filename.replace(".pdf", "") + "_page" + str(x) + ".txt"

  with open(output_filename, "w", encoding="utf-8") as archivo:
      archivo.write(texto)

pdf.close()
print("Se han creado los archivos de texto para las primeras 5 páginas del PDF.")