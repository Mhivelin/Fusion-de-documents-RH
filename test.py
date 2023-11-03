import requests


def call_zeendoc_login(email, cpassword, Url_client):

    password = ""

    # Construire l'URL en utilisant la variable Url_client
    url = f'https://armoires.zeendoc.com/{Url_client}/ws/3_0/Zeendoc.php'
    headers = {
        'Content-Type': 'text/xml; charset=utf-8',  # Spécifiez le type de contenu SOAP
    }

    # Remplacez le contenu de la requête avec le corps SOAP
    data = f"""
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns1="urn:Zeendoc">
       <soapenv:Header/>
       <soapenv:Body>
          <ns1:login>
             <Login>{email}</Login>
             <Password>{password}</Password>
             <CPassword>{cpassword}</CPassword>
          </ns1:login>
       </soapenv:Body>
    </soapenv:Envelope>
    """

    # Envoyez la requête POST
    response = requests.post(url, data=data, headers=headers)

    # Vérifiez la réponse
    if response.status_code == 200:
        return response.content
    else:
        return f'Erreur lors de la requête. Code de statut : {response.status_code}'


# Exemple d'utilisation de la fonction
email = 'marius.hivelin@gmail.com'
cpassword = 'X?BSh:R92EmyDKi'
Url_client = 'deltic_demo'

response_content = call_zeendoc_login(email, cpassword, Url_client)
print('Réponse du serveur :', response_content)
