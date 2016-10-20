#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
'''
@author: Adolfo Gómez, dkmaster at dkmon dot com
'''
from __future__ import unicode_literals

import sys
import os
import errno

USER = '{user}'
KEY = '{key}'

def logError(err):
    print(err)

def updateAuthorizedKeys(user, pubKey):
    # No X2Go server on windows
    if 'win' in sys.platform:
        logError('Not a linux platform')
        return

    # Create .ssh on user home
    home = os.path.expanduser('~{}'.format(user))
    if not os.path.exists(home):  # User not found, nothing done
        logError('Home folder for user {} not found'.format(user))
        return

    sshFolder = '{}/.ssh'.format(home)
    if not os.path.exists(sshFolder):
        try:
            os.makedirs(sshFolder, 0700)
        except OSError as e:
            if e.errno != errno.EEXIST:
                logError('Error creating .ssh folder for user {}: {}'.format(user, e))
                return
            # Folder has been created in between test & creation, thats ok

    authorizedKeys = '{}/authorized_keys'.format(sshFolder)
    try:
        with open(authorizedKeys, 'r') as f:
            lines = f.readlines()
    except Exception:
        lines = []

    with open(authorizedKeys, 'w') as f:
        for line in lines:
            if 'UDS@X2GOCLIENT' not in line and len(line.strip()) > 0:
                f.write(line)
        # Append pubkey
        f.write('ssh-rsa {} UDS@X2GOCLIENT\n'.format(pubKey))

    # Ensure access is correct
    os.chmod(authorizedKeys, 0600)

    # Done

updateAuthorizedKeys(USER, KEY)