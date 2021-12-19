from suds.client import Client

def get_opers(barcode):
    url = 'https://tracking.russianpost.ru/rtm34?wsdl'
    client = Client(url,headers={'Content-Type': 'application/soap+xml; charset=utf-8'})

    my_login = 'KKYVGXlbvkPfqV' #login #fix in prod
    my_password = 'tKiMsWKXGGLg' #password #fix in prod
    message = \
    """<?xml version="1.0" encoding="UTF-8"?>
                    <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:oper="http://russianpost.org/operationhistory" xmlns:data="http://russianpost.org/operationhistory/data" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
                    <soap:Header/>
                    <soap:Body>
                       <oper:getOperationHistory>
                          <data:OperationHistoryRequest>
                             <data:Barcode>""" + barcode+ """</data:Barcode>
                             <data:MessageType>0</data:MessageType>
                             <data:Language>RUS</data:Language>
                          </data:OperationHistoryRequest>
                          <data:AuthorizationHeader soapenv:mustUnderstand="1">
                             <data:login>"""+ my_login +"""</data:login>
                             <data:password>""" + my_password + """</data:password>
                          </data:AuthorizationHeader>
                       </oper:getOperationHistory>
                    </soap:Body>
                 </soap:Envelope>"""

    try:
        result = client.service.getOperationHistory(__inject={'msg':message})

        opers_maps = list()

        for rec in result.historyRecord:
            oper_map = {
                'date': rec.OperationParameters.OperDate,
                'index': rec.AddressParameters.OperationAddress.Index,
                'post_office': rec.AddressParameters.OperationAddress.Description,
                'oper_name': rec.OperationParameters.OperType.Name + " - " + rec.OperationParameters.OperAttr.Name
            }
            opers_maps.append(oper_map)

        return opers_maps
    except:
        return None;
