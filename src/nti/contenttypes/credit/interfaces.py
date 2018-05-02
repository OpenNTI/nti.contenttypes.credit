#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=inherit-non-class

from zope import interface

from zope.annotation.interfaces import IAttributeAnnotatable

from zope.container.constraints import contains
from zope.container.constraints import containers

from zope.container.interfaces import IContained
from zope.container.interfaces import IContainer

from nti.ntiids.schema import ValidNTIID

from nti.schema.field import Number
from nti.schema.field import Object
from nti.schema.field import DecodingValidTextLine as ValidTextLine


class ICreditDefinition(IContained):
    """
    The basic credit type object. This may be defined once and referenced in
    many places.
    """
    containers('.ICreditDefinitionContainer')

    credit_type = ValidTextLine(title=u'The credit type',
                                required=True)

    credit_units = ValidTextLine(title=u'The course units (hours, points, etc)',
                                 description=u'The course units (hours, points, etc)',
                                 required=True)

    NTIID = ValidNTIID(title=u"The NTIID of the credit definition",
                       required=False)


class ICreditDefinitionContainer(IContainer):
    """
    A storage container for :class:`ICreditDefinition` objects.
    """
    contains(ICreditDefinition)


class IAwardableCredit(interface.Interface):
    """
    The basic credit type object. This may be defined once and referenced in
    many places.
    """
    containers('.IAwardableCreditContainer')

    credit_definition = Object(ICreditDefinition,
                               title=u'The credit definition',
                               required=True)

    amount = Number(title=u"Amount",
                   description=u"The amount of the ICreditDefinition units that are awarded.",
                   required=True,
                   min=0.0,
                   default=None)

    NTIID = ValidNTIID(title=u"The NTIID of the awardable credit",
                       required=False)


class IAwardableCreditContext(IAttributeAnnotatable):
    """
    An object that may contain awardable credits.
    """


class IAwardableCreditContainer(IContainer):
    """
    An object that stores awardable credits.
    """
    contains(IAwardableCredit)

    def get_awardable_credits_for_user(user):
        """
        Return the awardable credits that may be possible for the given user.
        """
