#-*- coding:utf-8 -*-

import os
import etcd
from etcd import EtcdKeyNotFound, EtcdException, EtcdNotFile, EtcdKeyError
import json
from utils.tools import get_hostname, validate_hostname_port
from utils.datestore_error import DataStoreError, \
    NoEndpoint, MultipleEndpointsMatch


ETCD_AUTHORITY_DEFAULT = "127.0.0.1:2379"
ETCD_AUTHORITY_ENV = "ETCD_AUTHORITY"
ETCD_ENDPOINTS_ENV = "ETCD_ENDPOINTS"

# Secure etcd with SSL environment variables and paths
ETCD_SCHEME_DEFAULT = "http"
ETCD_SCHEME_ENV = "ETCD_SCHEME"
ETCD_KEY_FILE_ENV = "ETCD_KEY_FILE"
ETCD_CERT_FILE_ENV = "ETCD_CERT_FILE"
ETCD_CA_CERT_FILE_ENV = "ETCD_CA_CERT_FILE"


def handle_errors(fn):
    """
    Decorator function to decorate datastore API methods to handle common
    exception types and re-raise as datastore specific errors.
    :param fn: The function to datastore.
    :return: The decorated function.
    """
    def wrapped(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except EtcdException as e:
            # Don't leak out etcd exceptions.
            raise DataStoreError("%s: Error accessing etcd (%s).  Is etcd "
                                 "running?" % (fn.__name__, e.message))
    return wrapped


class DatastoreClient(object):

    def __init__(self):
        etcd_endpoints = os.getenv(ETCD_ENDPOINTS_ENV, '')
        etcd_authority = os.getenv(ETCD_AUTHORITY_ENV, ETCD_AUTHORITY_DEFAULT)
        etcd_scheme = os.getenv(ETCD_SCHEME_ENV, ETCD_SCHEME_DEFAULT)
        etcd_key = os.getenv(ETCD_KEY_FILE_ENV, '')
        etcd_cert = os.getenv(ETCD_CERT_FILE_ENV, '')
        etcd_ca = os.getenv(ETCD_CA_CERT_FILE_ENV, '')

        addr_env = None
        scheme_env = None
        etcd_addrs_raw = []
        if etcd_endpoints:
            # ETCD_ENDPOINTS specified: use it to determine scheme and etcd
            # location.
            endpoints = [x.strip() for x in etcd_endpoints.split(",")]
            try:
                scheme = None
                for e in endpoints:
                    s, a = e.split("://")
                    etcd_addrs_raw.append(a)
                    if scheme == None:
                        scheme = s
                    else:
                        if scheme != s:
                            raise DataStoreError(
                                "Inconsistent protocols in %s.  Value "
                                "provided is '%s'" %
                                (ETCD_ENDPOINTS_ENV, etcd_endpoints)
                            )
                etcd_scheme = scheme
                addr_env = ETCD_ENDPOINTS_ENV
                scheme_env = ETCD_ENDPOINTS_ENV
            except ValueError:
                raise DataStoreError("Invalid %s. It must take the form"
                                     "'ENDPOINT[,ENDPOINT][,...]' where "
                                     "ENDPOINT:='http[s]://ADDRESS:PORT'. "
                                     "Value provided is '%s'" %
                                     (ETCD_ENDPOINTS_ENV, etcd_endpoints))
        else:
            # ETCD_ENDPOINTS not specified, fall back to ETCD_AUTHORITY and
            # ETCD_SCHEME instead.
            etcd_addrs_raw.append(etcd_authority)
            addr_env = ETCD_AUTHORITY_ENV
            scheme_env = ETCD_SCHEME_ENV

        etcd_addrs = []
        for addr in etcd_addrs_raw:
            if not validate_hostname_port(addr):
                raise DataStoreError(
                    "Invalid %s. Address must take the form "
                    "<address>:<port>. Value provided is '%s'" %
                    (addr_env, addr)
                )
            (host, port) = addr.split(":", 1)
            etcd_addrs.append((host, int(port)))

        key_pair = (etcd_cert, etcd_key) if (etcd_cert and etcd_key) else None

        if etcd_scheme == "https":
            # key and certificate must be both specified or both not specified
            if bool(etcd_key) != bool(etcd_cert):
                raise DataStoreError("Invalid %s, %s combination. Key and "
                                     "certificate must both be specified or "
                                     "both be blank. Values provided: %s=%s, "
                                     "%s=%s" % (ETCD_KEY_FILE_ENV,
                                                ETCD_CERT_FILE_ENV,
                                                ETCD_KEY_FILE_ENV, etcd_key,
                                                ETCD_CERT_FILE_ENV, etcd_cert))
            # Make sure etcd key and certificate are readable
            if etcd_key and etcd_cert and not (os.path.isfile(etcd_key) and
                                               os.access(etcd_key, os.R_OK) and
                                               os.path.isfile(etcd_cert) and
                                               os.access(etcd_cert, os.R_OK)):
                raise DataStoreError("Cannot read %s and/or %s. Both must "
                                     "be readable file paths. Values "
                                     "provided: %s=%s, %s=%s" %
                                     (ETCD_KEY_FILE_ENV,
                                      ETCD_CERT_FILE_ENV,
                                      ETCD_KEY_FILE_ENV, etcd_key,
                                      ETCD_CERT_FILE_ENV, etcd_cert))
            # Certificate Authority cert must be provided, check it's readable
            if not etcd_ca or not (os.path.isfile(etcd_ca) and
                                   os.access(etcd_ca, os.R_OK)):
                raise DataStoreError("Invalid %s. Certificate Authority "
                                     "cert is required and must be a "
                                     "readable file path. Value provided: "
                                     "%s" % (ETCD_CA_CERT_FILE_ENV, etcd_ca))
        elif etcd_scheme != "http":
            raise DataStoreError("Invalid %s. Value must be one of: \"\", "
                                 "\"http\", \"https\". Value provided: %s" %
                                 (scheme_env, etcd_scheme))

        # Set CA value to None if it is a None-value string
        etcd_ca = None if not etcd_ca else etcd_ca

        # python-etcd Client requires a different invocation when there's only
        # a single etcd host.
        if len(etcd_addrs) > 1:
            # Specify allow_reconnect when there are multiple endpoints, so
            # python-etcd will try connecting to all of them if one fails.
            self.etcd_client = etcd.Client(host=tuple(etcd_addrs),
                                           protocol=etcd_scheme,
                                           cert=key_pair,
                                           ca_cert=etcd_ca,
                                           allow_reconnect=True)
        else:
            self.etcd_client = etcd.Client(host=etcd_addrs[0][0],
                                           port=etcd_addrs[0][1],
                                           protocol=etcd_scheme,
                                           cert=key_pair,
                                           ca_cert=etcd_ca)

        def to_json(self, indent=None):
            """
            Convert the Rules object to a JSON string.
    
            :param indent: Integer representing the level of indent from the
            returned json string. None = no indent, 0 = only newlines. Recommend
            using 1 for human-readable strings.
            :return:  A JSON string representation of this object.
            """
            return json.dumps(self.to_dict(), indent=indent)

        def __repr__(self):
            return self.__str__()