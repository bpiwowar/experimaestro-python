"""Tests for type validation"""

import pytest
from pathlib import Path
from experimaestro import config, Typename, argument, pathargument, ConstantArgument
import experimaestro.api as api
from experimaestro.scheduler import Job
from .utils import TemporaryExperiment
import logging

valns = Typename("validation")


def expect_validate(value):
    value.__xpm__.validate()

def expect_notvalidate(value):
    with pytest.raises(ValueError):
        value.__xpm__.validate()



@argument("value", type=int)
@config()
class A: pass

@argument("a", type=A)
@config()
class B: pass

@pathargument("path", "outdir")
@config()
class C: pass


def test_simple():
    expect_validate(A(value=1))

def test_missing():
    expect_notvalidate(A())


def test_simple_nested():
    b = B()
    b.a = A(value=1)
    expect_validate(b)

def test_missing_nested():
    b = B()
    b.a = A()
    expect_notvalidate(b)
    
def test_type():
    @config(valns.type.a)
    class A(): pass

    @config(valns.type.b)
    class B: pass

    @argument("a", A)
    @config(valns.type.c)
    class C: pass

    with pytest.raises(ValueError):
        C(a=B())

    with pytest.raises(ValueError):
        c = C()
        c.a = B()

def test_subtype():
    @config(valns.subtype.a)
    class A(): pass

    @config(valns.subtype.a1)
    class A1(A): pass

    @argument("a", A)
    @config(valns.subtype.b)
    class B: pass

    expect_validate(B(a=A1()))


def test_path():
    """Test of @pathargument"""
    @pathargument("value", "file.txt")
    @config(valns.path.a)
    class A: pass

    a = A()
    a.__xpm__.validate()
    with TemporaryExperiment("constant") as ws:
        jobcontext = Job(a)
        a.__xpm__.seal(jobcontext)
        assert isinstance(a.value, Path)
        parents = list(a.value.parents)
        assert a.value.name == "file.txt"
        assert a.value.parents[0].name == a.__xpm__.identifier.hex()
        assert a.value.parents[1].name == str(a.__class__.__xpm__.typename)
        assert a.value.parents[2].name == "jobs"
        assert a.value.parents[3] == ws.path

def test_constant():
    """Test of @ConstantArgument"""
    @ConstantArgument("value", 1)
    @config(valns.constant.a)
    class A: pass

    a = A()
    a.__xpm__.validate()
    with TemporaryExperiment("constant") as ws:
        jobcontext = Job(a)
        a.__xpm__.seal(jobcontext)
        assert a.value == 1


@argument("a", int)
@config()
def notset(a, b): pass


def test_notset():
    expect_notvalidate(notset(a=1))

@argument("a", int)
@config()
def notdeclared(): pass

def test_notdeclared():
    expect_notvalidate(notdeclared(a=1))


@argument("x", type=int)
@config()
class Parent: pass

@config()
class Child(Parent): pass

def test_child():
    expect_validate(Child(x=1))


# --- Default value


@pytest.mark.parametrize('value,apitype', [(1.5, api.FloatType), (1, api.IntType), (False, api.BoolType)])
def test_default(value, apitype):
    @argument("default", default=value)
    @config(valns.default[str(type(value))])
    class Default: pass

    value = Default()
    expect_validate(value)
    assert Default.__xpm__.arguments["default"].type.__class__ == apitype


def test_seal():
    """Test value sealing"""

    @argument("a", int)
    @config(register=False)
    class A(): pass

    a = A(a=2)
    a.__xpm__.seal(None)
    
    with pytest.raises(AttributeError):
        a.a = 1