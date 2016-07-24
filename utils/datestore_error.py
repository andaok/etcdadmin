#-*- coding: utf-8 -*-

from utils.__init__ import BaseError


class DataStoreError(BaseError):
    
    pass


class NoEndpoint(DataStoreError):
    
    pass

class MultipleEndpointsMatch(DataStoreError):
    
    pass
