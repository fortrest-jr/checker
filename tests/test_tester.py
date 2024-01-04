from __future__ import annotations

import os
from pathlib import Path
from typing import Type

import pytest
from pytest import CaptureFixture
from pytest_mock import MockFixture

from checker import plugins
from checker import tester
from checker.configs import PipelineStageConfig, CheckerConfig, CheckerTestingConfig
from checker.course import Course
from checker.plugins import PluginABC, PluginOutput


class _OutputEnvPlugin(PluginABC):
    name = 'env'

    class Args(PluginABC.Args):
        env_var: str

    def _run(self, args: Args, *, verbose: bool = False) -> PluginOutput:
        return PluginOutput(output=f'Env var value: {args.env_var}')


@pytest.fixture
def get_env_plugins() -> dict[str, Type[PluginABC]]:
    return {
        "env": _OutputEnvPlugin,
    }


@pytest.fixture
def get_env_pipeline() -> list[PipelineStageConfig]:
    return [
        PipelineStageConfig(
            name="stage1 - output env var value",
            run="env",
            args={"env_var": "${{ ENV_VAR }}"},
        )
    ]


@pytest.fixture
def no_tasks_course(mocker: MockFixture) -> Course:
    instance = mocker.Mock(spec=Course)
    instance.repository_root = Path('')
    instance.reference_root = instance.repository_root
    instance.get_tasks.return_value = []
    return instance


@pytest.fixture
def get_env_checker_config(mocker: MockFixture,
                           get_env_pipeline: list[PipelineStageConfig]) -> CheckerConfig:
    # example: https://github.com/manytask/course-template/blob/main/.checker.yml
    instance = mocker.Mock(spec=CheckerConfig)
    instance.testing = mocker.Mock(spec=CheckerTestingConfig)
    instance.testing.search_plugins = []
    instance.testing.global_pipeline = get_env_pipeline
    instance.testing.tasks_pipeline = []
    instance.testing.report_pipeline = []
    instance.structure = None
    instance.default_parameters = {}
    return instance


class TestTester:
    def test_env_var_through_plugin(self,
                                    mocker: MockFixture,
                                    capsys: CaptureFixture[str],
                                    get_env_pipeline: dict[str, Type[PluginABC]],
                                    get_env_checker_config: CheckerConfig,
                                    no_tasks_course: Course) -> None:
        env_var_name = 'ENV_VAR'
        env_var_val = "Test val 987"
        os.environ[env_var_name] = env_var_val

        mocker.patch.object(plugins, 'load_plugins')
        plugins.load_plugins.return_value = get_env_plugins
        tester_instance = tester.Tester(no_tasks_course, get_env_checker_config)
        tester_instance.run(Path(''))
        _, err = capsys.readouterr()

        assert env_var_val in err

    # TODO: test init

    # TODO: valid/invalid dir
    # TODO: get_context
    # TODO: add var in env, mocked pipline checks availability of env

    # TODO: [X] mock of plugin,
    #  [X] mock of pipeline,
    #  [] send env var,
    #  print env var in output,
    #  check output
    # TODO: test_pipeline.py
    pass
