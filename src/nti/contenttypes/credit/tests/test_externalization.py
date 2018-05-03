#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods,arguments-differ

from hamcrest import is_
from hamcrest import is_not
from hamcrest import not_none
from hamcrest import assert_that
from hamcrest import has_property

from nti.testing.matchers import verifiably_provides

import fudge
import unittest

from zope import component

from zc.intid import IIntIds

from nti.contenttypes.credit.credit import AwardableCredit
from nti.contenttypes.credit.credit import CreditDefinition
from nti.contenttypes.credit.credit import CreditDefinitionContainer

from nti.contenttypes.credit.interfaces import ICreditDefinition

from nti.contenttypes.credit.tests import SharedConfiguringTestLayer

from nti.externalization.externalization import to_external_object
from nti.externalization.externalization import StandardExternalFields

from nti.externalization.internalization import update_from_external_object

from nti.externalization.internalization import find_factory_for

from nti.intid.common import add_intid

CLASS = StandardExternalFields.CLASS
MIMETYPE = StandardExternalFields.MIMETYPE
CREATED_TIME = StandardExternalFields.CREATED_TIME
LAST_MODIFIED = StandardExternalFields.LAST_MODIFIED


class TestExternalization(unittest.TestCase):

    layer = SharedConfiguringTestLayer

    def test_credit_definition(self):
        container = CreditDefinitionContainer()
        credit_definition = CreditDefinition(credit_type=u'Credit',
                                             credit_units=u'Hours')
        assert_that(credit_definition,
                    verifiably_provides(ICreditDefinition))

        ext_obj = to_external_object(credit_definition)
        assert_that(ext_obj[CLASS], is_('CreditDefinition'))
        assert_that(ext_obj[MIMETYPE],
                    is_(CreditDefinition.mime_type))
        assert_that(ext_obj[CREATED_TIME], not_none())
        assert_that(ext_obj[LAST_MODIFIED], not_none())
        assert_that(ext_obj['credit_type'], is_(u'Credit'))
        assert_that(ext_obj['credit_units'], is_(u'Hours'))

        factory = find_factory_for(ext_obj)
        assert_that(factory, not_none())
        new_io = factory()
        new_io.__parent__ = container
        update_from_external_object(new_io, ext_obj, require_updater=True)

        assert_that(new_io, has_property('credit_type', is_(u'Credit')))
        assert_that(new_io, has_property('credit_units', is_(u'Hours')))

    def test_equality(self):
        cd1 = CreditDefinition(credit_type=u'Credit', credit_units=u'Hours')
        cd2 = CreditDefinition(credit_type=u'Credit_other', credit_units=u'Hours')
        cd3 = CreditDefinition(credit_type=u'Credit', credit_units=u'Hours_other')
        cd4 = CreditDefinition(credit_type=u'Credit', credit_units=u'Hours')
        assert_that(cd1, is_(cd4))
        assert_that(cd1, is_not(cd2))
        assert_that(cd1, is_not(cd3))

    def test_awardable_credit(self):
        credit_definition = CreditDefinition(credit_type=u'Credit',
                                             credit_units=u'Hours')
        intids = fudge.Fake().provides('getObject').returns(credit_definition)
        intids.provides('getId').returns(10)
        component.getGlobalSiteManager().registerUtility(intids, IIntIds)
        add_intid(credit_definition)
        awardable_credit = AwardableCredit(amount=42,
                                           credit_definition=credit_definition)

        ext_obj = to_external_object(awardable_credit)
        assert_that(ext_obj[CLASS], is_('AwardableCredit'))
        assert_that(ext_obj[MIMETYPE],
                    is_(AwardableCredit.mime_type))
        assert_that(ext_obj[CREATED_TIME], not_none())
        assert_that(ext_obj[LAST_MODIFIED], not_none())
        assert_that(ext_obj['amount'], is_(42))
        assert_that(ext_obj['credit_definition']['credit_type'], is_(u'Credit'))
        assert_that(ext_obj['credit_definition']['credit_units'], is_(u'Hours'))

        factory = find_factory_for(ext_obj)
        assert_that(factory, not_none())
