#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: common.py 124054 2017-11-16 05:21:47Z carlos.sanchez $
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import uuid

from datetime import datetime

from nti.contenttypes.credit import NTI
from nti.contenttypes.credit import AWARDED_CREDIT_NTIID_TYPE
from nti.contenttypes.credit import AWARDABLE_CREDIT_NTIID_TYPE
from nti.contenttypes.credit import CREDIT_DEFINITION_NTIID_TYPE

from nti.coremetadata.interfaces import SYSTEM_USER_NAME

from nti.ntiids.ntiids import make_ntiid
from nti.ntiids.ntiids import make_specific_safe

logger = __import__('logging').getLogger(__name__)


def _generate_ntiid(nttype, provider=NTI, now=None):
    now = datetime.utcnow() if now is None else now
    dstr = now.strftime("%Y%m%d%H%M%S %f")
    rand = str(uuid.uuid4().time_low)
    specific = make_specific_safe(u"%s_%s_%s" % (SYSTEM_USER_NAME, dstr, rand))
    result = make_ntiid(provider=provider,
                        nttype=nttype,
                        specific=specific)
    return result


def generate_awarded_credit_ntiid(provider=NTI, now=None):
    return _generate_ntiid(AWARDED_CREDIT_NTIID_TYPE, provider, now)


def generate_awardable_credit_ntiid(provider=NTI, now=None):
    return _generate_ntiid(AWARDABLE_CREDIT_NTIID_TYPE, provider, now)


def generate_credit_definition_ntiid(provider=NTI, now=None):
    return _generate_ntiid(CREDIT_DEFINITION_NTIID_TYPE, provider, now)
