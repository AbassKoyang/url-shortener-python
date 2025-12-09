import unittest;
import app;

VALID_URL = 'https://www.amazon.com/s/?_encoding=UTF8&k=fashion&pd_rd_w=yn28b&content-id=amzn1.sym.8a64fefa-e450-4bbe-83a4-970ea696b46d&pf_rd_p=8a64fefa-e450-4bbe-83a4-970ea696b46d&pf_rd_r=MVAF7TWRETBKS9NBMNJS&pd_rd_wg=mXilr&pd_rd_r=0a595438-7c7a-410c-81c4-64adcf16071e&ref_=pd_hp_d_btf_unk';
INVALID_URL = "kjbhgvhbjklnmlkbkvcghghmnjbvv";

class TestUrlShortener(unittest.TestCase):
    def test_validate_url_format_invalid(self):
        self.assertFalse(app.validate_url_format(url=INVALID_URL));
    def test_validate_url_format_valid(self):
        self.assertTrue(app.validate_url_format(url=VALID_URL));
    def test_validate_url_invalid(self):
        self.assertFalse(app.validate_url(url=INVALID_URL));
    def test_validate_url_valid(self):
        self.assertTrue(app.validate_url(url=VALID_URL));

if __name__ == '__main__':
    unittest.main();