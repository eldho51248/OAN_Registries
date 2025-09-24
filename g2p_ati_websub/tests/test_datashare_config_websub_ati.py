# Part of OpenG2P. See LICENSE file for full copyright and licensing details.
from odoo.tests.common import TransactionCase
from unittest.mock import patch


class TestG2PDatashareConfigWebsubATI(TransactionCase):
    """Test cases for ATI WebSub integration"""

    def setUp(self):
        super().setUp()
        self.websub_config_model = self.env["g2p.datashare.config.websub"]
        
        # Create test partner with ATI fields
        self.test_partner = self.env["res.partner"].create({
            "name": "Test Farmer",
            "is_registrant": True,
            "is_individual": True,
            "given_name": "John",
            "family_name": "Doe",
            "is_farmer": "yes",
            "farming_type": "mixed_farming",
        })

    def test_ati_data_extraction(self):
        """Test that ATI farmer data is extracted correctly"""
        websub_config = self.websub_config_model.create({
            "name": "Test ATI WebSub Config",
            "event_type": "WEBSUB_INDIVIDUAL_CREATED",
            "partner_id": "test_partner",
        })

        # Test data extraction
        ati_data = websub_config._get_ati_farmer_data({"id": self.test_partner.id})
        
        # Verify ATI data is extracted
        self.assertIn("given_name", ati_data)
        self.assertIn("family_name", ati_data)
        self.assertIn("is_farmer", ati_data)
        self.assertIn("farming_type", ati_data)
        
        self.assertEqual(ati_data["given_name"], "John")
        self.assertEqual(ati_data["family_name"], "Doe")
        self.assertEqual(ati_data["is_farmer"], "yes")
        self.assertEqual(ati_data["farming_type"], "mixed_farming")

    def test_ati_data_in_payload(self):
        """Test that ATI data is included in the WebSub payload"""
        websub_config = self.websub_config_model.create({
            "name": "Test ATI WebSub Config",
            "event_type": "WEBSUB_INDIVIDUAL_CREATED",
            "partner_id": "test_partner",
        })

        # Mock the parent publish method
        with patch.object(websub_config.__class__, 'publish_event_websub') as mock_publish:
            mock_publish.return_value = True
            
            # Call the publish method
            websub_config.publish_event_websub({"id": self.test_partner.id})
            
            # Verify the parent method was called with enhanced data
            mock_publish.assert_called_once()
            call_args = mock_publish.call_args[0][0]
            
            # Check that ATI data was added
            self.assertIn("ati_farmer_data", call_args)
            ati_data = call_args["ati_farmer_data"]
            
            self.assertEqual(ati_data["given_name"], "John")
            self.assertEqual(ati_data["family_name"], "Doe")
            self.assertEqual(ati_data["is_farmer"], "yes")
            self.assertEqual(ati_data["farming_type"], "mixed_farming")

    def test_no_ati_data_for_non_farmer(self):
        """Test that no ATI data is extracted for non-farmer partners"""
        non_farmer = self.env["res.partner"].create({
            "name": "Non Farmer",
            "is_registrant": True,
            "is_individual": True,
            "is_farmer": "no",
        })

        websub_config = self.websub_config_model.create({
            "name": "Test ATI WebSub Config",
            "event_type": "WEBSUB_INDIVIDUAL_CREATED",
            "partner_id": "test_partner",
        })

        # Test data extraction for non-farmer
        ati_data = websub_config._get_ati_farmer_data({"id": non_farmer.id})
        
        # Should still extract basic ATI fields but with limited data
        self.assertIn("is_farmer", ati_data)
        self.assertEqual(ati_data["is_farmer"], "no")
        # Other ATI fields should not be present for non-farmers
        self.assertNotIn("farming_type", ati_data)

    def test_empty_data_handling(self):
        """Test handling of empty or invalid data"""
        websub_config = self.websub_config_model.create({
            "name": "Test ATI WebSub Config",
            "event_type": "WEBSUB_INDIVIDUAL_CREATED",
            "partner_id": "test_partner",
        })

        # Test with empty data
        ati_data = websub_config._get_ati_farmer_data({})
        self.assertEqual(ati_data, {})
        
        # Test with invalid ID
        ati_data = websub_config._get_ati_farmer_data({"id": 99999})
        self.assertEqual(ati_data, {})
