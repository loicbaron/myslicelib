'''
Created on Aug 7, 2012, updated October 2015

This API class maps to the MyPLC API of PlanetLab

@author: Ciro Scognamiglio <ciro.scognamiglio@lip6.fr>
'''

import xmlrpc
import csv
import urllib

import logging


class Api(object):

    _map = {
        'Resource' : {
            'get' : {
                'method' : 'GetNodes',
                'properties' : ['hostname','hrn','arch','fcdistro','pldistro']
            }
        },
        'Slice' : {
            'addNodes' : 'AddSliceToNodes',
            'delNodes' : 'DeleteSliceFromNodes'
        },

        'Site' : [
        ]
    }

    def __init__(self, url, method, user, password):
        self.url = url
        self.auth = {
            'AuthMethod'    : method,
            'Username'      : user,
            'AuthString'    : password
        }
        try :
            logging.debug("Using API on %s" % self.url)
            self.api = xmlrpc.ServerProxy(self.url, allow_none=True)
        except TypeError :
            msg = "Invalid configuration"
            logging.error(msg)
            raise TypeError(msg)

    def _method(self, a, b):
        if not self._map[a][b]:
            raise NotImplementedError('Method not found or not implemented')
        else:
            return self._map[a][b]

    def get(self, obj):
        return self.request(self._map[obj]['get']['method'], {}, self._map[obj]['get']['properties'])






    ''' add object(s)
        add to esubject with esid list of eobject with eoids
    '''
    def add(self, esubject, eobject, esid, eoids):
        #print self._method(esubject, 'add' + eobject), esid, eoids
        return self.request( self._method(esubject, 'add' + eobject), esid, eoids )


    def update(self, eobject):
        pass

    def insert(self, eobject):
        pass

    def delete(self):
        pass

    def select(self, etype, efilter, ereturn):
        return self.request('Get' + etype, efilter, ereturn)

    def request(self, emethod, efilter, ereturn):
        logging.info("Sending %s({auth}, %s)" % ( emethod, efilter ))
        if ereturn:
            return getattr(self.api, emethod)(self.auth, efilter, ereturn)
        else:
            return getattr(self.api, emethod)(self.auth, efilter)

'''
/usr/local/lib/python2.7/dist-packages/manifold/bin/shell.py

---
srv = xmlrpclib.Server("http://localhost:7080/", allow_none = True)

q = {
    'object':    'resource',
    'filter':    [ 'a', 'b' ],
    'fields':    [ 'hrn','urn' ],
    'action':    'get/create/delete..'
}

ret = srv.forward(auth, q)
'''
