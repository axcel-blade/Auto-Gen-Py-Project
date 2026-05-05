from auto_gen_py_project.generator import create_project
from pathlib import Path
import shutil
import tempfile
import os


class TestProjectCreation:
    """Test suite for project creation functionality"""

    def setup_method(self):
        """Setup test environment before each test"""
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)

    def teardown_method(self):
        """Cleanup after each test"""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)

    def test_project_creation_new_folder(self):
        """Test creating project in a new folder (traditional mode)"""
        project_name = "test_project"
        create_project(project_name)

        # Check if project folder exists
        assert Path(project_name).exists(), f"Project folder '{project_name}' was not created"
        assert Path(project_name).is_dir(), f"'{project_name}' is not a directory"

    def test_src_directory_created(self):
        """Test that src directory is created"""
        project_name = "test_project"
        create_project(project_name)

        src_path = Path(project_name, "src")
        assert src_path.exists(), "src directory was not created"
        assert src_path.is_dir(), "src is not a directory"

    def test_main_py_file_created(self):
        """Test that main.py is created in src directory"""
        project_name = "test_project"
        create_project(project_name)

        main_py = Path(project_name, "src", "main.py")
        assert main_py.exists(), "main.py was not created"
        assert main_py.is_file(), "main.py is not a file"

    def test_main_py_content(self):
        """Test that main.py has correct content"""
        project_name = "test_project"
        create_project(project_name)

        main_py = Path(project_name, "src", "main.py")
        content = main_py.read_text()
        
        assert "def hello():" in content, "hello() function not found in main.py"
        assert "Hello from your new Python project" in content, "Expected content not found"

    def test_init_py_created(self):
        """Test that __init__.py is created"""
        project_name = "test_project"
        create_project(project_name)

        init_py = Path(project_name, "src", "__init__.py")
        assert init_py.exists(), "__init__.py was not created"

    def test_tests_directory_created(self):
        """Test that tests directory is created"""
        project_name = "test_project"
        create_project(project_name)

        tests_path = Path(project_name, "tests")
        assert tests_path.exists(), "tests directory was not created"
        assert tests_path.is_dir(), "tests is not a directory"

    def test_test_file_created(self):
        """Test that test_main.py is created in tests directory"""
        project_name = "test_project"
        create_project(project_name)

        test_main = Path(project_name, "tests", "test_main.py")
        assert test_main.exists(), "test_main.py was not created"
        assert test_main.is_file(), "test_main.py is not a file"

    def test_readme_created(self):
        """Test that README.md is created"""
        project_name = "test_project"
        create_project(project_name)

        readme = Path(project_name, "README.md")
        assert readme.exists(), "README.md was not created"
        assert "test_project" in readme.read_text(), "Project name not in README"

    def test_pyproject_toml_created(self):
        """Test that pyproject.toml is created"""
        project_name = "test_project"
        create_project(project_name)

        pyproject = Path(project_name, "pyproject.toml")
        assert pyproject.exists(), "pyproject.toml was not created"
        content = pyproject.read_text()
        assert "test_project" in content, "Project name not in pyproject.toml"

    def test_gitignore_created(self):
        """Test that .gitignore is created"""
        project_name = "test_project"
        create_project(project_name)

        gitignore = Path(project_name, ".gitignore")
        assert gitignore.exists(), ".gitignore was not created"
        content = gitignore.read_text()
        assert "__pycache__/" in content, "__pycache__/ not in .gitignore"
        assert "*.pyc" in content, "*.pyc not in .gitignore"

    def test_license_created(self):
        """Test that LICENSE file is created"""
        project_name = "test_project"
        create_project(project_name)

        license_file = Path(project_name, "LICENSE")
        assert license_file.exists(), "LICENSE was not created"
        assert "MIT License" in license_file.read_text(), "MIT License text not found"

    def test_project_structure_complete(self):
        """Test that all expected files are created"""
        project_name = "test_project"
        create_project(project_name)

        expected_files = [
            Path(project_name, "src", "__init__.py"),
            Path(project_name, "src", "main.py"),
            Path(project_name, "tests", "test_main.py"),
            Path(project_name, "README.md"),
            Path(project_name, "pyproject.toml"),
            Path(project_name, ".gitignore"),
            Path(project_name, "LICENSE"),
        ]

        for file_path in expected_files:
            assert file_path.exists(), f"Expected file {file_path} was not created"

    def test_venv_created_in_new_folder(self):
        """Test that a .venv is created in the generated project folder"""
        project_name = "test_project"
        create_project(project_name)

        venv_path = Path(project_name, ".venv")
        assert venv_path.exists(), ".venv directory was not created"
        assert venv_path.is_dir(), ".venv is not a directory"


