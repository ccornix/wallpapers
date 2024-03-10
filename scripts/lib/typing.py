"""Helper type aliases."""

__author__ = "ccornix"
__copyright__ = "Copyright (C) 2024 ccornix"
__license__ = "MIT"
__all__ = ["TNum"]

from sympy import Expr
from typing import TypeAlias

TNum: TypeAlias = int | Expr
