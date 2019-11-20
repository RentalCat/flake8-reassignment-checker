import ast
from typing import Iterator, Tuple, NamedTuple, Set, Optional
from . import __version__ as version


class _LintOutput(NamedTuple):
    lineno: int
    col_offset: int
    msg: str


class _Valiable(NamedTuple):
    name: str
    lineno: int
    type_: str


class ReassignmentChecker:
    name = "reassignment-checker"
    version = version

    def __init__(self, tree: ast.Module, filename: str) -> None:
        self.tree = tree

    def run(self) -> Iterator[Tuple[int, int, str, type]]:
        for o in self._check_names(
            self._analysis_valiables(ast.iter_child_nodes(self.tree))
        ):
            yield o.lineno, o.col_offset, o.msg, type(self)

    @classmethod
    def _analysis_valiables(cls, childs: Iterator[ast.AST]) -> Iterator[_Valiable]:
        child = next(childs, None)
        if not child:
            return

        if isinstance(child, ast.Assign):
            for target in child.targets:
                yield _Valiable(
                    name=cls._get_assign_name(target),
                    lineno=child.lineno,
                    type_="variable",
                )

        yield from cls._analysis_valiables(childs)

    @classmethod
    def _get_assign_name(cls, target: ast.AST) -> str:
        if isinstance(target, ast.Name):
            return target.id
        elif isinstance(target, ast.Attribute):
            return f"{cls._get_assign_name(target.value)}.{target.attr}"
        raise Exception()

    @classmethod
    def _check_names(
        cls, targets: Iterator[_Valiable], valiables: Optional[Set[_Valiable]] = None
    ) -> Iterator[_LintOutput]:
        target = next(targets, None)
        if not target:
            return

        _valiables: Set[_Valiable] = valiables or set()

        for v in _valiables:
            if target.name == v.name:
                yield _LintOutput(
                    lineno=target.lineno,
                    col_offset=-1,
                    msg=f'RAC001 {v.type_} "{v.name}" (defined in line {v.lineno}) has been reassigned.',
                )

        yield from cls._check_names(targets, _valiables | {target})
