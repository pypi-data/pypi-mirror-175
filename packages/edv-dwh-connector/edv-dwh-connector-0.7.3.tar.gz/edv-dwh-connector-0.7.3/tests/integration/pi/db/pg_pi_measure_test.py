"""
Test case for PI tag measures.
.. since: 0.2
"""

# -*- coding: utf-8 -*-
# Copyright (c) 2022 Endeavour Mining
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to read
# the Software only. Permissions is hereby NOT GRANTED to use, copy, modify,
# merge, publish, distribute, sublicense, and/or sell copies of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
from datetime import datetime

import sqlalchemy  # type: ignore
from hamcrest import assert_that, equal_to, calling, raises

from edv_dwh_connector.exceptions import ValueAlreadyExistsError
from edv_dwh_connector.pi.db.pg_pi_tag import PgPITags
from edv_dwh_connector.pi.db.pg_pi_measure import PgPIMeasures
from tests.adapted_postgresql import AdaptedPostreSQL, \
    PgDwhForTests


def test_save_new_measure() -> None:
    """
    Tests that it saves new measure.
    """

    with AdaptedPostreSQL() as postgres:
        dwh = PgDwhForTests(
            sqlalchemy.create_engine(postgres.get_connection_url())
        )
        tag_code = "AI162003_SCLD"
        date = datetime(
            year=2022, month=1, day=15,
            hour=12, minute=55, second=30, microsecond=177990
        )
        measure = PgPIMeasures(
            PgPITags(dwh).get(tag_code), dwh
        ).add(date=date, value=35.71)
        assert_that(
            measure.tag().code(), equal_to(tag_code),
            "Measure PI Tag should match"
        )
        assert_that(
            measure.date(), equal_to(
                datetime.strptime(
                    date.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
                    "%Y-%m-%d %H:%M:%S.%f"
                )
            ),
            "PI Tag measure date should match"
        )
        assert_that(
            measure.value(), equal_to(35.71),
            "PI Tag measure value should match"
        )


def test_try_to_add_existent_measure() -> None:
    """
    Try to add an existent measure for a tag.
    """

    with AdaptedPostreSQL() as postgres:
        dwh = PgDwhForTests(
            sqlalchemy.create_engine(postgres.get_connection_url())
        )
        tag_code = "AI162003_SCLD"
        date = datetime(
            year=2022, month=1, day=15,
            hour=12, minute=55, second=30, microsecond=177990
        )
        measures = PgPIMeasures(
            PgPITags(dwh).get(tag_code), dwh
        )
        measures.add(date=date, value=35.71)
        assert_that(
            calling(measures.add).with_args(
                date, 12.0
            ),
            raises(
                ValueAlreadyExistsError,
                f"A measure already exists at {date} for tag {tag_code}"
            ),
            "Tag existent measure adding should be rejected"
        )


def test_list_items() -> None:
    """
    Tests that it lists items.
    """

    with AdaptedPostreSQL() as postgres:
        tag_code = "AI162003_SCLD"
        date = datetime(
            year=2022, month=1, day=19,
            hour=15, minute=7, second=12, microsecond=177990
        )
        dwh = PgDwhForTests(
            sqlalchemy.create_engine(postgres.get_connection_url())
        )
        measures = PgPIMeasures(
            PgPITags(dwh).get(tag_code), dwh
        )
        measures.add(date=date, value=35.71)
        assert_that(
            len(measures.items(date, date)), equal_to(1),
            "Measures of PI Tag should be retrieved"
        )
        assert_that(
            len(measures.items(date.now(), date.now())), equal_to(0),
            "Measures of PI Tag should be empty"
        )
