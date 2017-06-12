# -*- coding: utf-8 -*-
"""
All available parsers, that convert raw representation could be received from
any external source, are and should be kept here.
"""
import ujson as json

from .rules import Rule, ProjectRule


class RuleParsingException(Exception):
    """
    Basic exception for all types of rule parsing errors
    """
    pass


class RuleParser:
    """
    Just a stub in case if we want to extend parsing sources.
    """
    pass


class JsonRuleParser(RuleParser):
    """
    Basic JSON parser.
    """

    @staticmethod
    def parse(json_string: str) -> Rule:
        """
        Actually perform parsing from JSON-encoded string to an actual rule.

        :param json_string: JSON dict with all the data about the achievement.
        :type json_string: str

        :returns: Fully parsed rule object.
        :rtype: Rule

        :exception: RuleParsingException
        """
        try:
            parsee = json.loads(json_string)
            # don't copy objects having same JSON but differently formatted
            hash_id = hash(json.dumps(parsee))
            rule = Rule(id=hash_id,
                        badge=parsee['badge'],
                        name=parsee['name'],
                        description=parsee['description'],
                        bonus=int(parsee['bonus']),
                        tasks_number=int(parsee['tasks_number']),
                        days_number=(parsee['days_number']),
                        is_weekend=bool(parsee['is_weekend']),
                        is_adjacent=bool(parsee['is_adjacent']))

            if 'task_type' not in parsee:
                return rule
            else:
                return ProjectRule.from_rule(rule,
                                             parsee['task_type'])
        except ValueError:
            raise RuleParsingException('Can not parse {}'.format(json_string))
        except KeyError as e:
            raise RuleParsingException('Invalid JSON passed: {}'.format(e))
