import base64
import http.client
import urllib
import json
from urllib.parse import urlencode


class api(object):
    def __init__(self, base_url:str, username:str, token:str):
        self.base_url = base_url
        self.username = username
        self.token = token
        self.headers = {
            'Authorization': 'cpanel ' + f"{self.username}:{self.token}"
        }
    
    def __cQuery(self,resource, kwargs,value={}):
        """Query Cpanel API
        https://documentation.cpanel.net/display/DD/Guide+to+UAPI
        Parameters
            resource: Module ( SSL , Email)
            faction: gener_csr 
            
        Returns
            JSON response
        """
        try:

            conn = http.client.HTTPSConnection(self.base_url, 2083)
            conn.request('GET', f'/execute/{resource}/{kwargs}?{urlencode(value)}', headers=self.headers)
            
            response = conn.getresponse()
            data = json.loads(response.read())
            conn.close()
            
            return data
        except:
           print((f"Error fetching {resource}"))
    
    ####
    ####
    #### SSL System Faction Generator CSR and Key
    ####
    ####
    
    def generatorCSR(self, domain:str, country:str, state:str, city:str, co:str,key_id:str,friendly_name):
            """Generate SSL Certificate

                This function generates an SSL certificate.

                    https://documentation.cpanel.net/display/DD/UAPI+Functions+-+SSL%3A%3Agenerate_csr,
                Parameters
                    string domain: example.com
                    country: TR - https://www.iso.org/iso-3166-country-codes.html
                    state: Istanbul
                    city: Istanbul
                    co: CVaRy LLC.
            """

            return self.__cQuery('SSL','generate_csr',{
                'domains': domain,
                'countryName': country,
                'stateOrProvinceName': city,
                'localityName': state,
                'organizationName': co,
                'key_id': key_id,
                'friendly_name': friendly_name
            })
    def generatorKey(self, keytype:str,keysize:int,friendly_name:str):
        """Generator SSL Key
            API Doc: https://documentation.cpanel.net/display/DD/UAPI+Functions+-+SSL%3A%3Agenerate_key
            Parameters
            keytpye: system,rsa-2048,rsa-4096
            int keysize: default(2048),4096(rsa-4096)
            friendly_name: This parameter defaults to the key's type, creation date, and creation time. (TestKey)
        """
        keysize = 0 
        return self.__cQuery('SSL','generate_key',{
            'keytype': keytype,
            'keysize': keysize,
            'friendly_name': friendly_name,
        })
    
    def generatorRequestSSL(self,domain:str,country:str,state:str,city:str,co:str):
        """AutoSSL Request CSR SSL System
        Parameters
        domain: example.com
        country: TR ( USA, AZ, ENG )
        state: Kocaeli
        city: Kocaeli
        co: Turhost Hosting Bilisim Hizmetleri
        """
        key_id = self.generatorKey("rsa-2048",2048,"AutoSSL System-"+domain)
        key_id = json.dumps(key_id)
        key_id = json.loads(key_id)
        autossl = self.generatorCSR(domain,country,state,city,co,key_id["data"]["id"],"AutoSSL System-"+domain)

        return autossl
    def listcsr(self):
        domainlist = self.__cQuery('SSL','list_csrs') # CSR List Talebi
        domainler = {}
        for i in range(len(domainlist["data"])): # Liste Sayısı Tespit
            dm = domainlist["data"][i]["commonName"] # Gelen Domainleri DM değişkenine ata
            domainler[i] = dm # Domainler Listesine DM değişkenini ekle

        return domainler # Fonsiyon döngüsü Json domain listesini ver.

    def domainlist(self,type):
        """
        Parameters
        type: addon_domains,sub_domains,parked_domains
        """
        domainlist = self.__cQuery('DomainInfo','list_domains')
        domainler = {}
        if type == "main_domain":
            return domainlist["data"][type]
        else:

            for i in range(len(domainlist["data"][type])): # Liste Sayısı Tespit
                dm = domainlist["data"][type][i] # Gelen Domainleri DM değişkenine ata
                domainler[i] = dm # Domainler Listesine DM değişkenini ekle

            return domainler
    def BlockIP_add_ip(self,ip):

        return self.__cQuery('BlockIP','add_ip',{
            'ip':ip
        })
    def BlockIP_remove_ip(self,ip):

        return self.__cQuery('BlockIP','remove_ip',{
            'ip':ip
        })
    
    def Quota_get_quota_info(self):

        return self.__cQuery('Quota','get_quota_info',{})

    def ResourceUsage_get_usages(self):

        return self.__cQuery('ResourceUsage','get_usages',{})



