import os
import unittest
import blindbox
from coverage import coverage

class TestBlindBox(unittest.TestCase):

    def setUp(self):
        self.cov = coverage()
        self.cov.start()

        import blindbox

    def tearDown(self):
        self.cov.stop()
        self.cov.save()
        self.cov.report()
        self.cov.erase()

    def test_main(self):
        # Test the main function
        with self.assertRaises(SystemExit):
            blindbox.main()

    def test_azuresevbuilder_init_new_project(self):
        # Test the init_new_project method of AzureSEVBuilder
        builder = blindbox.AzureSEVBuilder()
        builder.init_new_project(folder="test_folder")

        # Assert that the required files are created
        self.assertTrue(os.path.exists("test_folder/.gitignore"))
        self.assertTrue(os.path.exists("test_folder/blindbox.yml"))
        self.assertTrue(os.path.exists("test_folder/blindbox.tf"))

    def test_awsnitrobuilder_init_new_project(self):
        # Test the init_new_project method of AWSNitroBuilder
        builder = blindbox.AWSNitroBuilder()
        builder.init_new_project(folder="test_folder")

        # Assert that the required files are created
        self.assertTrue(os.path.exists("test_folder/blindbox.yml"))
        self.assertTrue(os.path.exists("test_folder/blindbox.tf"))

    # Add more test cases for other methods and functionalities

if __name__ == "__main__":
    unittest.main()
