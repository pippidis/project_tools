# Tools to set up and maintain projects
from pathlib import Path

class ProjectTools:
    ## DEFAULT VARIABLES

    # Names
    DEFAULT_COMPONENT_NAME = 'module_1'
    DEFAULT_INIT_FILE_NAME = '__init__.py'
    DEFAULT_README_FILE_NAME = 'readme.md'
    DEFAULT_TEST_FOLDER_NAME = 'tests'
    DEFAULT_LOGS_FOLDER_NAME = 'logs'
    DEFAULT_TEMP_FOLDER_NAME = 'temp'
    DEFAULT_COMMON_FOLDER_NAME = 'project_utils'
    DEFAULT_ASSETS_FOLDER_NAME = 'assets'
    DEFAULT_UTILS_FILE_NAME = 'utils.py'
    DEFAULT_COMPONENT_CODE_FOLDER_NAME = 'code'
    DEFAULT_LOGGING_CONFIG_FILE_NAME = 'logging.yaml'
    DEFAULT_CONFIG_FOLDER_NAME = 'config'
    DEFAULT_LOG_NAME = 'app.log'
    DEFAULT_SETTINGS_YAML_NAME = 'settings.yaml'

    # Pre- and Suffixs
    DEFAULT_TEST_PREFIX = 'test_'

    def __init__(self, 
                 root:Path = None, # type: ignore
                 components:list = None, # type: ignore

                 gitignore_template_path:Path = None, # type: ignore
                 utils_template_path:Path = None, # type: ignore
                 conftest_template_path:Path = None, # type: ignore
                 test_file_template_path: Path = None,# type: ignore
                 project_guide_template_path: Path = None,# type: ignore
                 log_utils_template_path: Path = None, # type: ignore
                 log_config_template_path: Path = None, # type: ignore
                 settings_utils_template_path: Path = None, # type: ignore
                 settings_yaml_template_path: Path = None, # type: ignore
                 **kwargs):
        
        # Setting up the list of the components: 
        self.components = [self.DEFAULT_COMPONENT_NAME] if not components else components

        # Creating the main paths paths
        self.root = Path(__file__).resolve().parent if not root else root

        # Assets paths
        self.gitignore_template_path = Path(__file__).resolve().parent / 'assets' / 'template_gitignore.txt' if not gitignore_template_path else gitignore_template_path
        self.utils_template_path = Path(__file__).resolve().parent / 'assets' / 'template_utils.txt' if not utils_template_path else utils_template_path
        self.conftest_template_path = Path(__file__).resolve().parent / 'assets' / 'template_conftest.txt' if not conftest_template_path else conftest_template_path
        self.test_file_template_path = Path(__file__).resolve().parent / 'assets' / 'template_test_file.txt' if not test_file_template_path else test_file_template_path
        self.project_guide_template_path = Path(__file__).resolve().parent / 'assets' / 'template_guide.md' if not project_guide_template_path else project_guide_template_path
        self.log_config_template_path = Path(__file__).resolve().parent / 'assets' / 'template_logging_config.yaml' if not log_config_template_path else log_config_template_path
        self.log_utils_template_path = Path(__file__).resolve().parent / 'assets' / 'template_utils_logging.txt' if not log_utils_template_path else log_utils_template_path
        self.settings_utils_template_path = Path(__file__).resolve().parent / 'assets' / 'template_settings.txt' if not settings_utils_template_path else settings_utils_template_path
        self.settings_yaml_template_path = Path(__file__).resolve().parent / 'assets' / 'template_settings_yaml.yaml' if not settings_yaml_template_path else settings_yaml_template_path

        # Default names: 
        self.init_file_name = self.DEFAULT_INIT_FILE_NAME
        self.readme_file_name = self.DEFAULT_README_FILE_NAME
        self.test_folder_name = self.DEFAULT_TEST_FOLDER_NAME
        self.logs_folder_name = self.DEFAULT_LOGS_FOLDER_NAME
        self.temp_folder_name = self.DEFAULT_TEMP_FOLDER_NAME
        self.assets_folder_name = self.DEFAULT_ASSETS_FOLDER_NAME
        self.utils_file_name = self.DEFAULT_UTILS_FILE_NAME
        self.test_file_prefix = self.DEFAULT_TEST_PREFIX
        self.component_code_folder_name = self.DEFAULT_COMPONENT_CODE_FOLDER_NAME
        self.common_folder_name = self.DEFAULT_COMMON_FOLDER_NAME
        self.config_folder_name = self.DEFAULT_CONFIG_FOLDER_NAME
        self.logging_config_file_name = self.DEFAULT_LOGGING_CONFIG_FILE_NAME
        self.log_file_name = self.DEFAULT_LOG_NAME
        self.settings_yaml_name = self.DEFAULT_SETTINGS_YAML_NAME

        # Overwritng any variable with kwargs: 
        for key, value in kwargs.items(): 
            self.__dict__[key] = value

        # Intitating empty lists: 
        self.folders_to_ignore = []

    ## UTILITY FUNCTIONS
    @staticmethod
    def create_and_check_empty_file(path: Path) -> bool:
        """
        Creates an empty file at the specified 'path' if it doesn't exist and checks if the file is empty.

        Args:
            path (Path): Path object representing the intended file path.

        Returns:
            bool: True if the file is empty after the operation, False if the file contains data.

        Raises:
            ValueError: If 'path' is a directory.
            OSError: For issues creating or accessing the file.
        """
        if path.is_dir():
            raise ValueError("Expected a file path, got a directory.")

        try:
            path.touch(exist_ok=True)  # Create the file if it doesn't exist
            return path.stat().st_size == 0  # Check if the file is empty
        except OSError as e:
            raise OSError(f"Error accessing {path}.") from e

    def create_folder(self, path: Path, add_to_gitignore:bool=False): 
        path.mkdir(parents=True, exist_ok=True) # Creates an empty folder at path if it does not exist
        if add_to_gitignore: self.folders_to_ignore.append(path) # Adds it to the list of things to ignore

    @staticmethod
    def copy_from_template(target_path:Path, 
                           template_path:Path, 
                           end_text:str='', 
                           replacement:dict=None, # type: ignore
                           only_empty_file:bool = True
                           ): 
        '''Copies template information from a template into the given file'''
        is_empty = ProjectTools.create_and_check_empty_file(target_path)
        if only_empty_file and not is_empty: return None # Checks if it is empty

        with target_path.open('w') as target_file:
            with template_path.open('r') as template_file: 
                text = template_file.read()
                if replacement: # Replaces keywords
                    for key, value in replacement.items():
                        text = text.replace(key, value)
                text += end_text
                target_file.write(text)

    ## CREATING MODULES ###################################
    def _create_gitignore(self):
        '''Creates the gitignore file'''
        end_text = '\n' + ''.join([f'{x.name}/\n' for x in self.folders_to_ignore])
        self.copy_from_template(self.root / '.gitignore', self.gitignore_template_path, end_text=end_text)

    def _create_readme(self, folder_path:Path):
        '''Creates a readme file'''
        component_name = folder_path.name
        readme_path = folder_path / self.readme_file_name
        is_empty = self.create_and_check_empty_file(readme_path)
        if not is_empty: return 
        text = f'# {component_name}\n'
        with readme_path.open('w') as file: 
            file.write(text)
    
    def _create_component(self, compnent_name):
        '''Creates a component'''
        # Making folder paths
        root_path = self.root / compnent_name
        code_path = root_path / self.component_code_folder_name
        test_path = root_path / self.test_folder_name
        
        # Creating the folders: 
        self.create_folder(root_path)
        self.create_folder(code_path)
        self.create_folder(test_path)

        # Creating the inits: 
        self.create_and_check_empty_file(root_path / self.init_file_name)
        self.create_and_check_empty_file(code_path / self.init_file_name)
        self.create_and_check_empty_file(test_path / self.init_file_name)

        # Creating the utils: 
        utils_path = code_path / self.utils_file_name
        replace = {'XX_LOGGING_SETUP_XX':'','XX_LOGGING_EXAMPLE_XX':''}
        replace['XX_LOGGING_SETUP_XX'] = f'from {self.common_folder_name}.logging import setup_logging\nlogger = setup_logging(__name__)'
        replace['XX_LOGGING_EXAMPLE_XX'] = f"logger.error('This is an Error example')"
        self.copy_from_template(utils_path, self.utils_template_path, replacement=replace)

        # Identify the non-init files in the component
        files_in_component = [file for file in code_path.glob('*.py') if file.is_file() and file.name != self.init_file_name]

        # Creating the tests: 
        conftest_path = test_path / 'conftest.py'
        print(compnent_name)
        replace = {'XXXX':f'..{self.component_code_folder_name}.{utils_path.stem}'  , 'YYYY':'example_function'}
        self.copy_from_template(conftest_path, self.conftest_template_path, replacement=replace)

        # Create the files spesific tests
        for file in files_in_component:
            test_file_name = self.test_file_prefix + file.stem  + '.py'
            test_file_path = test_path / test_file_name
            if file.stem == self.utils_file_name:
                replace = {'XXXX': f'..{self.component_code_folder_name}.{file.stem}', 'YYYY':'example_function'} # As i have the example function in utils
            else: 
                replace = {'XXXX': f'..{self.component_code_folder_name}.{file.stem}', 'YYYY':'*'}
            self.copy_from_template(test_file_path, self.test_file_template_path, replacement=replace)


    def build(self):
        '''The main build function - build the folder structure for the project'''

        # Creates all the paths: 
        self.assets_path = self.root / self.assets_folder_name
        self.temp_path = self.root / self.temp_folder_name
        self.logs_path = self.root / self.logs_folder_name
        self.common_path = self.root / self.common_folder_name
        self.config_path = self.root / self.config_folder_name

        # Creates the root folders:
        self.create_folder(self.root) # To make sure that the root is actually there
        self.create_folder(self.assets_path)
        self.create_and_check_empty_file(self.assets_path / '.gitkeep') # To keep the folder when using git
        self.create_folder(self.temp_path, add_to_gitignore=True)
        self.create_folder(self.logs_path, add_to_gitignore=True)
        self.create_folder(self.common_path) # If i create looging, i need it
        self.create_folder(self.config_path)

        # Creates the root files:
        self._create_gitignore()
        self._create_readme(self.root)
        self.create_and_check_empty_file(self.root / 'main.py')
        self.copy_from_template(self.root / 'project_guide.md', self.project_guide_template_path)

        # Creating the logging configuration yaml and the setup logging file
        logging_confing_file_path = self.config_path / self.logging_config_file_name
        logging_utils_file_path = self.common_path / 'logging.py'
        self.copy_from_template(logging_confing_file_path, self.log_config_template_path) # The config for the logging
        replace = {'XX_LOG_CONFIG_PATH_XX': f"'{self.config_folder_name}' / '{self.logging_config_file_name}'", 
                    'XX_LOG_STORAGE_PATH_XX': f"'{self.logs_folder_name}'",
                    'XX_LOGFILE_DEFAULT_NAME_XX': self.log_file_name,
                    'XX_LOG_FILE_PREFIX_XX': ''
                    }
        self.copy_from_template(logging_utils_file_path, self.log_utils_template_path, replacement=replace) # The utility fucntion
    
        # Creates the settings system
        settings_utils_file_path = self.common_path / 'settings.py'
        settings_yaml_file_path = self.common_path / self.settings_yaml_name
        self.copy_from_template(settings_utils_file_path, self.settings_utils_template_path) # The config for the settings
        self.copy_from_template(settings_yaml_file_path, self.settings_yaml_template_path) # The standard config yaml

        # Creates the components: 
        for component in self.components: 
            self._create_component(component)


if __name__=='__main__':
    import shutil
    folder_path = Path.cwd() / '__testing__'
    print('DELETING THE TEST FOLDER FIRST')
    if folder_path.exists() and folder_path.is_dir():
        shutil.rmtree(folder_path)
    print('TESTING')
    builder = ProjectTools(root=folder_path, components=['library','gui', 'time_track'])
    print(builder.__dict__)
    builder.build()