<?php
class ZeenDoc
{
    public $wsdl; // URL du fichier WSDL
    public $service_location; // URL de l'emplacement du service
    public $service_uri; // URI du service
    public $client; // Client SOAP
    public $result; // Résultat du client

    public function __construct($UrlClient = "deltic_demo")
    {
        $this->wsdl = "https://armoires.zeendoc.com/" . $UrlClient . "/ws/3_0/wsdl.php?WSDL";
        $this->service_location = "https://armoires.zeendoc.com/" . $UrlClient . "/ws/3_0/Zeendoc.php";
        $this->service_uri = "https://armoires.zeendoc.com/" . $UrlClient . "/ws/3_0/";
    }

    public function connect($userLogin, $userCPassword)
    {
        ini_set('soap.wsdl_cache_enabled', "0");

        $options = array(
            'location' => $this->service_location,
            'uri' => $this->service_uri,
            'trace' => true,
            'exceptions' => true,
            'features' => SOAP_SINGLE_ELEMENT_ARRAYS + SOAP_USE_XSI_ARRAY_TYPE
        );

        try {
            $this->client = new SoapClient($this->wsdl, $options);

            // Appel de la méthode 'login' du service SOAP
            $result = $this->client->__soapCall(
                'login',
                array(
                    'Login' => $userLogin,
                    'Password' => '',
                    'CPassword' => $userCPassword
                )
            );

            if (isset($result->Error_Msg)) {
                echo "<div class='alert alert-danger' role='alert'>Erreur : " . $result->Error_Msg . "</div>";
            } else {
                echo "<div class='alert alert-success' role='alert'>Connexion réussie</div>";
                return $result;
            }
        } catch (SoapFault $fault) {
            return $fault;
        }
    }

    public function getNBDocument($collId)
    {
        // fonction qui permet de récupérer le nombre de document d'une collection

        // Appel de la méthode 'getNbDoc' du service SOAP
        $result = $this->client->__soapCall(
            'getNbDoc',
            array(
                'Coll_Id' => $collId,
                'IndexList' => new SoapParam('', 'IndexList'),
                'StrictMode' => new SoapParam('', 'StrictMode'),
                'Fuzzy' => new SoapParam('', 'Fuzzy'),
                'Order_Col' => new SoapParam('', 'Order_Col'),
                'Order' => new SoapParam('', 'Order'),
                'Saved_Query_Id' => new SoapParam(240, 'Saved_Query_Id'),
                'Query_Operator' => new SoapParam('', 'Query_Operator')
            )
        );

        if (isset($result->Error_Msg)) {
            echo "<div class='alert alert-danger' role='alert'>Erreur : " . $result->Error_Msg . "</div>";
        } else {
            return $result;
        }
    }

    public function getDocument($collId)
    {
        // fonction qui permet de récupérer les documents d'une collection
        $result = $this->client->__soapCall(
            "getDocument",
            array(
                'Coll_Id' => $collId,
                'Res_Id' => new SoapParam(585, 'Res_Id'),
                'Upload_Id' => new SoapParam('', 'Upload_Id'),
                'Comments' => new SoapParam('', 'Comments'),
                'Lines_ConfigFileName' => new SoapParam('', 'Lines_ConfigFileName'),
                'Wanted_Columns' => new SoapParam('Filename;Page_Count', 'Wanted_Columns')
            )
        );

        if (isset($result->Error_Msg)) {
            echo "<div class='alert alert-danger' role='alert'>Erreur : " . $result->Error_Msg . "</div>";
        } else {
            echo "<div class='alert alert-success' role='alert'>Nombre de documents : " . $result . "</div>";
            return $result;
        }
    }

    public function getRights()
    {
        // fonction qui permet de récupérer toutes les informations de l'utilisateur connecté
        $result = $this->client->__soapCall(
            'getRights',
            array(
                'Get_ConfigSets' => 1
            )
        );

        $result = json_decode($result, true);

        if (isset($result['Error_Msg'])) {
            echo "<div class='alert alert-danger' role='alert'>Erreur : " . $result['Error_Msg'] . "</div>";
        } else {
            echo "<div class='alert alert-success' role='alert'>Récupération des droits réussie</div>";
            return $result;
        }
    }

    public function getInfoPerso()
    {
        //fonction qui permet de récupérer les informations de l'utilisateur connecté
        $result = $this->getRights();

        $infosUser = $result['User'];

        return $infosUser;
    }

    public function getCollList()
    {
        //fonction qui permet de récupérer la liste des collections de l'utilisateur connecté
        $result = $this->getRights();

        $collList = $result['Collections'];

        foreach ($collList as $key => $value) {
            $collList[$key]['Coll_Id'] = $value['Coll_Id'];
            $collList[$key]['Coll_Name'] = $value['Coll_Name'];
            $collList[$key]['Nb_Doc'] = $this->getNBDocument($value['Coll_Id'])['NBDocument'];
        }

        return $collList;
    }
}


// exemple d'utilisation