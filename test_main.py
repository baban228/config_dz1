import unittest
from unittest.mock import patch, MagicMock, mock_open
import zipfile
from io import StringIO
from shell_emulator import shell_emulator



class TestShellEmulator(unittest.TestCase):

    @patch("builtins.open", return_value=["name\n", "test.zip\n"])
    @patch("zipfile.ZipFile")
    def setUp(self, MockZipFile, mock_open):
        # Mock ZipFile and file content
        self.mock_zip = MagicMock()
        MockZipFile.return_value = self.mock_zip

        self.shell = shell_emulator()

    @patch.object(shell_emulator, 'create_path', return_value='/test/')
    @patch('zipfile.Path.iterdir')
    def test_ls(self, mock_iterdir, mock_create_path):
        # Setup the mock to return fake file list
        mock_iterdir.return_value = [MagicMock(name="file1"), MagicMock(name="file2")]

        # Capture print output
        with patch("builtins.print") as mock_print:
            self.shell.ls()
            mock_print.assert_any_call("file1")
            mock_print.assert_any_call("file2")

    @patch.object(shell_emulator, 'create_path', return_value='/test/')
    @patch('zipfile.Path.iterdir')
    @patch('zipfile.Path', return_value=MagicMock())
    def test_cd_success(self, MockPath, mock_iterdir, mock_create_path):
        # Mock the directory change
        mock_iterdir.return_value = [MagicMock(name="dir1"), MagicMock(name="dir2")]
        com = ["cd", "dir1"]

        with patch("builtins.print") as mock_print:
            self.shell.cd(com)
            mock_print.assert_called_with(self.shell.path_obj)

    @patch.object(shell_emulator, 'create_path', return_value='/test/')
    @patch('zipfile.Path.iterdir')
    @patch('zipfile.Path', return_value=MagicMock())
    def test_cd_fail(self, MockPath, mock_iterdir, mock_create_path):
        # Mock the directory that doesn't exist
        mock_iterdir.return_value = [MagicMock(name="dir1")]
        com = ["cd", "dir2"]

        with patch("builtins.print") as mock_print:
            self.shell.cd(com)
            mock_print.assert_called_with("No such file or directory")

    @patch("builtins.open", return_value=MagicMock(readlines=MagicMock(return_value=['name', 'test.zip'])))
    @patch('zipfile.ZipFile')
    @patch('zipfile.Path.iterdir')
    def test_uniq(self, mock_iterdir, mock_zipfile, mock_open):
        # Setup mock for file reading and directory listing
        mock_iterdir.return_value = [MagicMock(name="file1")]
        mock_file = MagicMock()
        mock_file.readlines.return_value = ["line1", "line2", "line1"]
        mock_zipfile.return_value.open.return_value.__enter__.return_value = mock_file

        # Mock the file to have duplicate lines
        com = ["uniq", "file1"]

        with patch("builtins.print") as mock_print:
            self.shell.uniq(com[1])
            mock_print.assert_any_call("line1")
            mock_print.assert_any_call("line2")

    @patch.object(shell_emulator, 'create_path', return_value='/test/')
    def test_sawed_off_path(self, mock_create_path):
        # Test sawed_off_path
        self.shell.path = '/test/dir1/dir2/'
        result = self.shell.sawed_off_path(self.shell.path)
        self.assertEqual(result, '/test/dir1/')

    def test_create_path(self):
        # Test create_path with different cases
        self.assertEqual(self.shell.create_path("test"), "/test/")
        self.assertEqual(self.shell.create_path("/test"), "/test/")
        self.assertEqual(self.shell.create_path("test/"), "/test/")

    @patch("builtins.print")
    def test_main_loop_exit(self, mock_print):
        # Test the shell exit functionality
        with patch("builtins.input", return_value="exit"):
            with patch("sys.exit") as mock_exit:
                self.shell.main_loop()
                mock_exit.assert_called_once()


if __name__ == "__main__":
    unittest.main()
