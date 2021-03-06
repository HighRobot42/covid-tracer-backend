# Copyright 2020 Raphael Javaux
#
# This file is part of CovidTracer.
#
# CovidTracer is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# CovidTracer is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with CovidTracer. If not, see<https://www.gnu.org/licenses/>.

import datetime

from sqlalchemy.schema import Index

from app import db, DAILY_KEY_SIZE

class DailyKey(db.Model):
    __tablename__ = 'daily_keys'

    date = db.Column(db.Date(), nullable=False, primary_key=True)

    # Stores the key as an hexadecimal string.
    key = db.Column(db.String(length=DAILY_KEY_SIZE * 2), primary_key=True, index=True)

    created_at = db.Column(
        db.DateTime(), nullable=False, index=True, default=datetime.datetime.utcnow
    )

    is_tested = db.Column(db.Boolean(), nullable=False) # Has it been tested against Covid-19?

class Request(db.Model):
    """Stores information, mostly for rate limiting purposes."""

    # Note:
    # Use a different table from `Case` so that IP addresses are not associated with the case
    # report.

    __tablename__ = 'requests'

    id = db.Column(db.Integer, primary_key=True)

    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.datetime.utcnow)

    # Information about the notifying device.
    remote_addr = db.Column(db.String, nullable=False)
    user_agent = db.Column(db.String, nullable=True)

    comment = db.Column(db.String(1000))

Index('idx_requests', Request.remote_addr, Request.created_at)
