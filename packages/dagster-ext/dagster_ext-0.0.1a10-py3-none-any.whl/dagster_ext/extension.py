"""Meltano Dagster extension."""
from __future__ import annotations

import os
import pkgutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

import structlog
import typer
from cookiecutter.main import cookiecutter
from rich import print
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Confirm, Prompt

import files_dagster_ext
from meltano.edk import models
from meltano.edk.extension import ExtensionBase
from meltano.edk.process import Invoker, log_subprocess_error

log = structlog.get_logger()


class Dagster(ExtensionBase):
    """Extension implementing the ExtensionBase interface."""

    def __init__(self) -> None:
        """Initialize the extension."""
        self.invokers = {
            "dagster": Invoker("dagster"),
            "dagit": Invoker("dagit"),
            "cloud": Invoker("dagster-cloud"),
            "meltano": Invoker("meltano", env={**os.environ, "MELTANO_ENVIRONMENT": ""}),
        }

    @property
    def utility_name(self) -> str:
        return os.getenv("MELTANO_UTILITY_NAME", "dagster")

    @property
    def dagster_home(self) -> Path:
        return Path(os.getenv("DAGSTER_HOME"))

    @property
    def cookiecutter_template_dir(self) -> str:
        """
        Find the location of the files extention.
        This houses the cookiecutter project.
        """
        return Path(files_dagster_ext.__path__._path[0]) / "dagster"

    def set_meltano_config(self, description: str, config_name: str, config_value: str) -> None:
        spinner = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        )

        with spinner as progress:
            progress.add_task(description=description, total=None)
            self.get_invoker_by_name("meltano").run(
                "config",
                self.utility_name,
                "set",
                config_name,
                config_value,
            )

    def initialize(self, force: bool = False) -> None:
        # TODO: This method needs to be cleaned up in the future.
        repository_dir = Prompt.ask(
            "Where do you want to install the Dagster project?",
            default="$MELTANO_PROJECT_ROOT/orchestrate/dagster",
        )

        self.set_meltano_config(
            description="Setting Dagster repository directory",
            config_name="repository_dir",
            config_value=repository_dir,
        )

        repository_dir = os.path.expandvars(repository_dir)
        repository_dir = Path(repository_dir)

        # install_github_actions = Confirm.ask(
        #     "Do you want to setup Dagster Cloud Serverless?",
        #     default=True,
        # )

        # if install_github_actions:
        #     cloud_organization = Prompt.ask("What is your Dagster Cloud organization name?")
        #     self.set_meltano_config(
        #         description="Setting Dagster Cloud organization",
        #         config_name="cloud_organization",
        #         config_value=cloud_organization,
        #     )

        #     cloud_api_token = Prompt.ask(
        #         "What is your Dagster Cloud api token?",
        #         password=True,
        #     )
        #     self.set_meltano_config(
        #         description="Setting Dagster Cloud organization",
        #         config_name="cloud_api_token",
        #         config_value=cloud_api_token,
        #     )

        #     cloud_location_name = Prompt.ask(
        #         "What is your Dagster Cloud location name?", default="meltano"
        #     )
        #     self.set_meltano_config(
        #         description="Setting Dagster Cloud location name",
        #         config_name="cloud_location_name",
        #         config_value=cloud_location_name,
        #     )

        # dbt_installed = Confirm.ask(
        #     "Do you have DBT installed?",
        #     default=True,
        # )

        # if dbt_installed:
        #     dbt_plugin = Prompt.ask(
        #         "Which DBT plugin do you have installed?",
        #         choices=["postgres", "snowflake", "bigquery", "redshift"],
        #     )
        #     print(
        #         "[blue]Make sure you define the DBT environment variables in the Dagster utility.[/blue]"
        #     )
        # else:
        #     dbt_plugin = None

        install_github_actions = True
        dbt_plugin = None

        cookiecutter_config = {
            "project_name": repository_dir.name,
            "install_github_actions": install_github_actions,
            "dbt_plugin": dbt_plugin,
        }

        cookiecutter(
            template=str(self.cookiecutter_template_dir),
            no_input=True,
            extra_context=cookiecutter_config,
            output_dir=str(repository_dir.parent),
            overwrite_if_exists=True,
        )

        print("[green]Successfully initialized your Dagster project![/green]")
        print("[green]Start Dagit by running `meltano invoke dagster:start`[/green]")

    def invoke(self, invoker: Invoker, command_name: str | None, *command_args: Any) -> None:
        """Invoke the underlying cli, that is being wrapped by this extension.

        Args:
            command_name: The name of the command to invoke.
            command_args: The arguments to pass to the command.
        """
        try:
            invoker.run_and_log(command_name, *command_args)
        except subprocess.CalledProcessError as err:
            log_subprocess_error(f"{invoker.bin} {command_name}", err, "Dagster invocation failed")
            sys.exit(err.returncode)

    def describe(self) -> models.Describe:
        """Describe the extension.

        Returns:
            The extension description
        """
        return models.Describe(
            commands=[
                models.ExtensionCommand(
                    name="dagster_extension",
                    description="extension commands",
                ),
                models.InvokerCommand(
                    name="dagster_invoker",
                    description="pass through invoker for dagster",
                ),
                models.InvokerCommand(
                    name="dagit_invoker",
                    description="pass through invoker for dagit",
                ),
                models.InvokerCommand(
                    name="cloud_invoker",
                    description="pass through invoker for dagster cloud",
                ),
            ]
        )

    def get_invoker_by_name(self, invoker_name: str) -> Invoker:
        return self.invokers[invoker_name]

    def pre_invoke(self, invoke_name: str | None, *invoke_args: Any) -> None:
        """Called before the extension is invoked.

        Args:
            invoke_name: The name of the command that will be passed to invoke.
            *invoke_args: The arguments that will be passed to invoke.
        """
        self.dagster_home.mkdir(parents=True, exist_ok=True)

    def pass_through_invoker(
        self, invoker_name: str, logger: structlog.BoundLogger, *command_args: Any
    ) -> None:
        """Pass-through invoker.

        This method is used to invoke the wrapped CLI with arbitrary arguments.
        Note this method will hard exit the process if an unhandled exception is
        encountered.

        Args:
            invoker_name: The name of the invoker, currently "dagster", "dagit" or "cloud".
            logger: The logger to use in the event an exception needs to be logged.
            *command_args: The arguments to pass to the command.
        """
        logger.debug(
            "pass through invoker called",
            command_args=command_args,
        )
        try:
            self.pre_invoke(None)
        except Exception:
            logger.exception(
                "pre_invoke failed with uncaught exception, please report to maintainer"
            )
            sys.exit(1)

        try:
            invoker = self.get_invoker_by_name(invoker_name)
            self.invoke(invoker, None, command_args)
        except Exception:
            logger.exception("invoke failed with uncaught exception, please report to maintainer")
            sys.exit(1)

        try:
            self.post_invoke(None)
        except Exception:
            logger.exception(
                "post_invoke failed with uncaught exception, please report to maintainer"  # noqa: E501
            )
            sys.exit(1)


if __name__ == "__main__":
    path = files_dagster_ext.__path__
