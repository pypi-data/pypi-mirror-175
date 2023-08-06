# Copyright (C) 2022 Quantuloop - All rights reserved
from ctypes import *
from ket.base import set_quantum_execution_target, set_process_features
from ket.clib.wrapper import load_lib
from os import environ
from os.path import dirname
import jwt
import warnings

_ql_pubkey = """\
-----BEGIN PUBLIC KEY-----
MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAqMVLlLgPaisE4Se3oqqF
1zgxFsQuBpv46d25X60FnGe2TVbqxz6lCVT33oowk22b9sMVjTkMoFCL4ocTCQxP
PLUqNgJnWAGr1GpdUvTzWgB5An2V9rKvknfLuSfoCeVIV5qxonz45Yh/F83cDjU3
T4+oXDjvadc9rGQmKhZ46yPeeODj/EGwcGUbgOcg3g3SckfO035NXrWfz8ndUWre
zrbHHAJdpCfEh9yBct9qMcVeQ3nlRwHG8z7d9/d8XKCujvEOWs3WV/kHt5B+M4Xc
29BtyaRFJ/kpluz+glA6eYtwPx3VRc/4QXjEVz6jOjEUe/rdATJUmL3LA/P5iawI
zGPe8qUAbLrY9fRIoAyA9NELtt61Vqrez3/i89MqX8wEc7CDzKmzafFwGJrdEhCp
WkN9eR6dJ7jtJsqXdm+CKJ+Le/4u/rqM+hWjIKjERPHTMGHwzHhWAQgAopasu/SJ
OtSm7/au1KBYG8efS0Q1KXl7xO3B8CxS5iKGtOgqW1mwZ/0V9Cx22NHdHteWEJtj
plVVSEgb5yZLX9hnTBbQaVmo3Up6QzCbIR8r/p9HKzJ/gWarvpy26T+rO5Rh+JdY
YKrqZc6vpo3uYm+7jLWGFsTH0JesgwYXkK59nuOPIoGEBLtPIl5CuZS7awMH5mSM
QWbrTs7JkgcoZ9HgU17m+y8CAwEAAQ==
-----END PUBLIC KEY-----
"""

API = load_lib(
    'Quantuloop PBW',
    dirname(__file__)+"/libpbw.so",
    {
        'quloop_pbw_run_and_set_result': ([c_void_p], []),
        'quloop_pbw_run_serialized': ([POINTER(c_uint8), c_size_t, POINTER(c_uint8), c_size_t, c_int32], [c_void_p]),
        'kbw_result_get': ([c_void_p], [POINTER(c_uint8), c_size_t]),
        'kbw_result_delete': ([c_void_p], []),
    },
    'kbw_error_message'
)


def run_and_set_result(process):
    if 'QL_TOKEN' not in environ:
        warnings.warn(
            'Quantuloop token undefined, please set your token with function "quantuloop.pbw.set_token()"')
    else:
        try:
            jwt.decode(environ['QL_TOKEN'], _ql_pubkey,
                       algorithms=['RS256'], audience="sim")
        except Exception as e:
            warnings.warn(str(e))

    API['quloop_pbw_run_and_set_result'](process)


def use_pbw():
    """Set PBW as the quantum execution target for Ket"""
    from os import environ
    environ['PBW_PATH'] = dirname(__file__)+'/lib'
    set_process_features()
    set_quantum_execution_target(run_and_set_result)


def set_token(token=None, file=None):
    """Set your Quantuloop token

    Args:
        token: token string.
        file: token file path.
    """
    if file is not None:
        with open(file, 'r') as file:
            token = file.read()
    environ['QL_TOKEN'] = token


def set_precision(precision: str):
    """Set float point precision for simulation

    Args:
        precision: Possible values are "single" and "double".

    Raises:
        ValueError: If `precision` is not "single" or "double"
    """

    if precision.upper() == "DOUBLE":
        environ['PBW_PRECISION'] = 'double'
    elif precision.upper() == "SINGLE":
        environ['PBW_PRECISION'] = 'single'
    else:
        raise ValueError("argument 'precision' must be 'double' or 'single'")


def set_num_gpus(n: int):
    """Set the number of GPUs used for the simulation

    Args:
        n: number of GPUs.    
    """

    environ['PBW_GPU_COUNT'] = str(n)


use_pbw()
