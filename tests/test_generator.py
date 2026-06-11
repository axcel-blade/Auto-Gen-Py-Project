from auto_gen_py_project.generator import create_project
from pathlib import Path
import shutil
import tempfile
import os


class TestProjectCreation:
    """Test suite for project creation functionality"""

    def setup_method(self):
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)

    def teardown_method(self):
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)

    def test_project_creation_new_folder(self):
        project_name = "test_project"
        create_project(project_name)
        assert Path(project_name).exists()
        assert Path(project_name).is_dir()

    def test_src_directory_created(self):
        create_project("test_project")
        assert Path("test_project", "src").is_dir()

    def test_main_py_file_created(self):
        create_project("test_project")
        assert Path("test_project", "src", "main.py").is_file()

    def test_main_py_content(self):
        create_project("test_project")
        content = Path("test_project", "src", "main.py").read_text()
        assert "def main" in content
        assert "Hello World!" in content

    def test_init_py_created(self):
        create_project("test_project")
        assert Path("test_project", "src", "__init__.py").exists()

    def test_tests_directory_created(self):
        create_project("test_project")
        assert Path("test_project", "tests").is_dir()

    def test_test_file_created(self):
        create_project("test_project")
        assert Path("test_project", "tests", "test_main.py").is_file()

    def test_readme_created(self):
        create_project("test_project")
        readme = Path("test_project", "README.md")
        assert readme.exists()
        assert "test_project" in readme.read_text()

    def test_pyproject_toml_created(self):
        create_project("test_project")
        pyproject = Path("test_project", "pyproject.toml")
        assert pyproject.exists()
        assert "test_project" in pyproject.read_text()

    def test_gitignore_created(self):
        create_project("test_project")
        gitignore = Path("test_project", ".gitignore")
        assert gitignore.exists()
        content = gitignore.read_text()
        assert "__pycache__/" in content
        assert "*.pyc" in content

    def test_license_created(self):
        create_project("test_project")
        license_file = Path("test_project", "LICENSE")
        assert license_file.exists()
        assert "MIT License" in license_file.read_text()

    def test_project_structure_complete(self):
        create_project("test_project")
        expected = [
            Path("test_project", "src", "__init__.py"),
            Path("test_project", "src", "main.py"),
            Path("test_project", "src", "resources", ".gitkeep"),
            Path("test_project", "tests", "test_main.py"),
            Path("test_project", "tests", "conftest.py"),
            Path("test_project", "README.md"),
            Path("test_project", "pyproject.toml"),
            Path("test_project", ".gitignore"),
            Path("test_project", "LICENSE"),
            Path("test_project", "pybuild.py"),
            Path("test_project", "pybuild.bat"),
            Path("test_project", ".github", "workflows", "ci.yml"),
        ]
        for f in expected:
            assert f.exists(), f"Expected {f} was not created"

    def test_venv_created_in_new_folder(self):
        create_project("test_project")
        assert Path("test_project", ".venv").is_dir()


