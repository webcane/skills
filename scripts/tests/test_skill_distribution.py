"""Integration checks in an isolated checkout; never install into real user dirs.

Run: python3 -m unittest discover -s scripts/tests -p 'test_skill_distribution.py'
"""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[2]


class DistributionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='skill-distribution-')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        shutil.copytree(ROOT / 'scripts', self.root / 'scripts', ignore=shutil.ignore_patterns('__pycache__'))
        # Substitute only the copied installer's home reference to exercise default
        # destinations without changing HOME or touching the developer's settings.
        installer = self.root / 'scripts/install-local.sh'
        installer.write_text(installer.read_text().replace('$HOME', '$TEST_USER_HOME'))
        self.user_dir = self.root / 'user with spaces'
        self.env = dict(os.environ, TEST_USER_HOME=str(self.user_dir))
        self.env.pop('INSTALL_DIR', None)
        self.env.pop('XDG_CONFIG_HOME', None)
        self.skill = self.root / 'skills/family/probe'
        (self.skill / 'references').mkdir(parents=True)
        (self.skill / 'SKILL.md').write_text('''---
name: probe
description: Distribution fixture
metadata:
  version: 1.2.3
  description_codex: Codex fixture
  description_claude_code: Claude Code fixture
  description_claudeai: Claude.ai fixture
---
# Probe
Use {{ASK_USER}} and {{MULTI_SELECT}}.
''')
        (self.skill / 'references/context.md').write_text('Resource payload\n')

    def run_script(self, script, *args, env=None, ok=True):
        result = subprocess.run(['bash', str(self.root / 'scripts' / script), *args],
                                cwd=self.root, env=env or self.env, text=True,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if ok:
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        else:
            self.assertNotEqual(result.returncode, 0)
        return result

    def installed(self, path, target):
        text = (path / 'probe/SKILL.md').read_text()
        self.assertEqual((path / 'probe/references/context.md').read_text(), 'Resource payload\n')
        if target == 'codex':
            self.assertIn('Codex fixture', text)
            self.assertNotIn('{{ASK_USER}}', text)
        elif target == 'claude-code':
            self.assertIn('Claude Code fixture', text)
            self.assertIn('AskUserQuestion', text)
        else:
            self.assertEqual(text, (self.skill / 'SKILL.md').read_text())

    def test_package_all_and_explicit_version(self):
        self.run_script('package-skill.sh', 'family/probe', '2.0.0')
        for suffix in ['.skill', '-2.0.0.skill', '-2.0.0.json']:
            self.assertTrue((self.root / 'dist' / ('probe' + suffix)).exists())
        for target in ['codex', 'claude-code', 'claudeai']:
            for suffix in ['', '-2.0.0']:
                with zipfile.ZipFile(self.root / f'dist/probe-{target}{suffix}.zip') as archive:
                    entry = 'skill.md' if target == 'claudeai' else 'SKILL.md'
                    self.assertIn(f'probe/{entry}', archive.namelist())
                    self.assertEqual(archive.read('probe/references/context.md'), b'Resource payload\n')

    def test_default_install_all_and_reinstall(self):
        self.run_script('install-local.sh', 'family/probe')
        paths = [('.agents/skills', 'codex'), ('.config/opencode/skills', 'opencode'),
                 ('.claude/skills', 'claude-code')]
        for path, target in paths:
            self.installed(self.user_dir / path, target)
        stale = self.user_dir / '.agents/skills/probe/stale.txt'
        stale.write_text('old')
        self.run_script('install-local.sh', 'family/probe', '--target', 'codex')
        self.assertFalse(stale.exists())

    def test_each_single_target(self):
        paths = {'codex': '.agents/skills', 'opencode': '.config/opencode/skills',
                 'claude-code': '.claude/skills'}
        for target, path in paths.items():
            with self.subTest(target=target):
                self.run_script('install-local.sh', '--target=' + target, 'family/probe')
                self.installed(self.user_dir / path, target)
                for other, other_path in paths.items():
                    if other != target:
                        self.assertFalse((self.user_dir / other_path).exists())
                shutil.rmtree(self.user_dir)

    def test_install_dir_inference_and_custom_target(self):
        for suffix, target in [('.agents/skills', 'codex'), ('.config/opencode/skills', 'opencode'),
                               ('.claude/skills', 'claude-code'), ('custom', 'generic')]:
            directory = self.root / 'override' / suffix
            self.run_script('install-local.sh', 'family/probe',
                            env=dict(self.env, INSTALL_DIR=str(directory)))
            self.installed(directory, target)
        custom = self.root / 'custom codex'
        self.run_script('install-local.sh', 'family/probe', '--target', 'codex',
                        env=dict(self.env, INSTALL_DIR=str(custom)))
        self.installed(custom, 'codex')
        self.assertFalse(self.user_dir.exists())

    def test_xdg_and_claude_alias(self):
        config = self.root / 'xdg config'
        self.run_script('install-local.sh', 'family/probe', '--target', 'opencode',
                        env=dict(self.env, XDG_CONFIG_HOME=str(config)))
        self.installed(config / 'opencode/skills', 'opencode')
        self.run_script('install-local.sh', 'family/probe', '--target', 'claude')
        self.installed(self.user_dir / '.claude/skills', 'claude-code')

    def test_bad_arguments_do_not_install(self):
        for args in [('family/probe', '--target', 'unknown'), ('family/probe', '--target'),
                     ('../probe',), ('/tmp/probe',), ('family/probe', '--typo')]:
            self.run_script('install-local.sh', *args, ok=False)
        self.run_script('install-local.sh', 'family/probe', '--target', 'all',
                        env=dict(self.env, INSTALL_DIR=str(self.root / 'override')), ok=False)
        self.assertFalse(self.user_dir.exists())
        self.assertFalse((self.root / 'override').exists())

    def test_build_failure_preserves_installation(self):
        destination = self.user_dir / '.agents/skills/probe'
        destination.mkdir(parents=True)
        (destination / 'keep.txt').write_text('existing installation')
        # An unknown neutral marker makes platform rendering fail.
        p = self.skill / 'SKILL.md'
        p.write_text(p.read_text() + '\n{{UNKNOWN_MARKER}}\n')
        self.run_script('install-local.sh', 'family/probe', '--target', 'codex', ok=False)
        self.assertEqual((destination / 'keep.txt').read_text(), 'existing installation')


if __name__ == '__main__':
    unittest.main()
