from __future__ import annotations

from typing import Type

import pytest
from pytest_mock import MockFixture

from checker.configs import PipelineStageConfig, CheckerConfig
from checker.course import Course
from checker.plugins import PluginABC, PluginOutput


class _OutputEnvPlugin(PluginABC):
    name = 'env'

    class Args(PluginABC.Args):
        env_var: str

    def _run(self, args: Args, *, verbose: bool = False) -> PluginOutput:
        return PluginOutput(output=f'Env var value: {args.env_var}')


@pytest.fixture
def get_env_plugin() -> dict[str, Type[PluginABC]]:
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
    instance.repository_dir = ''
    instance.reference_dir = None
    instance.get_tasks.return_value = []
    return instance


@pytest.fixture
def get_env_checker_config(mocker: MockFixture, get_env_pipeline: list[PipelineStageConfig]) -> Course:
    instance = mocker.Mock(spec=CheckerConfig)
    instance.testing.search_plugins
    instance.testing.global_pipeline = get_env_pipeline
    instance.testing.tasks_pipeline = []
    instance.testing.report_pipeline = []
    instance.structure = None
    instance.default_parameters = {}
    return instance


class TestTester:
    # TODO: mock of checker_config, example: https://github.com/manytask/course-template/blob/main/.checker.yml
    #   mock of testing_config
    #   mock of structure_config with None
    #   mock of default_params

    # TODO: mock pipelineRunner, not pass pipeline?

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
