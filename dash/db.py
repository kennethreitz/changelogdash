# -*- coding: utf-8 -*-

"""
dash.db
~~~~~~~

This module provides the Dashboard database interface.
"""

import os
from redis import Redis, from_url


__all__ = ('redis_connect',)



def redis_connect():
    """Connect to appropriate Redis system. Returns Redis instance. """

    try:
        # ep.io configuration
        # Leaving in memorium.
        from bundle_config import config
        r = Redis(
            host = config['redis']['host'],
            port = int(config['redis']['port']),
            password = config['redis']['password'],
        )
    except ImportError:
        # TODO: use local settings (env?)
        # r = Redis(host='localhost', port=6379, db=0)

        r = from_url(os.environ.get('OPENREDIS_URL'))

    return r