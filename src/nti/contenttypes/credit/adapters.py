#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from BTrees.OOBTree import OOBTree
from BTrees.OOBTree import OOTreeSet

from ZODB.interfaces import IConnection

from zope import component
from zope import interface

from zope.annotation import factory as an_factory

from zope.security.interfaces import IPrincipal

from nti.dublincore.time_mixins import PersistentCreatedAndModifiedTimeObject

from nti.containers.containers import CaseInsensitiveCheckingLastModifiedBTreeContainer

from nti.contenttypes.credit.interfaces import ICompletedItem
from nti.contenttypes.credit.interfaces import ISuccessAdapter
from nti.contenttypes.credit.interfaces import IItemNTIIDAdapter
from nti.contenttypes.credit.interfaces import IPrincipalAdapter
from nti.contenttypes.credit.interfaces import ICompletionContext

from nti.schema.fieldproperty import createDirectFieldProperties

from nti.schema.schema import SchemaConfigured

from nti.wref.interfaces import IWeakRef

COMPLETED_ITEM_ANNOTATION_KEY = 'nti.contenttypes.completion.interfaces.ICompletedItemContainer'
COMPLETABLE_ITEM_ANNOTATION_KEY = 'nti.contenttypes.completion.interfaces.ICompletableItemContainer'
COMPLETABLE_ITEM_DEFAULT_REQUIRED_ANNOTATION_KEY = 'nti.contenttypes.completion.interfaces.ICompletableItemDefaultRequiredPolicy'
COMPLETION_CONTAINER_ANNOTATION_KEY = 'nti.contenttypes.completion.interfaces.ICompletionContextCompletionPolicyContainer'

logger = __import__('logging').getLogger(__name__)


@component.adapter(ICompletionContext)
@interface.implementer(ICompletedItemContainer)
class CompletedItemContainer(CaseInsensitiveCheckingLastModifiedBTreeContainer,
                             SchemaConfigured):
