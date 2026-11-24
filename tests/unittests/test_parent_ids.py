import unittest

from tap_bing_ads import PARENT_ID_FIELDS, add_parent_id, with_parent_id


class TestParentIds(unittest.TestCase):
    """AdGroup and Ad records get the id of the parent they were fetched for."""

    def test_schema_gets_parent_id_without_touching_the_original(self):
        original = {'type': 'object', 'properties': {'Id': {'type': ['null', 'integer']}}}
        for obj, field in PARENT_ID_FIELDS.items():
            schema = with_parent_id(original, obj)
            self.assertEqual(schema['properties'][field], {'type': ['null', 'integer']})
            self.assertNotIn(field, original['properties'])

    def test_records_get_parent_id(self):
        records = add_parent_id([{'Id': 1}, {'Id': 2}], 'CampaignId', 42)
        self.assertEqual([r['CampaignId'] for r in records], [42, 42])

    def test_ad_groups_and_ads_map_to_their_parents(self):
        self.assertEqual(PARENT_ID_FIELDS, {'AdGroup': 'CampaignId', 'Ad': 'AdGroupId'})


if __name__ == '__main__':
    unittest.main()
