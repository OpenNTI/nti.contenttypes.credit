#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from zope import component
from zope import interface

from nti.contenttypes.credit.interfaces import ICreditDefinitionContainer

from nti.ntiids.interfaces import INTIIDResolver

logger = __import__('logging').getLogger(__name__)


@interface.implementer(INTIIDResolver)
class _CreditDefinitionNTIIDResolver(object):
    """
    Resolves credit definition objects through the container.
    """

    def resolve(self, ntiid):
        def_container = component.queryUtility(ICreditDefinitionContainer)
        try:
            return def_container.get_credit_definition(ntiid)
        except (AttributeError, KeyError):
            pass
        return None
