import os
import shutil
import unittest
from unittest.mock import patch
from core.project_generator import get_project_name, generate_go_project_structure

class TestProjectGenerator(unittest.TestCase):
    def setUp(self):
        self.test_project_name = "test_project"
        self.test_dir = os.path.join(os.getcwd(), self.test_project_name)

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    @patch('builtins.input', return_value=test_project_name)
    def test_get_project_name(self, mock_input):
        project_name = get_project_name()
        self.assertEqual(project_name, self.test_project_name)

    def test_generate_go_project_structure(self):
        generate_go_project_structure(self.test_project_name)
        expected_dirs = [
            self.test_project_name,
            os.path.join(self.test_project_name, "cmd"),
            os.path.join(self.test_project_name, "internal"),
            os.path.join(self.test_project_name, "internal", "entity"),
            os.path.join(self.test_project_name, "internal", "usecase"),
            os.path.join(self.test_project_name, "internal", "repository"),
            os.path.join(self.test_project_name, "internal", "handler"),
        ]
        for dir_path in expected_dirs:
            self.assertTrue(os.path.exists(dir_path))


if __name__ == "__main__":
    unittest.main()