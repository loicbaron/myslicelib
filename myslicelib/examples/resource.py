#!/usr/bin/env python3

from myslicelib.query.resource import ResourceQuery

'''
Resource Query examples
'''

'''
Returns a collection (model.Entities) object with the list of resources. Each element of the collection
is a Resource object (model.Resource)
'''
resources = ResourceQuery().all()

'''
Returns a specific resource by id, resource is a resource object (mode.Resource
'''
id = 'example.urn.resourceid'
resource = ResourceQuery().get(id)

'''
Modifies a property of a resource
'''
id = 'example.urn.resourceid'
resource = ResourceQuery().get(id)
resource.description = "This is a new description"
resource.save()