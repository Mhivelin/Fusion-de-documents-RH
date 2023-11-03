import requests

# Remplacez les valeurs spécifiques
url = 'https://armoires.zeendoc.com/deltic_demo/ws/3_0/Zeendoc.php'
headers = {
    'Content-Type': 'text/xml; charset=utf-8',  # Spécifiez le type de contenu SOAP
}

# Remplacez le contenu de la requête avec le corps SOAP
data = """
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns1="urn:Zeendoc">
   <soapenv:Header/>
   <soapenv:Body>
      <ns1:login>
         <Login>marius.hivelin@gmail.com</Login>
         <Password></Password>
         <CPassword>X?BSh:R92EmyDKi</CPassword>
      </ns1:login>
   </soapenv:Body>
</soapenv:Envelope>
"""

# Envoyez la requête POST
response = requests.post(url, data=data, headers=headers)

# Vérifiez la réponse
if response.status_code == 200:
    print('Réponse du serveur :', response.content)
else:
    print('Erreur lors de la requête. Code de statut :', response.status_code)
