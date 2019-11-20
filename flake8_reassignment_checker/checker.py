import ast
from typing import Iterator, Tuple, NamedTuple, Optional, List
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
        for o in self._check_names(self._analysis_valiables(ast.iter_child_nodes(self.tree))):
            yield o.lineno, o.col_offset, o.msg, type(self)

    @classmethod
    def _analysis_valiables(cls, childs: Iterator[ast.AST]) -> Iterator[_Valiable]:
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
    def _get_assign_names(cls, target: ast.AST) -> List[str]:
        if isinstance(target, ast.Name):
            return [target.id]
        # elif isinstance(target, ast.Attribute):
        #     return [f"{cls._get_assign_names(target.value)}.{target.attr}"]
        elif isinstance(target, ast.Tuple):
            return [n for e in target.elts for n in cls._get_assign_names(e)]
        raise Exception(f"unknown ast type: {type(target)}, [{target._fields}]")

    @classmethod
    def _check_names(
        cls, targets: Iterator[_Valiable], valiables: Optional[List[_Valiable]] = None
    ) -> Iterator[_LintOutput]:
        target = next(targets, None)
        if not target:
            return

        _valiables: List[_Valiable] = valiables or list()

        for v in _valiables:
            if target.name == v.name:
                yield _LintOutput(
                    lineno=target.lineno,
                    col_offset=-1,
                    msg=f'RAC001 {v.type_} "{v.name}" (defined in line {v.lineno}) has been reassigned.',
                )
                break

        yield from cls._check_names(targets, _valiables + [target])
