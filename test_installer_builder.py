import os
import pathlib
from unittest import TestCase
from installer_builder2 import format_data_file

class TestDataFileFormatter(TestCase):
    def test_format_data_file(self):
        # Test single file
        self.assertEqual(
            format_data_file("file.txt"),
            f"{os.path.abspath('file.txt')}=file.txt"
        )
        
    def test_deployment_flag(self):
        # Create builder with deployment enabled
        from installer_builder2 import InstallerBuilder
        builder = InstallerBuilder("TestApp", enable_deployment=True)
        self.assertTrue(builder.enable_deployment)
        
        # Create builder with deployment disabled (default)
        builder = InstallerBuilder("TestApp")
        self.assertFalse(builder.enable_deployment)
        
        # Test directory
        self.assertEqual(
            format_data_file("testdir/"),
            f"{os.path.abspath('testdir')}=testdir/=**/*"
        )
        
        # Test pattern
        self.assertEqual(
            format_data_file("dir/*.txt"),
            f"{os.path.abspath('dir')}/*.txt=dir/"
        )
        
        # Test pre-formatted string
        self.assertEqual(
            format_data_file("source=target"),
            "source=target"
        )
