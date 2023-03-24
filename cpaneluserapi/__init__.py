import base64
import http.client
import urllib
import json
from urllib.parse import urlencode

class multi_account:
    @classmethod
    def __init__(mult,token,username,hostname):
          mult.token = token
          mult.hostname = hostname
          mult.username = username

    def uapi(mult,resource, kwargs,value={}):
        """ Resource - Module Name

        kwars - Function Name

        value - "params": value

        Official API : https://documentation.cpanel.net/display/DD/Guide+to+UAPI
        """
        headers = {
            'Authorization': 'cpanel ' + f"{mult.username}:{mult.token}"
        }
        try:

            conn = http.client.HTTPSConnection(mult.hostname, 2083)
            conn.request('GET', f'/execute/{resource}/{kwargs}?{urlencode(value)}', headers=headers)
            
            response = conn.getresponse()
            data = json.loads(response.read())
            conn.close()
            
            return data
        except:
           print((f"Error fetching {resource}"))

class account:     
    @classmethod
    def hostname(cls,value):
        cls.hostname = value
    @classmethod
    def username(cls,value):
        cls.username = value
    @classmethod
    def token(cls,value):
        cls.token = value

    
    def cQuery(cls,resource, kwargs,value={}):
        headers = {
            'Authorization': 'cpanel ' + f"{cls.username}:{cls.token}"
        }
        try:

            conn = http.client.HTTPSConnection(cls.hostname, 2083)
            conn.request('GET', f'/execute/{resource}/{kwargs}?{urlencode(value)}', headers=headers)
            
            response = conn.getresponse()
            data = json.loads(response.read())
            conn.close()
            
            return data
        except:
           print((f"Error fetching {resource}"))

class BlockIP:
    
    def add_ip(ip):
        account.cQuery(account,"BlockIP","add_ip",value={
            "ip": ip
        })


    def remove_ip(ip):
        return account.cQuery(account,'BlockIP','remove_ip',{
            'ip':ip
        })
    

class SSL():

    def generatorCSR(domain:str, country:str, state:str, city:str, co:str,key_id:str,friendly_name):
               
                return account.cQuery(account,'SSL','generate_csr',{
                    'domains': domain,
                    'countryName': country,
                    'stateOrProvinceName': city,
                    'localityName': state,
                    'organizationName': co,
                    'key_id': key_id,
                    'friendly_name': friendly_name
                })
    def generatorKey(keytype:str,keysize:int,friendly_name:str):

            keysize = 0 
            return account.cQuery(account,'SSL','generate_key',{
                'keytype': keytype,
                'keysize': keysize,
                'friendly_name': friendly_name,
            })
        
    def generatorRequestSSL(domain:str,country:str,state:str,city:str,co:str):

            key_id = SSL.generatorKey("rsa-2048",2048,"AutoSSL System-"+domain)
            key_id = json.dumps(key_id)
            key_id = json.loads(key_id)
            autossl = {}
            autossl["key"] = key_id["data"]["text"]
            response = SSL.generatorCSR(domain,country,state,city,co,key_id["data"]["id"],"AutoSSL System-"+domain)
            autossl["csr"] = response["data"]["text"]

            return autossl
    def listcsr():
            domainlist = account.cQuery(account,'SSL','list_csrs') # CSR List Talebi
            domainler = {}
            for i in range(len(domainlist["data"])): # Liste Sayısı Tespit
                dm = domainlist["data"][i]["commonName"] # Gelen Domainleri DM değişkenine ata
                domainler[i] = dm # Domainler Listesine DM değişkenini ekle

            return domainler # Fonsiyon döngüsü Json domain listesini ver.
    
    def findkey(key_id):
        return account.cQuery(account,'SSL','find_csrs_for_key',{
            'id': key_id,
        })
    def delete_cert(id:str,friendly_name:None):
         return account.cQuery(account,"SSL","delete_cert",value={
              "id":id,
              "friendly_name":friendly_name
         })
    def delete_csr(id:str,friendly_name:None):
         return account.cQuery(account,"SSL","delete_csr",value={
              "id":id,
              "friendly_name":friendly_name
         })
    def delete_key(id:str,friendly_name:None):
         return account.cQuery(account,"SSL","delete_key",value={
              "id":id,
              "friendly_name":friendly_name
         })
    def delete_ssl(domain:str):
         return account.cQuery(account,"SSL","delete_ssl",value={
              "id":id,
         })
    def show_csr(domain:str,friendly_name:None):
         return account.cQuery(account,"SSL","show_csr",value={
              "id":id,
              "friendly_name":friendly_name
         })
    