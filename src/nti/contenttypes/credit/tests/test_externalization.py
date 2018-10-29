#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods,arguments-differ

from hamcrest import is_
from hamcrest import none
from hamcrest import is_not
from hamcrest import not_none
from hamcrest import has_length
from hamcrest import assert_that
from hamcrest import has_property
from hamcrest import same_instance

from nti.testing.matchers import verifiably_provides

import fudge
import unittest

from datetime import datetime
from datetime import timedelta

from zope import component

from zc.intid import IIntIds

from nti.contenttypes.credit.credit import AwardedCredit
from nti.contenttypes.credit.credit import AwardableCredit
from nti.contenttypes.credit.credit import CreditDefinition
from nti.contenttypes.credit.credit import CreditDefinitionContainer

from nti.contenttypes.credit.interfaces import ICreditDefinition
from nti.contenttypes.credit.interfaces import ICreditDefinitionContainer

from nti.contenttypes.credit.tests import SharedConfiguringTestLayer

from nti.externalization.externalization import to_external_object
from nti.externalization.externalization import StandardExternalFields

from nti.externalization.internalization import find_factory_for
from nti.externalization.internalization import update_from_external_object

from nti.intid.common import add_intid

from nti.ntiids.ntiids import find_object_with_ntiid

CLASS = StandardExternalFields.CLASS
MIMETYPE = StandardExternalFields.MIMETYPE
CREATED_TIME = StandardExternalFields.CREATED_TIME
LAST_MODIFIED = StandardExternalFields.LAST_MODIFIED


