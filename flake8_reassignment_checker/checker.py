from __future__ import annotations

import ast
import typing as t

from dataclasses import dataclass
# from .utils import groupby_sort

UNCHECK_VALIABLE_NAMES = ["_"]


@dataclass(frozen=True)
class _LintOutput:
    lineno: int
    col_offset: int
    msg: str


@dataclass(frozen=True)
class _Valiable:
    name: str
    lineno: int
    type_: str


class NodeVisitor:
    """NodeVisitor for flake8_reassignment_checker

    The default ``ast.NodeVisitor`` cannot be used because the second argument is not supported.
    Therefore, it is supported by our own implementation.
    """
    @classmethod
    def visit(cls, node: ast.AST) -> t.Iterator[_LintOutput]:
        _, _iter = cls._visit(node)
        yield from _iter

    def _visit(
        cls, node: ast.AST, defined_valiables: t.Optional[dict[str, _Valiable]] = None
    ) -> tuple[dict[str, _Valiable], t.Iterator[_LintOutput]]:
        yield dict(), _LintOutput(
            lineno=getattr(node, "lineno", 0),
            col_offset=getattr(node, "col_offset", 0),
            msg=f"{type(node)} [{getattr(node, 'simple', '')}] {node._fields}",
        )
        yield from getattr(
            cls, f"_visit_{node.__class__.__name__}", cls._generic_visit
        )(node, defined_valiables or dict())

    @classmethod
    def _generic_visit(
        cls, node: ast.AST, defined_valiables: dict[str, _Valiable]
    ) -> t.Iterable[_LintOutput]:
        for field_name, value in ast.iter_fields(node):
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, ast.AST):
                        yield from cls.visit(item)
            elif isinstance(value, ast.AST):
                yield from cls.visit(value)

    @staticmethod
    def _get_duplicate_valiable(node: ast.Name, defined_valiables: dict[str, _Valiable]) -> t.Optional[_Valiable]:
        if node.id in UNCHECK_VALIABLE_NAMES:
            return None
        return defined_valiables.get(node.id)

    @classmethod
    def _visit_AnnAssign(cls, node: ast.AnnAssign, defined_valiables: dict[str, _Valiable]) -> t.Iterable[_LintOutput]:
        if isinstance(node.target, ast.Name):
            dv = cls._get_duplicate_valiable(node.target, defined_valiables)
            if dv:
                yield _LintOutput(
                    lineno=node.lineno,
                    col_offset=node.col_offset,
                    msg=f"RAC001 valiable '{node.target.id}' (defined in line {dv.lineno}) has been reassigned.",
                )
            else:


    @classmethod
    def _visit_Name(cls, node: ast.Name, defined_valiables: set[_Valiable]) -> t.Iterable[_LintOutput]:
        print("Name called ============")
        if isinstance(node.id, str):
            if node.id != '_':
                print(f"name='{node.id}'")
                for v in defined_valiables:
                    if node.id == v.name:
                        print(f"duplicate name: '{node.id}'")
        print("========================")
        if False:
            yield from cls._generic_visit(node, defined_valiables)


class ReassignmentChecker:
    name = "reassignment-checker"
    version = "0.0.1"

    def __init__(self, tree: ast.Module, filepath: str, lines: str) -> None:
        print(lines)
        self.tree = tree

    def run(self) -> t.Iterator[tuple[int, int, str, type]]:
        for o in NodeVisitor.visit(self.tree):
            print(f":{o.lineno}:{o.col_offset}: {o.msg}")
        yield 0, 0, '', type(self)
        # for name, v_iter in groupby_sort(
        #     self._analysis_valiables(ast.iter_child_nodes(self.tree)), key=lambda v: v.name
        # ):
        #     valiables: list[_Valiable] = list(v_iter)
        #     if len(valiables) != 1:
        #         first_defined_no = valiables[0].lineno
        #         for v in valiables[1:]:
        #             yield (
        #                 v.lineno,
        #                 0,
        #                 f'RAC001 {v.type_} "{v.name}" ' f"(defined in line {first_defined_no}) has been reassigned.",
        #                 type(self),
        #             )

    @classmethod
    def _analysis_valiables(cls, childs: t.Iterator[ast.AST]) -> t.Iterator[_Valiable]:
        for child in childs:
            if isinstance(child, ast.Assign):
                for target in child.targets:
                    for name in cls._get_assign_names(target):
                        yield _Valiable(name, child.lineno, "variable")
            elif isinstance(child, ast.AnnAssign):
                for name in cls._get_assign_names(child.target):
                    yield _Valiable(name, child.lineno, "variable")

    @classmethod
    def _get_assign_names(cls, target: ast.AST) -> list[str]:
        if isinstance(target, ast.Name):
            return [target.id]
        # elif isinstance(target, ast.Attribute):
        #     return [f"{cls._get_assign_names(target.value)}.{target.attr}"]
        elif isinstance(target, ast.Tuple):
            return [n for e in target.elts for n in cls._get_assign_names(e)]
        raise Exception(f"unknown ast type: {type(target)}, [{target._fields}]")
