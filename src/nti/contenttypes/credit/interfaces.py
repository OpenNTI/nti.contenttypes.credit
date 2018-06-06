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

from zope.container.interfaces import IContained
from zope.container.interfaces import IContainer

from nti.base.interfaces import ICreated
from nti.base.interfaces import ILastModified

from nti.ntiids.schema import ValidNTIID

from nti.schema.field import Number
from nti.schema.field import Object
from nti.schema.field import ValidDatetime
from nti.schema.field import IndexedIterable
from nti.schema.field import DecodingValidTextLine as ValidTextLine


class ICreditDefinition(IContained, ICreated, ILastModified):
    """
    The basic credit type object. This may be defined once and referenced in
    many places.
    """
    credit_type = ValidTextLine(title=u'The credit type',
                                required=True,
                                min_length=1,
                                max_length=16)

    credit_units = ValidTextLine(title=u'The course units (hours, points, etc)',
                                 description=u'The course units (hours, points, etc)',
                                 required=True,
                                 default='',
                                 min_length=0,
                                 max_length=16)

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

    def add_credit_definition(new_credit_definition):
        """
        Insert the :class:`ICreditDefinition` by ntiid. This will de-dupe, ensuring
        that only one credit definition is in this container. This will return the
        credit definition object stored in the container.
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


class IAwardableCreditContext(interface.Interface):
    """
    An object that contains one or many :class:`IAwardableCredit` objects.
    """

    awardable_credits = IndexedIterable(value_type=Object(IAwardableCredit),
                                        title=u"The awardable credits",
                                        required=False,
                                        min_length=0)


class IAwardedCredit(ICreated, ILastModified, IContained):
    """
    A credit that has been awarded to a user.
    """
    title = ValidTextLine(title=u"Title of the awarded credit",
                          min_length=2,
                          required=True)

    description = ValidTextLine(title=u"Description of the awarded credit", required=False)

    credit_definition = Object(ICreditDefinition,
                               title=u'The credit definition',
                               required=True)

    amount = Number(title=u"Amount",
                   description=u"The amount of the ICreditDefinition units that are awarded.",
                   required=True,
                   min=0.0,
                   default=None)

    awarded_date = ValidDatetime(title=u"This awarded date",
                                 description=u"""When the credit was awarded. If not provided, will
                                 default to created date.""",
                                 required=True)

    issuer = ValidTextLine(title=u"This issue of the credit",
                           description=u"""This issue of the credit.""",
                           required=False)

    NTIID = ValidNTIID(title=u"The NTIID of the awarded credit",
                       required=False)


class ICreditTranscript(IContainer):
    """
    An object that provides :class:`IAwardedCredit` objects earned by a user.
    """

    contains(IAwardedCredit)

    def iter_awarded_credits():
        """
        Returns an iterator over the :class:`IAwardedCredit` objects in this
        transcript.
        """
