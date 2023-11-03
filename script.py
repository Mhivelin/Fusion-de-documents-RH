# import
# pour la connexion SOAP
import PyPDF2
from zeep import Client

# Connexion à Zeendoc


# Import des bibliothèques
import PyPDF2
import zeep


class ZeenDoc:
    def __init__(self, UrlClient="deltic_demo"):
        self.wsdl = f"https://armoires.zeendoc.com/{UrlClient}/ws/3_0/wsdl.php?WSDL"
        self.service_location = f"https://armoires.zeendoc.com/{UrlClient}/ws/3_0/Zeendoc.php"
        self.service_uri = f"https://armoires.zeendoc.com/{UrlClient}/ws/3_0/"
        self.client = zeep.Client(
            self.wsdl, transport=zeep.Transport(operation_timeout=10))

    def connect(self, userLogin, userCPassword):
        try:
            # Appel de la méthode 'login' du service SOAP
            result = self.client.service.login(userLogin, '', userCPassword)

            if hasattr(result, 'Error_Msg'):
                print(f"Erreur : {result.Error_Msg}")
            else:
                print("Connexion réussie")
                return result
        except zeep.exceptions.Fault as fault:
            return fault


# Test de connexion
if __name__ == "__main__":
    login = "marius.hivelin@gmail.com"
    CPassword = "X?BSh:R92EmyDKi"

    zeendoc = ZeenDoc()
    session = zeendoc.connect(login, CPassword)
    # Vous pouvez utiliser la session pour d'autres opérations Zeendoc si nécessaire.


def fusionDocs(listeDesBulletins, listeDesSyntheses, listeDesNotes, listeDesCourriers):
    # Créez un objet PDF de sortie vide
    pdf_final = PyPDF2.PdfFileWriter()

    # Fusionnez les bulletins de paie, synthèses, notes et courriers dans un ordre spécifique
    for documents in [listeDesBulletins, listeDesSyntheses, listeDesNotes, listeDesCourriers]:
        # Compteur de pages pour vérifier si nous devons ajouter une page blanche
        page_count = 0
        for document in documents:
            pdf = PyPDF2.PdfFileReader(document)
            for page_num in range(pdf.getNumPages()):
                page = pdf.getPage(page_num)
                pdf_final.addPage(page)
                page_count += 1

        # Si le nombre de pages est impair, ajoutez une page blanche
        if page_count % 2 != 0:
            blank_page = PyPDF2.PdfFileReader("blank_page.pdf").getPage(0)
            pdf_final.addPage(blank_page)

    # Créez un fichier PDF de sortie
    with open("pdf_final.pdf", "wb") as output_file:
        pdf_final.write(output_file)

    return "pdf_final.pdf"
