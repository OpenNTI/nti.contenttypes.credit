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

from nti.contenttypes.credit.common import generate_awarded_credit_ntiid
from nti.contenttypes.credit.common import generate_awardable_credit_ntiid
from nti.contenttypes.credit.common import generate_credit_definition_ntiid

from nti.contenttypes.credit.interfaces import IAwardedCredit
from nti.contenttypes.credit.interfaces import IAwardableCredit
from nti.contenttypes.credit.interfaces import ICreditDefinition
from nti.contenttypes.credit.interfaces import ICreditDefinitionContainer

from nti.containers.containers import CaseInsensitiveCheckingLastModifiedBTreeContainer

from nti.dublincore.time_mixins import PersistentCreatedAndModifiedTimeObject

from nti.externalization.representation import WithRepr

from nti.property.property import alias

from nti.schema.fieldproperty import createDirectFieldProperties

from nti.schema.schema import SchemaConfigured

from nti.wref.interfaces import IWeakRef

logger = __import__('logging').getLogger(__name__)


@WithRepr
@interface.implementer(ICreditDefinition)
class CreditDefinition(PersistentCreatedAndModifiedTimeObject,
                       Contained,
                       SchemaConfigured):
    createDirectFieldProperties(ICreditDefinition)

    __parent__ = None
    __name__ = None

    creator = None
    NTIID = alias('ntiid')

    mimeType = mime_type = "application/vnd.nextthought.credit.creditdefinition"

    def __eq__(self, other):
        try:
            return self is other \
                or (self.credit_type.lower(), self.credit_units.lower()) == (other.credit_type.lower(), other.credit_units.lower())
        except AttributeError:
            return NotImplemented

    def _ne__(self, other):
        try:
            return self is not other \
                and (self.credit_type.lower(), self.credit_units.lower()) != (other.credit_type.lower(), other.credit_units.lower())
        except AttributeError:
            return NotImplemented

    @Lazy
    def ntiid(self):
        return generate_credit_definition_ntiid()


@interface.implementer(ICreditDefinitionContainer)
class CreditDefinitionContainer(CaseInsensitiveCheckingLastModifiedBTreeContainer,
                                SchemaConfigured):
    createDirectFieldProperties(ICreditDefinitionContainer)

    __parent__ = None

    def get_credit_definition(self, ntiid):
        """
        Lookup the :class:`ICreditDefinition` by ntiid.

        TODO: We should queryNextUtility lookup too.
        """
        return self.get(ntiid)

    def add_credit_definition(self, new_credit_definition):
        # TODO: queryNextUtility
        # De-duping; this should be small per site.
        credit_definition = self.get_credit_definition_by(new_credit_definition.credit_type, new_credit_definition.credit_units)
        if credit_definition is not None:
            return credit_definition

        self[new_credit_definition.ntiid] = new_credit_definition
        return new_credit_definition

    def get_credit_definition_by(self, credit_type, credit_units):
        if credit_type is None or credit_units is None:
            return None
        for x in self.values():
            if (x.credit_type.lower(), x.credit_units.lower()) == (credit_type.lower(), credit_units.lower()):
                return x
        return None


@WithRepr
@interface.implementer(IAwardableCredit)
class AwardableCredit(PersistentCreatedAndModifiedTimeObject,
                      SchemaConfigured):
    createDirectFieldProperties(IAwardableCredit)

    __parent__ = None
    _credit_definition = None

    creator = None
    NTIID = alias('ntiid')

    mimeType = mime_type = "application/vnd.nextthought.credit.awardablecredit"

    def __init__(self, *args, **kwargs):
        super(AwardableCredit, self).__init__(*args, **kwargs)
        SchemaConfigured.__init__(self, *args, **kwargs)

    @property
    def credit_definition(self):
        result = None
        if self._credit_definition is not None:
            result = self._credit_definition()
        return result

    @credit_definition.setter
    def credit_definition(self, value):
        self._credit_definition = IWeakRef(value)

    @Lazy
    def ntiid(self):
        return generate_awardable_credit_ntiid()


@WithRepr
@interface.implementer(IAwardedCredit)
class AwardedCredit(PersistentCreatedAndModifiedTimeObject,
                    SchemaConfigured):

    createDirectFieldProperties(IAwardedCredit)
    __external_can_create__ = False

    __parent__ = None
    _credit_definition = None
    creator = None
    NTIID = alias('ntiid')

    mimeType = mime_type = "application/vnd.nextthought.credit.awardedcredit"

    def __init__(self, *args, **kwargs):
        super(AwardedCredit, self).__init__(*args, **kwargs)
        SchemaConfigured.__init__(self, *args, **kwargs)

    @property
    def credit_definition(self):
        result = None
        if self._credit_definition is not None:
            result = self._credit_definition()
        return result

    @credit_definition.setter
    def credit_definition(self, value):
        self._credit_definition = IWeakRef(value)

    @Lazy
    def ntiid(self):
        return generate_awarded_credit_ntiid()

    @Lazy
    def issuer(self):
        return getattr(self.creator, 'username', self.creator)

    @Lazy
    def awarded_date(self):
        return self.created
