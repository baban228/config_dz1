import os
import tempfile
import unittest
import xml.etree.ElementTree as ET
import zipfile
from unittest.mock import mock_open, patch

from shell_emulator import ShellEmulator


class TestShellEmulator(unittest.TestCase):
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="""
    [user]
    name = "test_user"
    computer = "test_computer"
    parametr = "test_param"

    [paths]
    vfs = "system.zip"
    log = "config.xml"
    start_script = "start.sh"
    """,
    )
    def setUp(self, mock_open):
        # Create a temp directory to mock file creation
        self.test_dir = tempfile.TemporaryDirectory()
        self.config_path = os.path.join(self.test_dir.name, "config.toml")
        with open(self.config_path, "w") as f:
            f.write("""
            [user]
            name = "test_user"
            computer = "test_computer"
            parametr = "test_param"

            [paths]
            vfs = "test.zip"
            log = "test_log.xml"
            start_script = "start.sh"
            """)

        # Mock zip file creation
        self.zip_path = os.path.join(self.test_dir.name, "test.zip")
        with zipfile.ZipFile(self.zip_path, "w") as zipf:
            zipf.writestr("folder/file1.txt", "This is a test file")
            zipf.writestr("file2.txt", "Another file")

        # Create a dummy start script
        self.start_script_path = os.path.join(self.test_dir.name, "start.sh")
        with open(self.start_script_path, "w") as f:
            f.write("echo 'Running start script'\n")

        # Set up the paths in the mock configuration
        self.config = {
            "user": {
                "name": "test_user",
                "computer": "test_computer",
                "parametr": "test_param",
            },
            "paths": {
                "vfs": self.zip_path,
                "log": os.path.join(self.test_dir.name, "test_log.xml"),
                "start_script": self.start_script_path,
            },
        }

    def tearDown(self):
        # Cleanup after test
        self.test_dir.cleanup()

    @patch(
        "toml.load",
        return_value={
            "user": {
                "name": "test_user",
                "computer": "test_computer",
                "parametr": "test_param",
            },
            "paths": {
                "vfs": "test.zip",
                "log": "test_log.xml",
                "start_script": "start.sh",
            },
        },
    )
    @patch("builtins.open", new_callable=mock_open, read_data="This is a start script")
    def test_load_config(self, mock_file, mock_toml_load):
        # Test if the config loads correctly
        shell = ShellEmulator(self.config_path)
        self.assertEqual(shell.username, "test_user")
        self.assertEqual(shell.computer_name, "test_computer")
        self.assertEqual(shell.fs_zip_path, self.zip_path)

    def test_load_vfs(self):
        # Test if the virtual file system loads correctly
        shell = ShellEmulator(self.config_path)
        shell.load_vfs()
        self.assertIn("/folder/file1.txt", shell.vfs)
        self.assertEqual(shell.vfs["/folder/file1.txt"], "This is a test file")

    def test_ls_command(self):
        # Test ls command functionality
        shell = ShellEmulator(self.config_path)
        shell.load_vfs()
        with patch("builtins.print") as mocked_print:
            shell.ls()
            mocked_print.assert_any_call("file2.txt")
            mocked_print.assert_any_call("folder")

    def test_cd_command(self):
        # Test changing directories
        shell = ShellEmulator(self.config_path)
        shell.load_vfs()
        shell.cd("/folder")
        self.assertEqual(shell.current_path, "/folder")

    def test_invalid_cd_command(self):
        # Test invalid directory change
        shell = ShellEmulator(self.config_path)
        shell.load_vfs()
        with patch("builtins.print") as mocked_print:
            shell.cd("/nonexistent")
            mocked_print.assert_called_with("No such directory: /nonexistent")

    def test_logging(self):
        # Test if logging actions work
        shell = ShellEmulator(self.config_path)
        shell.create_log_file()
        shell.log_action("test_command")
        log_tree = ET.parse(shell.log_file)
        root = log_tree.getroot()
        actions = root.findall("action")
        self.assertEqual(actions[0].find("command").text, "test_command")

    def test_whoami_command(self):
        # Test whoami command
        shell = ShellEmulator(self.config_path)
        with patch("builtins.print") as mocked_print:
            shell.whoami()
            mocked_print.assert_called_with("test_user")

    @patch("builtins.input", side_effect=["whoami", "exit"])
    @patch("builtins.print")
    def test_shell_run(self, mock_print, mock_input):
        # Test shell run loop
        shell = ShellEmulator(self.config_path)
        with patch(
                "shell_emulator.ShellEmulator.exit_shell", side_effect=SystemExit
        ) as mock_exit:
            with self.assertRaises(SystemExit):
                shell.run()
            mock_print.assert_any_call("test_user@test_computer:/$ ")
            mock_print.assert_any_call("test_user")


if __name__ == "__main__":
    unittest.main()
