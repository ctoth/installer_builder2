import os
import pathlib
import platform
import subprocess
from unittest import TestCase
from installer_builder2 import format_data_file, _format_nuitka_datafiles

class TestDataFileFormatter(TestCase):
    def test_format_data_file(self):
        # Test single file
        self.assertEqual(
            format_data_file("file.txt"),
            f"{os.path.abspath('file.txt')}=file.txt"
        )
        
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

    def test_deployment_flag(self):
        # Create builder with deployment enabled
        from installer_builder2 import InstallerBuilder
        builder = InstallerBuilder("TestApp", enable_deployment=True)
        self.assertTrue(builder.enable_deployment)
        
        # Create builder with deployment disabled (default)
        builder = InstallerBuilder("TestApp")
        self.assertFalse(builder.enable_deployment)

    def test_installer_builder_config(self):
        from installer_builder2 import InstallerBuilder
        
        builder = InstallerBuilder(
            "TestApp",
            version="1.2.3",
            company_name="Test Company",
            console=True
        )
        
        self.assertEqual(builder.app_name, "TestApp")
        self.assertEqual(builder.version, "1.2.3")
        self.assertEqual(builder.company_name, "Test Company")
        self.assertTrue(builder.console)

    def test_data_file_handling(self):
        from installer_builder2 import InstallerBuilder
        
        builder = InstallerBuilder("TestApp")
        builder.data_files = ["test.txt", "data/*.dat"]
        builder.data_directories = ["assets/"]
        
        # Test that data files are properly formatted
        formatted_files = _format_nuitka_datafiles(builder.data_files)
        self.assertTrue(any("test.txt" in f for f in formatted_files))
        self.assertTrue(any("*.dat" in f for f in formatted_files))

    def test_platform_specific(self):
        from installer_builder2 import InstallerBuilder
        
        builder = InstallerBuilder("TestApp")
        
        if platform.system() == "Windows":
            # Test Windows-specific paths
            self.assertTrue(str(builder.dist_path).endswith('dist'))
        elif platform.system() == "Darwin":
            # Test macOS-specific paths
            self.assertTrue(str(builder.dist_path).endswith('dist'))

    def test_error_handling(self):
        from installer_builder2 import InstallerBuilder
        import os
        
        # Create test file that will cause compilation error
        test_file = "test_main.py"
        
        # Test with invalid module import
        builder = InstallerBuilder("TestApp", main_module=test_file)
        with self.assertRaises(subprocess.CalledProcessError):
            builder.compile_distribution()
