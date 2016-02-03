from myslicelib.util.url import validateUrl

class Endpoint(object):
    """
    An endpoint specifies a remote API endpoint.
    type is the type of endpoint, e.g. AM, Reg
    protocol specifies the protocol, default is SFA
    url is the remote url
    """

    def __init__(self, type="AM", protocol="SFA", url=None):
        self.type = type
        self.protocol = protocol
        if not url or not validateUrl(url):
            raise ValueError("URL not valid")
        else:
            self.url = url



    def __str__(self):
        return self.url


class Credential(object):

    def __init__(self, userid=None, password=None, email=None, hrn=None, private_key=None, certificate=None):
        if not private_key or not email or not hrn:
            raise ValueError("private key, email and hrn must be specified")
            exit(1)

        self.email = email
        self.hrn = hrn
        self.private_key = private_key

        # if not certfile:
        #     self.certificate = self.sign_certificate() #
        # else:
        self.certificate = certificate

    # def sign_certificate(self):
    #     keypair = Keypair(filename = self.pkey.encode('latin1'))
    #     self_signed = Certificate(subject = self.hrn)
    #     self_signed.set_pubkey(keypair)
    #     self_signed.set_issuer(keypair, subject = self.hrn.encode('latin1'))
    #     self_signed.set_data('email:' + self.email, 'subjectAltName')
    #     self_signed.sign()
    #     return self_signed.save_to_string()