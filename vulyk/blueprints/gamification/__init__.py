# -*- coding: utf-8 -*-
"""
The core of gamification sub-project.
"""
import flask
from flask import Blueprint, Response, send_file

from vulyk import utils
from vulyk.models.user import User
from vulyk.blueprints.gamification.models.foundations import (
    FundModel, FundFilterBy)

from . import listeners
from .models.events import EventModel

gamification = Blueprint('gamification', __name__)


@gamification.route('/funds', methods=['GET'])
@gamification.route('/funds/<string:category>', methods=['GET'])
def funds(category: str = None) -> Response:
    """
    The list of foundations we donate to or those, that backed us.
    May be filtered using `category` parameter that currently takes two values
    `donatable` and `nondonatable`. If a full list is needed – parameter must
    be omitted.

    :param category: Filter list
    :type category: str

    :return: Funds list filtered by category (if passed).
    :rtype: Response
    """
    filtering = FundFilterBy.NO_FILTER

    if category is not None:
        if category == 'donatable':
            filtering = FundFilterBy.DONATABLE
        elif category == 'nondonatable':
            filtering = FundFilterBy.NON_DONATABLE
        else:
            flask.abort(utils.HTTPStatus.NOT_FOUND)

    return utils.json_response({'funds': list(FundModel.get_funds(filtering))})


@gamification.route('/funds/<string:fund_id>/logo', methods=['GET'])
def fund_logo(fund_id: str) -> Response:
    """
    Simple controller that will return you a logotype of the fund if it exists
    in the DB by fund's ID.
    To fulfill mimetype we use that fact that ImageGridFSProxy relies on
    Pillow's Image class that recognises correct mimetype for images. Thus the
    proxy has a field named `format`, which contain an uppercase name of
    the type. E.g.: 'JPEG'.

    :param fund_id: Current fund ID
    :type fund_id: str

    :return: An response with a file or 404 if fund is not found
    :rtype: Response
    """
    fund = FundModel.find_by_id(fund_id)

    if fund is None:
        flask.abort(utils.HTTPStatus.NOT_FOUND)

    return send_file(fund.logo,
                     mimetype='image/{}'.format(fund.logo.format.lower()),
                     cache_timeout=360000)


@gamification.route('/events', methods=['GET'])
def unseen_events() -> Response:
    """
    The list of yet unseen events we return for currently logged in user.

    :return: Events list (may be empty) or Forbidden if not authorized.
    :rtype: Response
    """
    user = flask.g.user

    if isinstance(user, User):
        return utils.json_response({
            'events': EventModel.get_unread_events(flask.g.user)})
    else:
        flask.abort(utils.HTTPStatus.FORBIDDEN)
