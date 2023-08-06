"""
Collector plugin for helm charts
"""

import os

from typing import Any, Dict, Optional

from packageurl import PackageURL  # type: ignore

from hoppr import __version__
from hoppr.base_plugins.collector import SerialCollectorPlugin
from hoppr.base_plugins.hoppr import hoppr_rerunner
from hoppr.context import Context
from hoppr.hoppr_types.cred_object import CredObject
from hoppr.result import Result


class CollectHelmPlugin(SerialCollectorPlugin):
    """
    Class to copy helm charts
    """

    supported_purl_types = ["helm"]
    required_commands = ["helm"]

    def get_version(self) -> str:  # pylint: disable=duplicate-code
        return __version__

    def __init__(self, context: Context, config: Optional[Dict] = None) -> None:
        super().__init__(context=context, config=config)
        if self.config is not None:
            if "helm_command" in self.config:
                self.required_commands = [self.config["helm_command"]]

    @hoppr_rerunner
    def collect(
        self, comp: Any, repo_url: str, creds: CredObject = None
    ):  # pylint: disable=duplicate-code
        """
        Collect helm chart
        """

        purl = PackageURL.from_string(comp.purl)
        helm_result = self.check_purl_specified_url(purl, repo_url)
        if not helm_result.is_success():
            return helm_result

        target_dir = self.directory_for(
            purl.type, repo_url, subdir=f"{purl.name}_{purl.version}"
        )

        for subdir in ["", purl.name]:
            source_url = os.path.join(repo_url, subdir)
            self.get_logger().info(f"Copying helm chart from {source_url}")

            command = [
                "helm",
                "fetch",
                "--repo",
                source_url,
                "--destination",
                f"{target_dir}",
                purl.name,
                "--version",
                purl.version,
            ]

            password_list = []
            if creds is not None:
                command = command + [
                    "--username",
                    creds.username,
                    "--password",
                    creds.password,
                ]
                password_list = [creds.password]

            run_result = self.run_command(command, password_list)
            if run_result.returncode == 0:
                self.get_logger().info(
                    f"Complete helm chart artifact copy for {purl.to_string()}"
                )

                return Result.success()

        msg = f"Failed to download {purl.name} version {purl.version} helm chart"
        self.get_logger().error(msg)
        return Result.retry(msg)
