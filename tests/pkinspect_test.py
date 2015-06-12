# -*- coding: utf-8 -*-
u"""PyTest for :mod:`pykern.pkinspect`

:copyright: Copyright (c) 2015 Bivio Software, Inc.  All Rights Reserved.
:license: http://www.apache.org/licenses/LICENSE-2.0.html
"""
from __future__ import absolute_import, division, print_function, unicode_literals
from io import open

import subprocess
import sys

import pytest
import py

from pykern import pkinspect
from pykern import pkio
from pykern import pkunit


def test_module_basename():
    p1 = pkunit.import_module_from_data_dir('p1')
    assert pkinspect.module_basename(p1) == 'p1'
    m1 = pkunit.import_module_from_data_dir('p1.m1')
    assert pkinspect.module_basename(m1) == 'm1'
    assert pkinspect.module_basename(m1.C) == 'm1'
    assert pkinspect.module_basename(m1.C()) == 'm1'
    assert pkinspect.module_basename(m1) == 'm1'
    assert pkinspect.module_basename(m1.C) == 'm1'
    assert pkinspect.module_basename(m1.C()) == 'm1'
    p2 = pkunit.import_module_from_data_dir('p1.p2')
    assert pkinspect.module_basename(p2) == 'p2'
    m2 = pkunit.import_module_from_data_dir('p1.p2.m2')
    assert pkinspect.module_basename(m2) == 'm2'


def test_caller_module():
    m1 = pkunit.import_module_from_data_dir('p1.m1')
    assert __name__ == m1.caller_module().__name__, \
        'When called, caller_module should return this module'


def test_is_caller_main():
    m1 = pkunit.import_module_from_data_dir('p1.m1')
    assert not m1.is_caller_main(), \
        'When not called from main, is_caller_main is False'
    with pkio.save_chdir(pkunit.data_dir()):
        subprocess.check_call([
            sys.executable,
            '-c',
            'from p1 import m1; assert m1.is_caller_main()'])