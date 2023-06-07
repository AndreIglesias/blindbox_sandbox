import os
import unittest
import shutil
import yaml
from coverage import coverage
from unittest.mock import patch, MagicMock, ANY
from blindbox import requests
from blindbox.command import builder as bd

class TestBlindBox(unittest.TestCase):

    def test_azuresevbuilder_init_new_project(self):
        # Test the init_new_project method of AzureSEVBuilder
        azure_builder = bd.AzureSEVBuilder()
        test_folder = "test_folder"
        azure_builder.init_new_project(folder=test_folder)

        # Assert that the required files are created
        self.assertTrue(os.path.exists(test_folder + "/.gitignore"))
        self.assertTrue(os.path.exists(test_folder + "/blindbox.yml"))
        self.assertTrue(os.path.exists(test_folder + "/blindbox.tf"))
        shutil.rmtree(test_folder)

    '''def test_awsnitrobuilder_init_new_project(self):
        # Test the init_new_project method of AWSNitroBuilder
        aws_builder = bd.AWSNitroBuilder()
        test_folder = "test_folder"
        aws_builder.init_new_project(folder=test_folder)

        # Assert that the required files are created
        self.assertTrue(os.path.exists(test_folder + "/blindbox.yml"))
        self.assertTrue(os.path.exists(test_folder + "/blindbox.tf"))
        shutil.rmtree(test_folder)
    '''

    def test_yes_no_question_interactive_mode(self):
        builder = bd.BlindBoxBuilder()
        builder.interactive_mode = True

        with patch('inquirer.prompt', return_value={'answer': True}):
            result = builder.yes_no_question("Are you sure?")
            self.assertTrue(result)

    def test_yes_no_question_non_interactive_mode(self):
        builder = bd.BlindBoxBuilder()
        builder.interactive_mode = False

        result = builder.yes_no_question("Are you sure?")
        self.assertIsNone(result)

    def test_init_new_project(self):
        # Create a temporary folder for the test
        temp_folder = "temp_project"
        os.mkdir(temp_folder)

        try:
            b = bd.BlindBoxBuilder()
            b.init_new_project(temp_folder)

            self.assertTrue(os.path.exists(os.path.join(temp_folder, ".gitignore")))
            self.assertTrue(os.path.exists(os.path.join(temp_folder, "blindbox.yml")))
            self.assertTrue(os.path.exists(os.path.join(temp_folder, "blindbox.tf")))
        except NotImplementedError:
            print("Not implemented init new project")
        finally:
            # Clean up the temporary folder
            shutil.rmtree(temp_folder)

    def test_assert_tf_available(self):
        builder = bd.BlindBoxBuilder()
        builder.assert_tf_available()
        self.assertTrue(builder._tf_available)

    def test_assert_docker_available(self):
        builder = bd.BlindBoxBuilder()
        builder.assert_docker_available()
        self.assertTrue(builder._docker_available)

    '''
    @patch("blindbox.command.builder.subprocess")
    def test_tf_init_if_necessary(self, mock_subprocess):
        builder = bd.BlindBoxBuilder()
        builder.tf_init_if_necessary("tf_dir")
        mock_subprocess.run.assert_called_with(
            ["terraform", "init"], cwd="tf_dir"
        )
    '''

    def test_run_subprocess_capture_output(self):
        builder = bd.BlindBoxBuilder()
        command = ['echo', 'Hello, World!']

        result = builder.run_subprocess(command, return_stdout=True)

        self.assertEqual(result, b'Hello, World!\n')

    def test_save_project_settings(self):

        settings = bd.BlindBoxYml(platform='azure-sev')
        project_folder = 'tests'
        bd.BlindBoxBuilder.save_project_settings(settings, project_folder=project_folder)

        # Verify that the file has been created
        file_path = os.path.join(project_folder, 'blindbox.yml')
        self.assertTrue(os.path.exists(file_path))

        with open(file_path, 'r') as file:
            file_content = file.read()
        expected_content = yaml.safe_dump(settings.dict(), encoding='utf-8')
        self.assertEqual(file_content, expected_content.decode('utf-8'))

    def test_get_project_settings(self):
        builder = bd.BlindBoxBuilder()
        settings = bd.BlindBoxYml(platform='azure-sev')
        builder.save_project_settings(settings, project_folder='tests')

        builder.open = MagicMock(return_value='{"platform": "azure-sev"}')
        result = builder.get_project_settings(project_folder='tests')

        self.assertIsInstance(result, bd.BlindBoxYml)
        self.assertEqual(result.platform, 'azure-sev')

if __name__ == '__main__':
    unittest.main()
    command.builder.info("hola")