class TestGeneratedFeatures:
    """Tests for the new Gradle-equivalent features in generated projects."""

    def setup_method(self):
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)

    def teardown_method(self):
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)

    # Resources directory (src/main/resources equivalent)
    def test_resources_directory_created(self):
        create_project("test_project")
        assert Path("test_project", "src", "resources").is_dir()

    def test_resources_gitkeep_created(self):
        create_project("test_project")
        assert Path("test_project", "src", "resources", ".gitkeep").exists()

    # Gradle Wrapper equivalent
    def test_unix_wrapper_created(self):
        create_project("test_project")
        wrapper = Path("test_project", "pybuild")
        assert wrapper.exists()
        content = wrapper.read_text()
        assert ".venv" in content
        assert "auto_gen_py_project.build_system.cli" in content

    def test_windows_wrapper_created(self):
        create_project("test_project")
        wrapper = Path("test_project", "pybuild.bat")
        assert wrapper.exists()
        content = wrapper.read_text()
        assert ".venv" in content
        assert "auto_gen_py_project.build_system.cli" in content

    # pyproject.toml with dev dependencies
    def test_pyproject_has_dev_dependencies(self):
        create_project("test_project")
        content = Path("test_project", "pyproject.toml").read_text()
        assert "[project.optional-dependencies]" in content
        assert "dev" in content
        assert "pytest" in content
        assert "pytest-cov" in content
        assert "ruff" in content

    def test_pyproject_has_test_dependencies(self):
        create_project("test_project")
        content = Path("test_project", "pyproject.toml").read_text()
        assert "test" in content
        assert "pytest-xdist" in content

    def test_pyproject_has_lint_dependencies(self):
        create_project("test_project")
        content = Path("test_project", "pyproject.toml").read_text()
        assert "lint" in content
        assert "mypy" in content

    def test_pyproject_has_pytest_config(self):
        create_project("test_project")
        content = Path("test_project", "pyproject.toml").read_text()
        assert "[tool.pytest.ini_options]" in content
        assert "testpaths" in content

    def test_pyproject_has_coverage_config(self):
        create_project("test_project")
        content = Path("test_project", "pyproject.toml").read_text()
        assert "[tool.coverage.run]" in content

    # conftest.py
    def test_conftest_created(self):
        create_project("test_project")
        assert Path("test_project", "tests", "conftest.py").exists()

    def test_conftest_adds_src_to_path(self):
        create_project("test_project")
        content = Path("test_project", "tests", "conftest.py").read_text()
        assert "sys.path" in content
        assert "src" in content

    # Generated CI workflow
    def test_ci_yml_created(self):
        create_project("test_project")
        assert Path("test_project", ".github", "workflows", "ci.yml").exists()

    def test_ci_yml_has_matrix_builds(self):
        create_project("test_project")
        content = Path("test_project", ".github", "workflows", "ci.yml").read_text()
        assert "matrix" in content
        assert "python-version" in content

    def test_ci_yml_has_junit_xml(self):
        create_project("test_project")
        content = Path("test_project", ".github", "workflows", "ci.yml").read_text()
        assert "junit-xml" in content

    def test_ci_yml_has_coverage(self):
        create_project("test_project")
        content = Path("test_project", ".github", "workflows", "ci.yml").read_text()
        assert "coverage" in content
        assert "cov-report" in content

    def test_ci_yml_uploads_test_results(self):
        create_project("test_project")
        content = Path("test_project", ".github", "workflows", "ci.yml").read_text()
        assert "upload-artifact" in content
        assert "test-results" in content

    # Generated pybuild.py tasks
    def test_pybuild_has_check_task(self):
        create_project("test_project")
        content = Path("test_project", "pybuild.py").read_text()
        assert "def check():" in content

    def test_pybuild_has_assemble_task(self):
        create_project("test_project")
        content = Path("test_project", "pybuild.py").read_text()
        assert "def assemble():" in content

    def test_pybuild_has_run_task(self):
        create_project("test_project")
        content = Path("test_project", "pybuild.py").read_text()
        assert "def run():" in content

    def test_pybuild_has_coverage_task(self):
        create_project("test_project")
        content = Path("test_project", "pybuild.py").read_text()
        assert "def coverage():" in content

    def test_pybuild_has_lock_task(self):
        create_project("test_project")
        content = Path("test_project", "pybuild.py").read_text()
        assert "def lock():" in content

    def test_pybuild_has_task_groups(self):
        create_project("test_project")
        content = Path("test_project", "pybuild.py").read_text()
        assert 'group="verification"' in content
        assert 'group="build"' in content
        assert 'group="application"' in content
        assert 'group="utility"' in content

    def test_pybuild_test_task_writes_junit_xml(self):
        create_project("test_project")
        content = Path("test_project", "pybuild.py").read_text()
        assert "junit-xml" in content

    def test_pybuild_coverage_task_writes_html_and_xml(self):
        create_project("test_project")
        content = Path("test_project", "pybuild.py").read_text()
        assert "cov-report" in content
        assert "html" in content
        assert "xml" in content

    def test_gitignore_covers_new_artefacts(self):
        create_project("test_project")
        content = Path("test_project", ".gitignore").read_text()
        assert "htmlcov/" in content
        assert "requirements.lock" in content
        assert ".coverage" in content


