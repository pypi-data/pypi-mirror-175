# QUANTCONNECT.COM - Democratizing Finance, Empowering Individuals.
# Lean CLI v1.0. Copyright 2021 QuantConnect Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from pathlib import Path

from click import command, option, Choice, confirm, prompt

from lean.click import LeanCommand
from lean.constants import DEFAULT_DATA_DIRECTORY_NAME, DEFAULT_LEAN_CONFIG_FILE_NAME
from lean.container import container
from lean.models.errors import MoreInfoError


def _download_repository(output_path: Path) -> None:
    """Downloads the LEAN repository as a zip file.

    :param output_path: the path to the zip file where the LEAN repository must be saved to
    """
    logger = container.logger
    logger.info("Downloading latest sample data from the Lean repository...")

    # We download the entire Lean repository and extract the data and the launcher's config file
    # GitHub doesn't allow downloading a specific directory
    # Since we need ~80% of the total repository in terms of file size this shouldn't be too big of a problem
    response = container.http_client.get("https://github.com/QuantConnect/Lean/archive/master.zip", stream=True)

    total_size_bytes = int(response.headers.get("content-length", 0))
    print_file_size_at_mb = 10

    # Sometimes content length isn't set, don't show a progress bar in that case
    if total_size_bytes > 0:
        progress = logger.progress()
        progress_task = progress.add_task("")
    else:
        progress = progress_task = None

    try:
        with output_path.open("wb") as file:
            written_bytes = 0

            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
                written_bytes += len(chunk)

                if progress is not None:
                    progress.update(progress_task, completed=(written_bytes / total_size_bytes) * 100)

                file_size_mb = round(written_bytes / 1024 / 1024, 2)
                if file_size_mb >= print_file_size_at_mb:
                    print_file_size_at_mb += 20
                    logger.info(f"Download Progress {file_size_mb} MB")
    except KeyboardInterrupt as e:
        if progress is not None:
            progress.stop()
        raise e

    if progress is not None:
        progress.stop()


@command(cls=LeanCommand)
@option("--language", "-l",
              type=Choice(container.cli_config_manager.default_language.allowed_values, case_sensitive=False),
              help="The default language to use for new projects")
def init(language: str) -> None:
    """Scaffold a Lean configuration file and data directory."""

    from shutil import copytree
    from zipfile import ZipFile

    current_dir = Path.cwd()
    data_dir = current_dir / DEFAULT_DATA_DIRECTORY_NAME
    lean_config_path = current_dir / DEFAULT_LEAN_CONFIG_FILE_NAME

    # Abort if one of the files we are going to create already exists to prevent us from overriding existing files
    for path in [data_dir, lean_config_path]:
        if path.exists():
            relative_path = path.relative_to(current_dir)
            raise MoreInfoError(f"{relative_path} already exists, please run this command in an empty directory",
                                "https://www.lean.io/docs/v2/lean-cli/initialization/directory-structure#02-lean-init")

    logger = container.logger

    # Warn the user if the current directory is not empty
    if next(current_dir.iterdir(), None) is not None:
        logger.info("This command will create a Lean configuration file and data directory in the current directory")
        confirm("The current directory is not empty, continue?", default=False, abort=True)

    # Download the Lean repository
    tmp_directory = container.temp_manager.create_temporary_directory()
    _download_repository(tmp_directory / "master.zip")

    # Extract the downloaded repository
    with ZipFile(tmp_directory / "master.zip") as zip_file:
        zip_file.extractall(tmp_directory / "master")

    # Copy the data directory
    copytree(tmp_directory / "master" / "Lean-master" / "Data", data_dir)

    # Create the config file
    lean_config_manager = container.lean_config_manager
    config = (tmp_directory / "master" / "Lean-master" / "Launcher" / "config.json").read_text(encoding="utf-8")
    config = lean_config_manager.clean_lean_config(config)
    lean_config_manager.store_known_lean_config_path(lean_config_path)

    # Update the data-folder configuration
    config = config.replace('"data-folder": "../../../Data/"', f'"data-folder": "{DEFAULT_DATA_DIRECTORY_NAME}"')

    with lean_config_path.open("w+", encoding="utf-8") as file:
        file.write(config)

    # Prompt for some general configuration if not set yet
    cli_config_manager = container.cli_config_manager
    if cli_config_manager.default_language.get_value() is None:
        default_language = language if language is not None else prompt("What should the default language for new projects be?",
                                        default=cli_config_manager.default_language.default_value,
                                        type=Choice(cli_config_manager.default_language.allowed_values))
        cli_config_manager.default_language.set_value(default_language)

    logger.info(f"""
The following objects have been created:
- {DEFAULT_LEAN_CONFIG_FILE_NAME} contains the configuration used when running the LEAN engine locally
- {DEFAULT_DATA_DIRECTORY_NAME}/ contains the data that is used when running the LEAN engine locally

The following documentation pages may be useful:
- Setting up local autocomplete: https://www.lean.io/docs/v2/lean-cli/projects/autocomplete
- Synchronizing projects with the cloud: https://www.lean.io/docs/v2/lean-cli/projects/cloud-synchronization

Here are some commands to get you going:
- Run `lean create-project "My Project"` to create a new project with starter code
- Run `lean cloud pull` to download all your QuantConnect projects to your local drive
- Run `lean backtest "My Project"` to backtest a project locally with the data in {DEFAULT_DATA_DIRECTORY_NAME}/
""".strip())
