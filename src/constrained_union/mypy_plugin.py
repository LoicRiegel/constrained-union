"""mypy plugin for constrained union checks."""

from __future__ import annotations

from typing import TYPE_CHECKING, Final, override

from mypy.plugin import FunctionContext, Plugin
from mypy.subtypes import find_member, is_subtype
from mypy.types import Instance, Type, UnionType, get_proper_type

if TYPE_CHECKING:
    from collections.abc import Callable

_ASSERT_UNION_IMPLEMENTS_NAME: Final[str] = "constrained_union._assert_union_implements.assert_union_implements"


class ConstrainedUnionsPlugin(Plugin):
    """mypy plugin that checks that all members of a union type implement a given Protocol."""

    @override
    def get_function_hook(self, fullname: str) -> Callable[[FunctionContext], Type] | None:
        if fullname == _ASSERT_UNION_IMPLEMENTS_NAME:
            return _assert_union_implements_hook
        return None


def _assert_union_implements_hook(ctx: FunctionContext) -> Type:
    default_return_type = get_proper_type(ctx.default_return_type)
    if not isinstance(default_return_type, Instance):
        return ctx.default_return_type
    try:
        union_type_arg, protocol_type_arg = default_return_type.args
    except ValueError:
        ctx.api.fail('Expected exactly two type arguments to "assert_union_implements"', ctx.context)
        return ctx.default_return_type
    union_type_arg = get_proper_type(union_type_arg)
    if not isinstance(union_type_arg, UnionType):
        ctx.api.fail('First type argument to "assert_union_implements" must be a union type', ctx.context)
        return ctx.default_return_type
    protocol_type_arg = get_proper_type(protocol_type_arg)
    if not isinstance(protocol_type_arg, Instance) or not protocol_type_arg.type.is_protocol:
        ctx.api.fail('Second type argument to "assert_union_implements" must be a protocol type', ctx.context)
        return ctx.default_return_type

    protocol_name = _type_display_name(protocol_type_arg)

    for member in union_type_arg.items:
        proper_member = get_proper_type(member)
        if is_subtype(proper_member, protocol_type_arg):
            continue
        member_name = _type_display_name(proper_member)
        ctx.api.fail(f'Union member "{member_name}" does not implement protocol "{protocol_name}"', ctx.context)
        for missing_attr in _missing_protocol_members(proper_member, protocol_type_arg):
            ctx.api.fail(f"Missing member: {missing_attr}", ctx.context)

    return ctx.default_return_type


def _missing_protocol_members(member: Type, protocol: Instance) -> list[str]:
    proper_member = get_proper_type(member)
    if not isinstance(proper_member, Instance):
        return []

    missing: list[str] = []
    for attr_name in protocol.type.protocol_members:
        if attr_name.startswith("__") and attr_name.endswith("__"):
            continue
        if find_member(attr_name, proper_member, proper_member) is None:
            missing.append(attr_name)

    return missing


def _type_display_name(typ: Type) -> str:
    proper = get_proper_type(typ)
    if isinstance(proper, Instance):
        return proper.type.name
    if isinstance(proper, UnionType):
        return " | ".join(_type_display_name(item) for item in proper.items)
    return str(proper)


def plugin(version: str) -> type[Plugin]:  # noqa: ARG001
    """Mypy plugin entry point."""
    return ConstrainedUnionsPlugin
