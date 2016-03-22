from datetime import datetime
import dateutil.parser
import pytz
from OpenSSL import crypto, SSL
import os.path
import xml.etree.ElementTree
from myslicelib.util.url import validateUrl
#from myslicelib.util.certificate import Keypair, Certificate

class Endpoint(object):
    """
    An endpoint specifies a remote API endpoint.
    type is the type of endpoint, e.g. AM, Reg
    protocol specifies the protocol, default is SFA
    url is the remote url

    name: name of the testbed/facility (not needed)

    """

    def __init__(self, type="AM", protocol="SFA", url=None, name=None):
        self.name = name
        self.type = type
        self.protocol = protocol
        if not url or not validateUrl(url):
            raise ValueError("URL not valid")
        else:
            self.url = url
    
    def __str__(self):
        return self.url


class Credential(object):

    def __init__(self, userid=None, password=None, email=None, hrn=None, private_key=None, certificate=None, sfa_credentials=None):
        if not private_key or not email or not hrn:
            raise ValueError("private key, email and hrn must be specified")
            exit(1)

        self.email = email
        self.hrn = hrn
        self.private_key = private_key

        if not certificate:
            self.certificate = self.create_self_signed_cert()
        else:
            self.certificate = certificate

        # this dict can contain: user_credential, hrn of a slice, hrn of an authority...
        # sfa_credentials can be delegated from another user
        if sfa_credentials:
            for k,v in sfa_credentials.items():
                if os.path.isfile(v):
                    with open(v, "r") as myfile:
                        v = myfile.read()
                # Check if the credential is expired
                el = xml.etree.ElementTree.fromstring(v)
                expiration = el.find('credential').find('expires').text
                exp = dateutil.parser.parse(expiration)
                utc = pytz.utc
                if exp > utc.localize(datetime.now()):
                    setattr(self, k.replace('.','_'), v)
                    print(k+': is valid')
                else:
                    print(k+': is expired')

    def create_self_signed_cert(self):

        # create a key pair
        k = crypto.PKey()
        k.generate_key(crypto.TYPE_RSA, 1024)

        # create a self-signed cert
        cert = crypto.X509()
        cert.get_subject().C = "FR"
        cert.get_subject().ST = "Paris"
        cert.get_subject().L = "Paris"
        cert.get_subject().O = "Onelab"
        # cert.get_subject().OU = ""
        cert.get_subject().CN = self.hrn.encode('latin1')
        cert.set_serial_number(1000)
        cert.gmtime_adj_notBefore(0)
        cert.gmtime_adj_notAfter(10*365*24*60*60)
        cert.set_issuer(cert.get_subject())
        cert.set_pubkey(k)
        cert.sign(k, 'sha1')

        #crypto.X509Extension (name, critical, value)
        return crypto.dump_certificate(crypto.FILETYPE_PEM, cert)

        # open(self.private_key, "wt").write(
        #     crypto.dump_privatekey(crypto.FILETYPE_PEM, k))

    def sign_certificate(self):
        keypair = Keypair(filename = self.private_key.encode('latin1'))
        self_signed = Certificate(subject = self.hrn)
        self_signed.set_pubkey(keypair)
        self_signed.set_issuer(keypair, subject = self.hrn.encode('latin1'))
        self_signed.set_data('email:' + self.email, 'subjectAltName')
        self_signed.sign()
        return self_signed.save_to_string()