class TestInitInCurrentFolder:
    """Test suite for init in current folder functionality (-i flag)"""

    def setup_method(self):
        """Setup test environment before each test"""
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)

    def teardown_method(self):
        """Cleanup after each test"""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)

    def test_init_in_current_folder(self):
        """Test creating project in current folder with -i flag"""
        project_name = "my_project"
        create_project(project_name, init_in_current_folder=True)

        # Check that project files exist in current directory, not in subdirectory
        assert Path("src").exists(), "src directory was not created in current folder"
        assert Path("tests").exists(), "tests directory was not created in current folder"
        assert Path("README.md").exists(), "README.md was not created in current folder"

        # Ensure project folder was NOT created
        assert not Path(project_name).exists() or not Path(project_name).is_dir(), \
            f"'{project_name}' subdirectory should not be created with -i flag"

    def test_init_src_directory_in_current_folder(self):
        """Test src directory is created in current folder"""
        project_name = "my_project"
        create_project(project_name, init_in_current_folder=True)

        src_path = Path("src")
        assert src_path.exists(), "src directory was not created in current folder"
        assert src_path.is_dir(), "src is not a directory"

    def test_init_main_py_in_current_folder(self):
        """Test main.py is created in current folder's src"""
        project_name = "my_project"
        create_project(project_name, init_in_current_folder=True)

        main_py = Path("src", "main.py")
        assert main_py.exists(), "main.py was not created in current folder"

    def test_init_tests_in_current_folder(self):
        """Test tests directory is created in current folder"""
        project_name = "my_project"
        create_project(project_name, init_in_current_folder=True)

        tests_path = Path("tests")
        assert tests_path.exists(), "tests directory was not created in current folder"
        assert tests_path.is_dir(), "tests is not a directory"

    def test_init_readme_in_current_folder(self):
        """Test README.md is created in current folder"""
        project_name = "my_project"
        create_project(project_name, init_in_current_folder=True)

        readme = Path("README.md")
        assert readme.exists(), "README.md was not created in current folder"
        content = readme.read_text()
        assert "my_project" in content, "Project name not in README"

    def test_init_pyproject_in_current_folder(self):
        """Test pyproject.toml is created in current folder"""
        project_name = "my_project"
        create_project(project_name, init_in_current_folder=True)

        pyproject = Path("pyproject.toml")
        assert pyproject.exists(), "pyproject.toml was not created in current folder"
        content = pyproject.read_text()
        assert "my_project" in content, "Project name not in pyproject.toml"

    def test_init_gitignore_in_current_folder(self):
        """Test .gitignore is created in current folder"""
        project_name = "my_project"
        create_project(project_name, init_in_current_folder=True)

        gitignore = Path(".gitignore")
        assert gitignore.exists(), ".gitignore was not created in current folder"

    def test_init_license_in_current_folder(self):
        """Test LICENSE is created in current folder"""
        project_name = "my_project"
        create_project(project_name, init_in_current_folder=True)

        license_file = Path("LICENSE")
        assert license_file.exists(), "LICENSE was not created in current folder"

    def test_init_complete_structure(self):
        """Test that all expected files are created in current folder"""
        project_name = "my_project"
        create_project(project_name, init_in_current_folder=True)

        expected_files = [
            Path("src", "__init__.py"),
            Path("src", "main.py"),
            Path("tests", "test_main.py"),
            Path("README.md"),
            Path("pyproject.toml"),
            Path(".gitignore"),
            Path("LICENSE"),
        ]

        for file_path in expected_files:
            assert file_path.exists(), f"Expected file {file_path} was not created in current folder"

    def test_init_creates_venv_in_current_folder(self):
        """Test that .venv is created in current folder for -i mode"""
        project_name = "my_project"
        create_project(project_name, init_in_current_folder=True)

        venv_path = Path(".venv")
        assert venv_path.exists(), ".venv directory was not created in current folder"
        assert venv_path.is_dir(), ".venv in current folder is not a directory"


class TestProjectNames:
    """Test suite for different project name variations"""

    def setup_method(self):
        """Setup test environment before each test"""
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)

    def teardown_method(self):
        """Cleanup after each test"""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)

    def test_project_with_hyphens(self):
        """Test project name with hyphens"""
        project_name = "my-awesome-project"
        create_project(project_name)

        assert Path(project_name).exists(), f"Project folder '{project_name}' was not created"
        assert Path(project_name, "README.md").exists()

    def test_project_with_underscores(self):
        """Test project name with underscores"""
        project_name = "my_awesome_project"
        create_project(project_name)

        assert Path(project_name).exists(), f"Project folder '{project_name}' was not created"

    def test_project_with_numbers(self):
        """Test project name with numbers"""
        project_name = "project123"
        create_project(project_name)

        assert Path(project_name).exists(), f"Project folder '{project_name}' was not created"


class TestEdgeCases:
    """Test suite for edge cases"""

    def setup_method(self):
        """Setup test environment before each test"""
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)

    def teardown_method(self):
        """Cleanup after each test"""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)

    def test_existing_project_folder(self):
        """Test creating project when folder already exists"""
        project_name = "existing_project"
        # Create folder first
        Path(project_name).mkdir()

        # Should not raise error, should create files inside
        create_project(project_name)
        assert Path(project_name, "src").exists()
        assert Path(project_name, "README.md").exists()

    def test_idempotent_init_in_current_folder(self):
        """Test that init can be run multiple times (overwrites files)"""
        project_name = "my_project"
        
        # First run
        create_project(project_name, init_in_current_folder=True)
        first_readme = Path("README.md").read_text()

        # Second run should overwrite
        create_project(project_name, init_in_current_folder=True)
        second_readme = Path("README.md").read_text()

        # Both should have the same content
        assert first_readme == second_readme
        assert Path("src", "main.py").exists()