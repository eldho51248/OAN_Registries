from odoo.exceptions import UserError, ValidationError
from odoo.tests.common import TransactionCase


class TestG2PFarmer(TransactionCase):
    def setUp(self):
        super().setUp()

        self.FarmerModel = self.env["g2p.farmer"]
        self.RegionModel = self.env["g2p.region"]
        self.ZoneModel = self.env["g2p.zone"]
        self.WoredaModel = self.env["g2p.woreda"]
        self.KebeleModel = self.env["g2p.kebele"]

        # Setup test data
        self.test_region = self.RegionModel.create({"name": "Test Region", "code": "TR"})
        self.test_zone = self.ZoneModel.create(
            {"name": "Test Zone", "region": self.test_region.id, "code": "TZ"}
        )
        self.test_woreda = self.WoredaModel.create(
            {"name": "Test Woreda", "zone": self.test_zone.id, "code": "TW"}
        )
        self.test_kebele = self.KebeleModel.create(
            {"name": "Test Kebele", "woreda": self.test_woreda.id, "code": "TK"}
        )

    def test_01_create_farmer_profile(self):
        """Test creating a farmer profile."""
        farmer_data = {
            "given_name": "John",
            "family_name": "Doe",
            "regionn": self.test_region.id,
            "zone": self.test_zone.id,
            "woreda": self.test_woreda.id,
            "kebele": self.test_kebele.id,
            "birthdate": "1990-01-01",
            "has_personal_phone": "yes",
            "is_farmer": "yes",
            "education": "basic",
            "state": "draft",
        }
        farmer = self.FarmerModel.create(farmer_data)

        # Check if the farmer profile was created successfully
        self.assertEqual(farmer.given_name, "John", "Farmer's given name is incorrect")
        self.assertEqual(farmer.family_name, "Doe", "Farmer's family name is incorrect")
        self.assertEqual(farmer.regionn.id, self.test_region.id, "Farmer's region is incorrect")

    def test_02_update_farmer_profile(self):
        """Test updating a farmer profile."""
        farmer_data = {
            "given_name": "Jane",
            "family_name": "Doe",
            "regionn": self.test_region.id,
            "zone": self.test_zone.id,
            "woreda": self.test_woreda.id,
            "kebele": self.test_kebele.id,
            "birthdate": "1995-01-01",
            "has_personal_phone": "no",
            "is_farmer": "yes",
            "education": "intermediary",
            "state": "approved",
        }
        farmer = self.FarmerModel.create(farmer_data)

        # Update the farmer profile
        farmer.write({"given_name": "Updated Name"})

        # Check if the update was successful
        self.assertEqual(
            farmer.given_name, "Updated Name", "Farmer's given name was not updated successfully"
        )

    def test_03_compute_age_int(self):
        """Test computed age_int field."""
        farmer_data = {
            "given_name": "John",
            "family_name": "Doe",
            "regionn": self.test_region.id,
            "zone": self.test_zone.id,
            "woreda": self.test_woreda.id,
            "kebele": self.test_kebele.id,
            "birthdate": "1990-01-01",
            "has_personal_phone": "yes",
            "is_farmer": "yes",
            "education": "basic",
            "state": "draft",
        }
        farmer = self.FarmerModel.create(farmer_data)

        # Check computed age_int field
        self.assertEqual(farmer.age_int, "34", "Computed age_int field is incorrect")

    def test_04_validation_error_on_create(self):
        """Test validation error when creating a farmer without phone numbers."""
        farmer_data = {
            "given_name": "John",
            "family_name": "Doe",
            "regionn": self.test_region.id,
            "zone": self.test_zone.id,
            "woreda": self.test_woreda.id,
            "kebele": self.test_kebele.id,
            "birthdate": "1990-01-01",
            "has_personal_phone": "no",
            "is_farmer": "yes",
            "education": "basic",
            "state": "draft",
            "phone_number_ids": False,  # Trigger validation error
        }

        with self.assertRaises(ValidationError):
            self.FarmerModel.create(farmer_data)

    def test_05_check_user_group_permission(self):
        """Test user group permission."""
        farmer = self.FarmerModel.create({"given_name": "John"})

        # Simulate a user who does not belong to the required group
        self.env.user = self.env["res.users"].browse(self.env.uid)
        self.env.user.groups_id = [(3, self.env.ref("g2p_ati.group_data_enumerator").id)]

        # Attempt to edit the record
        with self.assertRaises(UserError):
            farmer.write({"given_name": "Updated Name"})
