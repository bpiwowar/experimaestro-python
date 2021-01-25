"""test_annotations.py

Test all the annotations for configurations and tasks
"""

# Annotation specific tests

from typing import Optional, List
from experimaestro import config, Param, task, help, Config
import experimaestro.core.types as types
import pytest
from typing_extensions import Annotated

# --- Test manual name for configuration


@config("annotations.b")
class B:
    pass


def test_fullname():
    assert str(B.__xpm__.identifier) == "annotations.b"


# --- Automatic name for configuration


@config()
class A:
    pass


def test_noname():
    assert str(A.__xpm__.identifier) == "experimaestro.tests.test_annotations.a"


# --- Use type annotations


def gettype(t: type):
    return t.__xpm__


def ArgumentValue(default=None, *, help=""):
    return default


def test_type_hinting():
    """Test for type hinting"""

    @config()
    class MyConfig:
        """A configuration

        Attributes:
            w: An integer
        """

        __xpmid__ = "annotations.class_variable.config"

        x: Param[int]
        y: Param[float] = 2.3
        z: Param[Optional[float]]
        t: Param[List[float]]
        w: Param[int]
        opt: Param[Optional[int]]

    ot = gettype(MyConfig)

    # Check required parameter
    arg_x = ot.getArgument("x")
    assert arg_x.name == "x"
    assert isinstance(arg_x.type, types.IntType)
    assert arg_x.required

    arg_y = ot.getArgument("y")
    assert arg_y.name == "y"
    assert isinstance(arg_y.type, types.FloatType)
    assert arg_y.default == 2.3
    assert not arg_y.required

    arg_z = ot.getArgument("z")
    assert arg_z.name == "z"
    assert isinstance(arg_y.type, types.FloatType)
    assert not arg_z.required

    arg_t = ot.getArgument("t")
    assert arg_t.name == "t"
    assert isinstance(arg_t.type, types.ArrayType)
    assert isinstance(arg_t.type.type, types.FloatType)
    assert arg_t.required

    arg_w = ot.getArgument("w")
    assert arg_w.help == "An integer"

    arg_opt = ot.getArgument("opt")
    assert not arg_opt.required


def test_redefined_param():
    @config(register=False)
    class A:
        x: Param[int]

    @config(register=False)
    class B:
        x: Param[int] = 3

    atx = gettype(A).getArgument("x")
    btx = gettype(B).getArgument("x")

    assert atx.required

    assert not btx.required


# --- Task annotations


def test_task_config():
    @config()
    class Output:
        pass

    @task()
    class Task:
        def config(self) -> Output:
            return Output()

    output = Task().submit(dryrun=True)
    assert type(output) == Output
