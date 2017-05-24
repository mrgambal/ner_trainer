# -*- coding: utf-8 -*-
"""Module contains all models directly related to the main entity - tasks."""

from flask_mongoengine import Document
from mongoengine import (
    BooleanField,
    CASCADE,
    DateTimeField,
    DictField,
    IntField,
    ListField,
    ReferenceField,
    StringField
)

from vulyk.models.user import User


class Batch(Document):
    """
    Helper category to group tasks.
    """
    id = StringField(max_length=50, primary_key=True)
    task_type = StringField(max_length=50, required=True, db_field='taskType')
    tasks_count = IntField(default=0, required=True, db_field='tasksCount')
    tasks_processed = IntField(default=0, db_field='tasksProcessed')

    meta = {
        'collection': 'batches',
        'allow_inheritance': True,
        'indexes': [
            'task_type'
        ]
    }

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return 'Batch [{id}] ({processed}/{count})'.format(
            id=self.id,
            processed=self.tasks_processed,
            count=self.tasks_count)


class AbstractTask(Document):
    """
    This is AbstractTask model.
    You need to inherit it in your model
    """
    id = StringField(max_length=200, default='', primary_key=True)
    task_type = StringField(max_length=50, required=True, db_field='taskType')
    batch = ReferenceField(Batch, reverse_delete_rule=CASCADE)

    users_count = IntField(default=0, db_field='usersCount')
    users_processed = ListField(ReferenceField(User),
                                db_field='usersProcessed')
    users_skipped = ListField(ReferenceField(User), db_field='usersSkipped')

    closed = BooleanField(default=False)
    task_data = DictField(required=True)

    meta = {
        'collection': 'tasks',
        'allow_inheritance': True,
        'indexes': [
            'task_type',
            'batch'
        ]
    }

    def as_dict(self):
        """
        Converts the model-instance into a safe and lightweight dictionary.

        :rtype: dict
        """
        return {
            'id': self.id,
            'closed': self.closed,
            'data': self.task_data
        }

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        str(self)


class AbstractAnswer(Document):
    """
    This is AbstractTask model.
    You need to inherit it in your model
    """
    task = ReferenceField(AbstractTask, reverse_delete_rule=CASCADE)
    created_by = ReferenceField(User, reverse_delete_rule=CASCADE,
                                db_field='createdBy')
    created_at = DateTimeField(db_field='createdAt')
    task_type = StringField(max_length=50, required=True, db_field='taskType')
    # not sure - could be extended
    result = DictField()

    meta = {
        'collection': 'reports',
        'allow_inheritance': True,
        'indexes': [
            'task',
            'created_by',
            'created_at',
            {
                'fields': ['created_by', 'task'],
                'unique': True
            }
        ]
    }

    # TODO: decide, if we need it at all
    @property
    def corrections(self):
        """
        Returns whole amount of actions/corrections given by user in this
        particular answer.

        :return: Count of corrections in this answer
        :rtype: int
        """
        return 1

    @corrections.setter
    def corrections(self, value):
        pass

    @corrections.deleter
    def corrections(self):
        pass

    def as_dict(self):
        """
        Converts the model-instance into a safe that will include also task
        and user.

        :rtype: dict
        """
        return {
            'task': self.task.as_dict(),
            'answer': self.result,
            'user': self.created_by.as_dict()
        }

    def __str__(self):
        return str(self.pk)

    def __repr__(self):
        return 'Report [{} by {}]'.format(self.created_by, self.task)
