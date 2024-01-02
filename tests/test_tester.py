from __future__ import annotations

from typing import Type

import pytest

from checker.configs import PipelineStageConfig
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


class TestTester:
    # TODO: mock of course
    #   mock of checker_config
    #       mock of testing_config
    #       mock of default_params
    #   repository_dir
    #   reference_dir
    #   get_tasks

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
