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

from zope.container.constraints import contains
from zope.container.constraints import containers

from zope.container.interfaces import IContained
from zope.container.interfaces import IContainer

from nti.base.interfaces import ICreated
from nti.base.interfaces import ILastModified

from nti.ntiids.schema import ValidNTIID

from nti.schema.field import Number
from nti.schema.field import Object
from nti.schema.field import DecodingValidTextLine as ValidTextLine


class ICreditDefinition(IContained, ICreated, ILastModified):
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
    A storage container for :class:`ICreditDefinition` objects, accessible as
    a registered utility.
    """
    contains(ICreditDefinition)

    def get_credit_definition(ntiid):
        """
        Lookup the :class:`ICreditDefinition` by ntiid.
        """


class IAwardableCredit(ICreated, ILastModified):
    """
    Composes a credit definition with a value amount, useful for displaying.
    """
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


class IAwardedCredit(ICreated, ILastModified):
    """
    A credit that has been awarded to a user.
    """
    title = ValidTextLine(title=u"Title of the awarded credit", required=True)

    description = ValidTextLine(title=u"Description of the awarded credit", required=False)

    credit_definition = Object(ICreditDefinition,
                               title=u'The credit definition',
                               required=True)

    amount = Number(title=u"Amount",
                   description=u"The amount of the ICreditDefinition units that are awarded.",
                   required=True,
                   min=0.0,
                   default=None)

    NTIID = ValidNTIID(title=u"The NTIID of the awarded credit",
                       required=False)


class ICreditTranscript(interface.Interface):
    """
    An object that provides :class:`IAwardedCredit` objects earned by a user.
    """
