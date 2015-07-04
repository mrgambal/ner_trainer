#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_task_types
"""
import unittest

from mock import patch, Mock

from vulyk.models.tasks import AbstractTask, AbstractAnswer
from vulyk.models.task_types import AbstractTaskType
from .base import (
    _collection,
    BaseTest,
    mocked_get_connection,
)


class TestTaskTypes(BaseTest):
    def test_init_task_inheritance(self):
        class NoTask(AbstractTaskType):
            task_model = Mock

        self.assertRaises(AssertionError, lambda: NoTask({}))

    def test_init_answer_inheritance(self):
        class NoAnswer(AbstractTaskType):
            task_model = AbstractTask
            answer_model = Mock

        self.assertRaises(AssertionError, lambda: NoAnswer({}))

    def test_init_type_name(self):
        class NoTypeName(AbstractTaskType):
            task_model = AbstractTask
            answer_model = AbstractAnswer

        self.assertRaises(AssertionError, lambda: NoTypeName({}))

    def test_init_template_name(self):
        class NoTemplateName(AbstractTaskType):
            task_model = AbstractTask
            answer_model = AbstractAnswer
            type_name = 'FakeTaskType'

        self.assertRaises(AssertionError, lambda: NoTemplateName({}))

    @patch('mongoengine.connection.get_connection', mocked_get_connection)
    @patch('mongoengine.queryset.base.BaseQuerySet.count', lambda *a: 22)
    def test_to_dict(self):
        got = {
            'name': 'Fake name',
            'description': 'Fake description',
            'type': 'FakeTaskType',
            'tasks': 22
        }

        class FakeModel(AbstractTask):
            pass

        class ToDict(AbstractTaskType):
            task_model = FakeModel
            answer_model = AbstractAnswer
            type_name = 'FakeTaskType'
            template = 'tmpl.html'

            _name = 'Fake name'
            _description = 'Fake description'

        self.assertDictEqual(ToDict({}).to_dict(), got)


if __name__ == '__main__':
    unittest.main()