class TestExternalization(unittest.TestCase):

    layer = SharedConfiguringTestLayer

    def setUp(self):
        self.container = CreditDefinitionContainer()
        component.getGlobalSiteManager().registerUtility(self.container,
                                                         ICreditDefinitionContainer)

    def tearDown(self):
        component.getGlobalSiteManager().unregisterUtility(self.container,
                                                           ICreditDefinitionContainer)

    def test_credit_definition(self):
        credit_definition = CreditDefinition(credit_type=u'Credit',
                                             credit_units=u'Hours')
        credit_definition2 = CreditDefinition(credit_type=u'Credit',
                                              credit_units=u'Hours')
        definition_ntiid = credit_definition.ntiid
        assert_that(credit_definition.ntiid, is_(definition_ntiid))
        assert_that(credit_definition,
                    verifiably_provides(ICreditDefinition))

        # NTIID resolving
        found_definition = find_object_with_ntiid(definition_ntiid)
        assert_that(found_definition, none())
        self.container[definition_ntiid] = credit_definition

        # De-duping
        added_def = self.container.add_credit_definition(credit_definition)
        assert_that(added_def, is_(credit_definition))

        added_def = self.container.add_credit_definition(credit_definition2)
        assert_that(added_def, is_(credit_definition))

        found_definition = find_object_with_ntiid(definition_ntiid)
        assert_that(found_definition, is_(credit_definition))

        ext_obj = to_external_object(credit_definition)
        assert_that(ext_obj[CLASS], is_('CreditDefinition'))
        assert_that(ext_obj[MIMETYPE],
                    is_(CreditDefinition.mime_type))
        assert_that(ext_obj[CREATED_TIME], not_none())
        assert_that(ext_obj[LAST_MODIFIED], not_none())
        assert_that(ext_obj['credit_type'], is_(u'Credit'))
        assert_that(ext_obj['credit_units'], is_(u'Hours'))
        assert_that(ext_obj['NTIID'], is_(definition_ntiid))

        factory = find_factory_for(ext_obj)
        assert_that(factory, not_none())
        new_io = factory()
        new_io.__parent__ = self.container
        update_from_external_object(new_io, ext_obj, require_updater=True)

        assert_that(new_io, has_property('credit_type', is_(u'Credit')))
        assert_that(new_io, has_property('credit_units', is_(u'Hours')))
        assert_that(new_io, has_property('NTIID', is_(definition_ntiid)))

        credit_definition = CreditDefinition(credit_type=u'Credit')
        ext_obj = to_external_object(credit_definition)
        assert_that(ext_obj[CLASS], is_('CreditDefinition'))
        assert_that(ext_obj[MIMETYPE],
                    is_(CreditDefinition.mime_type))
        assert_that(ext_obj[CREATED_TIME], not_none())
        assert_that(ext_obj[LAST_MODIFIED], not_none())
        assert_that(ext_obj['credit_type'], is_(u'Credit'))
        assert_that(ext_obj['credit_units'], is_(u''))

    def test_equality(self):
        cd1 = CreditDefinition(credit_type=u'Credit', credit_units=u'Hours')
        cd2 = CreditDefinition(credit_type=u'Credit_other', credit_units=u'Hours')
        cd3 = CreditDefinition(credit_type=u'Credit', credit_units=u'Hours_other')
        cd4 = CreditDefinition(credit_type=u'Credit', credit_units=u'Hours')
        cd_lower = CreditDefinition(credit_type=u'credit', credit_units=u'hours')
        assert_that(cd1, is_(cd4))
        assert_that(cd1, is_not(cd2))
        assert_that(cd1, is_not(cd3))
        assert_that(cd1, is_(cd_lower))

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

    def test_awarded_credit(self):
        credit_definition = CreditDefinition(credit_type=u'Credit',
                                             credit_units=u'Hours')
        intids = fudge.Fake().provides('getObject').returns(credit_definition)
        intids.provides('getId').returns(10)
        component.getGlobalSiteManager().registerUtility(intids, IIntIds)
        add_intid(credit_definition)
        yesterday = datetime.utcnow() - timedelta(days=1)
        awarded_credit = AwardedCredit(title=u'Credit conference',
                                       description=u'desc',
                                       amount=42,
                                       credit_definition=credit_definition,
                                       issuer=u'my issuer',
                                       awarded_date=yesterday)

        ext_obj = to_external_object(awarded_credit)
        assert_that(ext_obj[CLASS], is_('AwardedCredit'))
        assert_that(ext_obj[MIMETYPE],
                    is_(AwardedCredit.mime_type))
        assert_that(ext_obj[CREATED_TIME], not_none())
        assert_that(ext_obj[LAST_MODIFIED], not_none())
        assert_that(ext_obj['amount'], is_(42))
        assert_that(ext_obj['title'], is_(u'Credit conference'))
        assert_that(ext_obj['description'], is_(u'desc'))
        assert_that(ext_obj['issuer'], is_(u'my issuer'))
        assert_that(ext_obj['awarded_date'], not_none())
        assert_that(ext_obj['credit_definition']['credit_type'], is_(u'Credit'))
        assert_that(ext_obj['credit_definition']['credit_units'], is_(u'Hours'))

        factory = find_factory_for(ext_obj)
        assert_that(factory, none())


class TestCreditDefinitionContainer(unittest.TestCase):

    layer = SharedConfiguringTestLayer

    def test_get_credit_definition_by(self):
        credit_definition = CreditDefinition(credit_type=u'School', credit_units=u'Points')
        assert_that(credit_definition.__parent__, is_(None))
        container = CreditDefinitionContainer()
        container.add_credit_definition(credit_definition)
        assert_that(credit_definition.__parent__, same_instance(container))
        assert_that(container, has_length(1))

        assert_that(container.get_credit_definition_by(credit_type=None, credit_units=None), is_(None))
        assert_that(container.get_credit_definition_by(credit_type=u'School', credit_units=None), is_(None))
        assert_that(container.get_credit_definition_by(credit_type=None, credit_units=u'Points'), is_(None))
        assert_that(container.get_credit_definition_by(credit_type=u'School', credit_units=u'Points'), same_instance(credit_definition))
        assert_that(container.get_credit_definition_by(credit_type=u'school', credit_units=u'points'), same_instance(credit_definition))
