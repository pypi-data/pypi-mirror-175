import datetime as dt
import json
import os
import textwrap
from io import StringIO
from unittest import TestCase, skipUnless

import pandas as pd
import requests
from htimeseries import HTimeseries

from enhydris_api_client import EnhydrisApiClient

from . import test_timeseries_hts


@skipUnless(
    os.getenv("ENHYDRIS_API_CLIENT_E2E_TEST"), "Set ENHYDRIS_API_CLIENT_E2E_TEST"
)
class EndToEndTestCase(TestCase):
    """End-to-end test against a real Enhydris instance.
    To execute this test, specify the ENHYDRIS_API_CLIENT_E2E_TEST environment variable
    like this:
        ENHYDRIS_API_CLIENT_E2E_TEST='
            {"base_url": "http://localhost:8001",
             "token": "topsecrettokenkey",
             "owner_id": 9,
             "variable_id": 22,
             "unit_of_measurement_id": 18
             }
        '
    This should point to an Enhydris server. Avoid using a production database for
    that; the testing functionality will write objects to the database. Although
    things are normally cleaned up (created objects will be deleted), id serial
    numbers will be affected and things might not be cleaned up if there is an error.
    """

    def setUp(self):
        v = json.loads(os.getenv("ENHYDRIS_API_CLIENT_E2E_TEST"))
        self.token = v["token"]
        self.client = EnhydrisApiClient(v["base_url"], token=self.token)
        self.client.__enter__()
        self.owner_id = v["owner_id"]
        self.variable_id = v["variable_id"]
        self.unit_of_measurement_id = v["unit_of_measurement_id"]

    def tearDown(self):
        self.client.__exit__()

    def test_e2e(self):
        # Verify we're authenticated
        token = self.client.session.headers.get("Authorization")
        self.assertEqual(token, f"token {self.token}")

        # Create a test station
        tmp_station_id = self.client.post_station(
            {
                "name": "My station",
                "copyright_holder": "Joe User",
                "copyright_years": "2019",
                "geom": "POINT(20.94565 39.12102)",
                "original_srid": 4326,
                "owner": self.owner_id,
                "display_timezone": "Etc/GMT-1",
            }
        )

        # Get the test station
        station = self.client.get_station(tmp_station_id)
        self.assertEqual(station["id"], tmp_station_id)
        self.assertEqual(station["name"], "My station")

        # Patch station and verify
        self.client.patch_station(tmp_station_id, {"name": "New name"})
        station = self.client.get_station(tmp_station_id)
        self.assertEqual(station["name"], "New name")

        # Put station and verify
        self.client.put_station(
            tmp_station_id,
            {
                "name": "Newer name",
                "copyright_holder": "Joe User",
                "copyright_years": "2019",
                "geom": "POINT(20.94565 39.12102)",
                "original_srid": 4326,
                "owner": self.owner_id,
            },
        )
        station = self.client.get_station(tmp_station_id)
        self.assertEqual(station["name"], "Newer name")

        # Create a time series group and verify it was created
        self.timeseries_group_id = self.client.post_timeseries_group(
            tmp_station_id,
            data={
                "name": "My time series group",
                "gentity": tmp_station_id,
                "variable": self.variable_id,
                "unit_of_measurement": self.unit_of_measurement_id,
                "precision": 2,
            },
        )
        timeseries_group = self.client.get_timeseries_group(
            tmp_station_id, self.timeseries_group_id
        )
        self.assertEqual(timeseries_group["name"], "My time series group")

        # Create a time series and verify it was created
        self.timeseries_id = self.client.post_timeseries(
            tmp_station_id,
            self.timeseries_group_id,
            data={
                "type": "Regularized",
                "time_step": "10min",
                "timeseries_group": self.timeseries_group_id,
            },
        )
        timeseries = self.client.get_timeseries(
            tmp_station_id, self.timeseries_group_id, self.timeseries_id
        )
        self.assertEqual(timeseries["type"], "Regularized")

        # Post time series data
        self.client.post_tsdata(
            tmp_station_id,
            self.timeseries_group_id,
            self.timeseries_id,
            test_timeseries_hts,
            default_timezone="Etc/GMT-2",
        )

        # Get the last date and check it
        date = self.client.get_ts_end_date(
            tmp_station_id, self.timeseries_group_id, self.timeseries_id
        )
        self.assertEqual(date, dt.datetime(2014, 1, 5, 7, 0))

        # Change display timezone
        self.client.patch_station(
            tmp_station_id, data={"display_timezone": "Etc/GMT-2"}
        )

        # Get the last date again and check it
        date = self.client.get_ts_end_date(
            tmp_station_id, self.timeseries_group_id, self.timeseries_id
        )
        self.assertEqual(date, dt.datetime(2014, 1, 5, 8, 0))

        # Get all time series data and check it
        hts = self.client.read_tsdata(
            tmp_station_id, self.timeseries_group_id, self.timeseries_id
        )
        pd.testing.assert_frame_equal(hts.data, test_timeseries_hts.data)

        # The other attributes should have been set too.
        self.assertTrue(hasattr(hts, "variable"))

        # Get part of the time series data and check it
        hts = self.client.read_tsdata(
            tmp_station_id,
            self.timeseries_group_id,
            self.timeseries_id,
            start_date=dt.datetime(2014, 1, 3, 8, 0),
            end_date=dt.datetime(2014, 1, 4, 8, 0),
        )
        expected_result = HTimeseries(
            StringIO(
                textwrap.dedent(
                    """\
                    2014-01-03 08:00,13.0,
                    2014-01-04 08:00,14.0,
                    """
                )
            )
        )
        pd.testing.assert_frame_equal(hts.data, expected_result.data)

        # Delete the time series and verify
        self.client.delete_timeseries(
            tmp_station_id, self.timeseries_group_id, self.timeseries_id
        )
        with self.assertRaises(requests.HTTPError):
            self.client.get_timeseries(
                tmp_station_id, self.timeseries_group_id, self.timeseries_id
            )

        # Delete station
        self.client.delete_station(tmp_station_id)
        with self.assertRaises(requests.HTTPError):
            self.client.get_station(tmp_station_id)