class TestInitInCurrentFolder:
    """Test suite for init in current folder functionality (-i flag)"""

    def setup_method(self):
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)

    def teardown_method(self):
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)

    def test_init_in_current_folder(self):
        create_project("my_project", init_in_current_folder=True)
        assert Path("src").exists()
        assert Path("tests").exists()
        assert Path("README.md").exists()
        assert not Path("my_project").is_dir()

    def test_init_src_directory_in_current_folder(self):
        create_project("my_project", init_in_current_folder=True)
        assert Path("src").is_dir()

    def test_init_main_py_in_current_folder(self):
        create_project("my_project", init_in_current_folder=True)
        assert Path("src", "main.py").exists()

    def test_init_tests_in_current_folder(self):
        create_project("my_project", init_in_current_folder=True)
        assert Path("tests").is_dir()

    def test_init_readme_in_current_folder(self):
        create_project("my_project", init_in_current_folder=True)
        readme = Path("README.md")
        assert readme.exists()
        assert "my_project" in readme.read_text()

    def test_init_pyproject_in_current_folder(self):
        create_project("my_project", init_in_current_folder=True)
        pyproject = Path("pyproject.toml")
        assert pyproject.exists()
        assert "my_project" in pyproject.read_text()

    def test_init_gitignore_in_current_folder(self):
        create_project("my_project", init_in_current_folder=True)
        assert Path(".gitignore").exists()

    def test_init_license_in_current_folder(self):
        create_project("my_project", init_in_current_folder=True)
        assert Path("LICENSE").exists()

    def test_init_complete_structure(self):
        create_project("my_project", init_in_current_folder=True)
        expected = [
            Path("src", "__init__.py"),
            Path("src", "main.py"),
            Path("src", "resources", ".gitkeep"),
            Path("tests", "test_main.py"),
            Path("tests", "conftest.py"),
            Path("README.md"),
            Path("pyproject.toml"),
            Path(".gitignore"),
            Path("LICENSE"),
            Path("pybuild.py"),
            Path("pybuild.bat"),
            Path(".github", "workflows", "ci.yml"),
        ]
        for f in expected:
            assert f.exists(), f"Expected {f} was not created in current folder"

    def test_init_creates_venv_in_current_folder(self):
        create_project("my_project", init_in_current_folder=True)
        assert Path(".venv").is_dir()


class TestProjectNames:
    """Test suite for different project name variations"""

    def setup_method(self):
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)

    def teardown_method(self):
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)

    def test_project_with_hyphens(self):
        create_project("my-awesome-project")
        assert Path("my-awesome-project").exists()
        assert Path("my-awesome-project", "README.md").exists()

    def test_project_with_underscores(self):
        create_project("my_awesome_project")
        assert Path("my_awesome_project").exists()

    def test_project_with_numbers(self):
        create_project("project123")
        assert Path("project123").exists()


class TestEdgeCases:
    """Test suite for edge cases"""

    def setup_method(self):
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)

    def teardown_method(self):
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)

    def test_existing_project_folder(self):
        Path("existing_project").mkdir()
        create_project("existing_project")
        assert Path("existing_project", "src").exists()
        assert Path("existing_project", "README.md").exists()

    def test_idempotent_init_in_current_folder(self):
        create_project("my_project", init_in_current_folder=True)
        first_readme = Path("README.md").read_text()
        create_project("my_project", init_in_current_folder=True)
        second_readme = Path("README.md").read_text()
        assert first_readme == second_readme
        assert Path("src", "main.py").exists()
