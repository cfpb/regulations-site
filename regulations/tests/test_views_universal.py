from datetime import datetime, timedelta
import random

from unittest import TestCase
from mock import patch

from regulations.views import universal_landing as universal


class UniversalLandingTest(TestCase):
    """ Tests for the view that drives the main (universal) landing page. """

    def test_filter_future_amendments(self):
        versions = []
        futures = []

        today = datetime.today()
        for i in xrange(1, 5):
            future_date = today + timedelta(days=i)
            v = {'by_date': future_date}
            versions.append(v)
            futures.append(v)

        for i in xrange(1, 3):
            past_date = today - timedelta(days=i)
            versions.append({'by_date': past_date})

        random.shuffle(versions)

        self.assertEqual(len(versions), 6)
        filtered = universal.filter_future_amendments(versions)
        self.assertEqual(len(filtered), 4)
        self.assertEqual(futures, filtered)
