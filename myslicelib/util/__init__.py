from OpenSSL import crypto, SSL
import os.path
from myslicelib.util.url import validateUrl

class Endpoint(object):
    """
    An endpoint specifies a remote API endpoint.
    type is the type of endpoint, e.g. AM, Reg
    protocol specifies the protocol, default is SFA
    url is the remote url

    name: name of the testbed/facility (not needed)

    """

    def __init__(self, type="AM", protocol="SFA", url=None, name=None, timeout=None, technologies=None):
        self.name = name
        self.type = type
        self.protocol = protocol
        self.technologies = technologies.split(',')
        if timeout:
            self.timeout = timeout
        else:
            # DEFAULT TIMEOUT
            self.timeout = 10 
        if not url or not validateUrl(url):
            raise ValueError("URL not valid")
        else:
            self.url = url
    
    def __str__(self):
        return self.url


class Authentication(object):

    def __init__(self, userid=None, password=None, email=None, hrn=None, private_key=None, certificate=None, credentials=None):
        if not private_key or not email or not hrn:
            raise ValueError("private key, email and hrn must be specified")

        self.email = email
        self.hrn = hrn
        self.private_key = private_key

        if not certificate:
            certificate = self.create_self_signed_cert(private_key)
        if not isinstance(certificate, str):
            certificate = certificate.decode()

        self.certificate = certificate

        if credentials:
            self.credentials = credentials

    def __repr__(self):
        print("email: {}, hrn: {}, pkey: {}".format(self.email,self.hrn,self.private_key))

    def create_self_signed_cert(self, private_key=None):
        if not private_key:
            # create a key pair
            k = crypto.PKey()
            k.generate_key(crypto.TYPE_RSA, 1024)
        else:
            k = crypto.load_privatekey(crypto.FILETYPE_PEM, private_key)

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
        from myslicelib.util.certificate import Keypair, Certificate
        keypair = Keypair(filename = self.private_key.encode('latin1'))
        self_signed = Certificate(subject = self.hrn)
        self_signed.set_pubkey(keypair)
        self_signed.set_issuer(keypair, subject = self.hrn.encode('latin1'))
        self_signed.set_data('email:' + self.email, 'subjectAltName')
        self_signed.sign()
        return self_signed.save_to_string()
