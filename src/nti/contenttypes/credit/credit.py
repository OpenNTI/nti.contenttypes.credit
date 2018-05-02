#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id: model.py 123306 2017-10-19 03:47:14Z carlos.sanchez $
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from zope import interface

from zope.cachedescriptors.property import Lazy

from zope.container.contained import Contained

from nti.contenttypes.credit.interfaces import IAwardableCredit
from nti.contenttypes.credit.interfaces import ICreditDefinition
from nti.contenttypes.credit.interfaces import IAwardableCreditContainer
from nti.contenttypes.credit.interfaces import ICreditDefinitionContainer

from nti.containers.containers import CaseInsensitiveCheckingLastModifiedBTreeContainer

from nti.dublincore.time_mixins import PersistentCreatedAndModifiedTimeObject

from nti.externalization.representation import WithRepr

from nti.ntiids.oids import to_external_ntiid_oid

from nti.property.property import alias

from nti.schema.fieldproperty import createDirectFieldProperties

from nti.schema.schema import SchemaConfigured

from nti.wref.interfaces import IWeakRef

logger = __import__('logging').getLogger(__name__)


@WithRepr
@interface.implementer(ICreditDefinition)
class CreditDefinition(PersistentCreatedAndModifiedTimeObject, Contained, SchemaConfigured):
    createDirectFieldProperties(ICreditDefinition)

    __parent__ = None
    __name__ = None
    NTIID = alias('ntiid')

    mimeType = mime_type = "application/vnd.nextthought.credit.creditdefinition"

    @Lazy
    def ntiid(self):
        return to_external_ntiid_oid(self)


@interface.implementer(ICreditDefinitionContainer)
class CreditDefinitionContainer(CaseInsensitiveCheckingLastModifiedBTreeContainer,
                                SchemaConfigured):
    createDirectFieldProperties(ICreditDefinitionContainer)

    __parent__ = None


@WithRepr
@interface.implementer(IAwardableCredit)
class AwardableCredit(PersistentCreatedAndModifiedTimeObject, SchemaConfigured):
    createDirectFieldProperties(IAwardableCredit)

    __parent__ = None
    _credit_definition = None
    NTIID = alias('ntiid')

    mimeType = mime_type = "application/vnd.nextthought.credit.awardablecredit"

    def __init__(self, credit_definition=None, *args, **kwargs):
        SchemaConfigured.__init__(self, *args, **kwargs)
        self._credit_definition = IWeakRef(credit_definition)

    @property
    def credit_definition(self):
        result = None
        if self._credit_definition is not None:
            result = self._credit_definition()
        return result

    @Lazy
    def ntiid(self):
        return to_external_ntiid_oid(self)


@interface.implementer(IAwardableCreditContainer)
class AwardableCreditContainer(CaseInsensitiveCheckingLastModifiedBTreeContainer,
                                SchemaConfigured):
    createDirectFieldProperties(IAwardableCreditContainer)

    __parent__ = None

    def get_awardable_credits_for_user(self, unused_user):
        """
        Return the awardable credits that may be possible for the given user.
        """
        return [x for x in self.values()]
