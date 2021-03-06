# -*- coding: utf-8 -*-

# Model based on https://github.com/llazzaro/django-scheduler
#
# Copyright (c) 2016 Virtual Cable S.L.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
#    * Redistributions of source code must retain the above copyright notice,
#      this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright notice,
#      this list of conditions and the following disclaimer in the documentation
#      and/or other materials provided with the distribution.
#    * Neither the name of Virtual Cable S.L. nor the names of its contributors
#      may be used to endorse or promote products derived from this software
#      without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
.. moduleauthor:: Adolfo Gómez, dkmaster at dkmon dot com
"""

from __future__ import unicode_literals

__updated__ = '2017-12-12'

from django.db import models
from uds.models.UUIDModel import UUIDModel
from django.utils.encoding import python_2_unicode_compatible
# from django.utils.translation import ugettext_lazy as _, ugettext
from uds.models.Tag import TaggingMixin

import logging

logger = logging.getLogger(__name__)


@python_2_unicode_compatible
class Calendar(UUIDModel, TaggingMixin):

    name = models.CharField(max_length=128, default='')
    comments = models.CharField(max_length=256, default='')
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Meta class to declare db table
        """
        db_table = 'uds_calendar'
        app_label = 'uds'

    def save(self, *args, **kwargs):
        logger.debug('Saving calendar')

        res = UUIDModel.save(self, *args, **kwargs)

        # Basically, recalculates all related actions next execution time...
        try:
            for v in self.calendaraction_set.all():
                v.save()
        except Exception:
            pass

        return res

    def __str__(self):
        return 'Calendar "{}" modified on {} with {} rules'.format(self.name, self.modified, self.rules.count())
