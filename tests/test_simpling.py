import unittest
from sdr_utils.sampling import generate_samples

class TestSampling(unittest.TestCase):
    def setUp(self):
        self.trait_definitions = [
            {"name": "Hat", "values": ["Alpine Hat", "Ascot Cap", "Aviator Hat"]},
            {"name": "Eyes", "values": ["Has Angelic eyes", "Has Bewitching eyes", "Has Bold eyes"]},
            {"name": "Mouth", "values": ["Angelic Savor", "Belching", "Blissful Munch "]},
            {"name": "Clothes", "values": ["Anime School Uniform", "Bandolier", "Baseball Tee"]},
            {"name": "Pet", "values": ["Alpaca Cria", "Baby Albatross", "Baby Albino Peacock"]},
            {"name": "Necklace", "values": ["Beaded Necklace", "Bib Necklace", "Butterfly necklace"]}
        ]

    def test_generate_samples(self):
        samples = generate_samples(self.trait_definitions)
        self.assertEqual(len(samples), 60)  # 10 samples for each trait definition
        print(samples)
        # Check that each sample is a dictionary with keys matching the trait names
        # for sample in samples:
        #     self.assertTrue(all(key in sample for key in [trait['name'] for trait in self.trait_definitions]))

if __name__ == '__main__':
    unittest.main()
