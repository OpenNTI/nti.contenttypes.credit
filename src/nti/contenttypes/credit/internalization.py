#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import collections

import six

from zope import component
from zope import interface

from nti.contenttypes.credit.interfaces import IAwardedCredit
from nti.contenttypes.credit.interfaces import IAwardableCredit
from nti.contenttypes.credit.interfaces import ICreditDefinition
from nti.contenttypes.credit.interfaces import ICreditDefinitionContainer

from nti.externalization.datastructures import InterfaceObjectIO

from nti.externalization.interfaces import IInternalObjectUpdater

logger = __import__('logging').getLogger(__name__)


class AbstractNormalizationUpdater(InterfaceObjectIO):
    """
    Finds and maps to an existing credit definition ref during internalization.
    """

    __slots__ = ('_ext_self',)

    _excluded_in_ivars_ = frozenset(
        getattr(InterfaceObjectIO, '_excluded_in_ivars_').union({'NTIID', 'ntiid'})
    )

    def updateFromExternalObject(self, parsed, *args, **kwargs):
        """
        Normalize our credit definition.
        """
        # Not the best place for this...
        if 'amount' in parsed:
            try:
                if float(parsed['amount']).is_integer():
                    parsed['amount'] = int(parsed['amount'])
            except (TypeError, ValueError):
                pass
        credit_definition = parsed.get('credit_definition')
        if credit_definition is not None:
            if isinstance(credit_definition, six.string_types):
                credit_definition_ntiid = credit_definition
            elif isinstance(credit_definition, collections.Mapping):
                credit_definition_ntiid = credit_definition.get('ntiid')
            else:
                credit_definition_ntiid = getattr(credit_definition, 'ntiid', '')
            if credit_definition_ntiid:
                container = component.getUtility(ICreditDefinitionContainer)
                credit_definition_obj = container.get_credit_definition(credit_definition_ntiid)
                parsed['credit_definition'] = credit_definition_obj
        result = super(AbstractNormalizationUpdater, self).updateFromExternalObject(parsed, *args, **kwargs)
        return result
CreditDefinitionNormalizationUpdater = AbstractNormalizationUpdater

@component.adapter(IAwardedCredit)
@interface.implementer(IInternalObjectUpdater)
class _AwardedCreditUpdater(AbstractNormalizationUpdater):

    _ext_iface_upper_bound = IAwardedCredit


@component.adapter(IAwardableCredit)
@interface.implementer(IInternalObjectUpdater)
class _AwardableCreditUpdater(AbstractNormalizationUpdater):

    _ext_iface_upper_bound = IAwardableCredit


@component.adapter(ICreditDefinition)
@interface.implementer(IInternalObjectUpdater)
class _CreditDefinitinoUpdater(InterfaceObjectIO):

    _ext_iface_upper_bound = ICreditDefinition

    _excluded_in_ivars_ = frozenset(
        getattr(InterfaceObjectIO, '_excluded_in_ivars_').union({'NTIID', 'ntiid'})
    )
