from __future__ import annotations

import ast
import typing as t


class _LintOutput(t.NamedTuple):
    lineno: int
    col_offset: int
    msg: str


class _Valiable(t.NamedTuple):
    name: str
    lineno: int
    type_: str


class ReassignmentChecker:
    name = "reassignment-checker"
    version = "0.0.1"

    def __init__(self, tree: ast.Module, filepath: str, lines: str) -> None:
        self.tree = tree

    def run(self) -> t.Iterator[tuple[int, int, str, type]]:
        if False:
            yield 0, 0, "ERROR", type(self)
        for o in self._check_names(self._analysis_valiables(ast.iter_child_nodes(self.tree))):
            yield o.lineno, o.col_offset, o.msg, type(self)

    @classmethod
    def _analysis_valiables(cls, childs: t.Iterator[ast.AST]) -> t.Iterator[_Valiable]:
        child = next(childs, None)
        if not child:
            return

        if isinstance(child, ast.Assign):
            for target in child.targets:
                for name in cls._get_assign_names(target):
                    yield _Valiable(name, child.lineno, "variable")
        elif isinstance(child, ast.AnnAssign):
            for name in cls._get_assign_names(child.target):
                yield _Valiable(name, child.lineno, "variable")

        yield from cls._analysis_valiables(childs)

    @classmethod
    def _get_assign_names(cls, target: ast.AST) -> list[str]:
        if isinstance(target, ast.Name):
            return [target.id]
        # elif isinstance(target, ast.Attribute):
        #     return [f"{cls._get_assign_names(target.value)}.{target.attr}"]
        elif isinstance(target, ast.Tuple):
            return [n for e in target.elts for n in cls._get_assign_names(e)]
        raise Exception(f"unknown ast type: {type(target)}, [{target._fields}]")

    @classmethod
    def _check_names(
        cls, targets: t.Iterator[_Valiable], valiables: t.Optional[list[_Valiable]] = None
    ) -> t.Iterator[_LintOutput]:
        target = next(targets, None)
        if not target:
            return

        _valiables: list[_Valiable] = valiables or list()

        for v in _valiables:
            if target.name == v.name:
                yield _LintOutput(
                    lineno=target.lineno,
                    col_offset=-1,
                    msg=f'RAC001 {v.type_} "{v.name}" (defined in line {v.lineno}) has been reassigned.',
                )
                break

        yield from cls._check_names(targets, _valiables + [target])
