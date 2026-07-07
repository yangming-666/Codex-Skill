import os
import importlib.util
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
from pathlib import Path


SCRIPT_PATH = Path(__file__).with_name("configure_tokenx24_api_key.py")
SPEC = importlib.util.spec_from_file_location("configure_tokenx24_api_key", SCRIPT_PATH)
config = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(config)


class ConfigureTokenX24ApiKeyTests(unittest.TestCase):
    def test_default_profile_uses_zshrc_for_zsh(self):
        path = config.default_profile_path(shell="/bin/zsh", system="Darwin", home="/tmp/home")

        self.assertEqual(path, Path("/tmp/home/.zshrc"))

    def test_default_profile_uses_zshrc_for_macos_when_shell_is_missing(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            path = config.default_profile_path(shell=None, system="Darwin", home="/tmp/home")

        self.assertEqual(path, Path("/tmp/home/.zshrc"))

    def test_default_profile_uses_bashrc_for_linux_bash(self):
        path = config.default_profile_path(shell="/bin/bash", system="Linux", home="/tmp/home")

        self.assertEqual(path, Path("/tmp/home/.bashrc"))

    def test_default_profile_uses_bash_profile_for_macos_bash(self):
        path = config.default_profile_path(shell="/bin/bash", system="Darwin", home="/tmp/home")

        self.assertEqual(path, Path("/tmp/home/.bash_profile"))

    def test_upsert_appends_managed_block_when_missing(self):
        updated = config.upsert_api_key("export OTHER=value\n", "tx-test-key", shell="zsh")

        self.assertIn(config.MARKER_START, updated)
        self.assertIn("export TOKENX24_API_KEY='tx-test-key'", updated)
        self.assertTrue(updated.endswith("\n"))

    def test_upsert_replaces_existing_managed_block(self):
        original = "\n".join(
            [
                "export OTHER=value",
                config.MARKER_START,
                "export TOKENX24_API_KEY='old-key'",
                config.MARKER_END,
                "",
            ]
        )

        updated = config.upsert_api_key(original, "new-key", shell="bash")

        self.assertIn("export OTHER=value", updated)
        self.assertIn("export TOKENX24_API_KEY='new-key'", updated)
        self.assertNotIn("old-key", updated)
        self.assertEqual(updated.count(config.MARKER_START), 1)

    def test_upsert_replaces_unmanaged_export(self):
        updated = config.upsert_api_key(
            "export TOKENX24_API_KEY=old\nexport OTHER=value\n",
            "new-key",
            shell="bash",
        )

        self.assertIn("export TOKENX24_API_KEY='new-key'", updated)
        self.assertIn("export OTHER=value", updated)
        self.assertNotIn("TOKENX24_API_KEY=old", updated)

    def test_write_api_key_creates_profile_and_sets_private_permissions(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            profile = Path(tmpdir) / ".zshrc"

            config.write_api_key(profile, "tx-test-key", shell="zsh")

            self.assertIn("TOKENX24_API_KEY", profile.read_text(encoding="utf-8"))
            mode = os.stat(profile).st_mode & 0o777
            self.assertEqual(mode, 0o600)

    def test_cli_requires_explicit_api_key_input(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            profile = Path(tmpdir) / ".zshrc"
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT_PATH),
                    "--profile",
                    str(profile),
                    "--shell",
                    "zsh",
                ],
                capture_output=True,
                text=True,
                timeout=5,
            )

            self.assertEqual(result.returncode, 2)
            self.assertIn("--api-key or --stdin is required", result.stderr)
            self.assertFalse(profile.exists())


if __name__ == "__main__":
    unittest.main()
