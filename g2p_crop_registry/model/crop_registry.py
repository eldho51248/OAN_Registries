from odoo import api, fields, models


class G2PCrop(models.Model):
    _name = 'g2p.crop.registry'
    _description = 'G2p Crop Registry'


    zone_name = fields.Char(string="Zone Name")
    woreda_name = fields.Char(string="Woreda Name")
    kebele_name = fields.Char(string="Kebele Name")
    kebele_code = fields.Char(string="Kebele Code")
    land_id = fields.Char(string="Land ID")
    land_area = fields.Char(string="Land Area")
    owner_name = fields.Char(string="Owner Name")
    ownership_type = fields.Char(string="Ownership Type")
    land_certificate = fields.Char(string="Land Certificate")
    soil_fertility = fields.Char(string="Soil Fertility")
    current_land_use = fields.Char(string="Current Land Use")
    crop_name = fields.Char(string="Crop Name")
    crop_verity = fields.Char(string="Crop Verity")
    crop_area = fields.Char(string="Crop Area")
    crop_season = fields.Char(string="Crop Season")
    crop_produce_min = fields.Char(string="Crop Produce Min")
    crop_produce_max = fields.Char(string="Crop Produce Max")
    crop_wholesale_min = fields.Char(string="Crop Wholesale Min")
    crop_wholesale_max = fields.Char(string="Crop Wholesale Max")
    crop_retail_min = fields.Char(string="Crop Retail Min")
    crop_retail_max = fields.Char(string="Crop Retail Max")
    crop_volume = fields.Char(string="Crop Volume")
    live_stock_type = fields.Char(string="Live Stock Type")
    live_stock_number = fields.Char(string="Live Stock Number")
    live_strock_water_source = fields.Char(string="Live Strock Water Source")
    cultivation_land = fields.Char(string="Cultivation Land")
    cultivation_area = fields.Char(string="Cultivation Area")
    cultivation_crop_name = fields.Char(string="Cultivation Crop Name")
    sown_land = fields.Char(string="Sown Land")
    sown_area = fields.Char(string="Sown Area")
    sown_crop_name = fields.Char(string="Sown Crop Name")
    harvested_land = fields.Char(string="Harvested Land")
    harvested_area = fields.Char(string="Harvested Area")
    harvested_crop_name = fields.Char(string="Harvested Crop Name")
    irrigation_type = fields.Char(string="Irrigation Type")
    surveyor_name = fields.Char(string="Surveyor Name")
    surveyor_fullname = fields.Char(string="Surveyor Full Name")
    surveyor_mobile_number = fields.Char(string="Surveyor Mobile Number")
    supervisor_name = fields.Char(string="Supervisor Name")
    supervisor_fullname = fields.Char(string="Supervisor Full Name")
    supervisor_mobile_number = fields.Char(string="Supervisor Mobile Number")
    first_approvel_status = fields.Char(string="First Approvel Status")
    second_approvel_status = fields.Char(string="Second Approvel Status")
    verifier_name = fields.Char(string="Verifier Name")
    verifier_mobile_number = fields.Char(string="Verifier Mobile Number")




