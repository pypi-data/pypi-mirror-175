# Copyright (c) Qotto, 2022

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Union, Optional

from dataclasses_json import dataclass_json, config

__all__ = [
    'Namespace',
    'Matching',
    'Application',
    'Permission',
    'Organization',
    'Authorization',
    'Role',
    'User',
    'Member',
    'Account',
    'Cookie',
    'Identity',
]


class Matching(Enum):
    ALL = 'ALL'
    EXACT = 'EXACT'
    ASCENDANT = 'ASCENDANT'
    DESCENDANT = 'DESCENDANT'
    SAME_BRANCH = 'SAME_BRANCH'

    def __str__(self) -> str:
        return self.name


class Namespace:
    _nodes: list[str]

    def __init__(
            self,
            nodes: Union[str, list[str]],
    ) -> None:
        """
        >>> Namespace('a:::b  :c:d')
        a:b:c:d
        >>> Namespace(['a', '  b  ', 'c', '', '', 'd'])
        a:b:c:d
        >>> Namespace(['a:', 'b', 'c', 'd'])
        Traceback (most recent call last):
            ...
        ValueError: A node cannot contain colons ":".
        >>> Namespace(['a', 1, 'c', 'd'])
        Traceback (most recent call last):
            ...
        TypeError: A node must be a str.
        >>> Namespace('')
        Traceback (most recent call last):
            ...
        ValueError: Namespace must have at least one node.
        """
        if isinstance(nodes, str):
            nodes = list(filter(len, (v.strip().lower() for v in nodes.split(':'))))
        elif isinstance(nodes, list):
            if any(filter(lambda x: not isinstance(x, str), nodes)):
                raise TypeError("A node must be a str.")
            if any(filter(lambda x: ':' in str(x), nodes)):
                raise ValueError("A node cannot contain colons \":\".")
            nodes = list(filter(len, (v.strip().lower() for v in nodes)))
        if not nodes:
            raise ValueError("Namespace must have at least one node.")
        for node in nodes:
            if not node:
                raise ValueError("Namespace node must not be empty.")
        self._nodes = nodes

    @property
    def path(self) -> str:
        return ':'.join(self._nodes)

    @property
    def nodes(self) -> list[str]:
        return self._nodes.copy()

    def matches(self, other: Namespace, matching: Matching = Matching.ALL) -> bool:
        """
        Test is self is <matching> of other.
        """
        if matching == Matching.ALL:
            return True
        if matching == Matching.EXACT:
            return self == other
        if matching == Matching.ASCENDANT:
            return self >= other
        if matching == Matching.DESCENDANT:
            return self <= other
        if matching == Matching.SAME_BRANCH:
            return self <= other or self >= other
        raise ValueError(f"Unknown matching type {matching}.")

    def __eq__(self, other) -> bool:
        return (isinstance(other, Namespace)
                and len(self) == len(other)
                and self.path == other.path)

    def __hash__(self):
        return hash(self.path)

    def __le__(self, other) -> bool:
        return (isinstance(other, Namespace)
                and len(self) >= len(other)
                and Namespace(self._nodes[:len(other)]) == other)

    def __ge__(self, other) -> bool:
        return (isinstance(other, Namespace)
                and len(self) <= len(other)
                and Namespace(other._nodes[:len(self)]) == self)

    def __lt__(self, other) -> bool:
        return (isinstance(other, Namespace)
                and len(self) > len(other)
                and Namespace(self._nodes[:len(other)]) == other)

    def __gt__(self, other) -> bool:
        return (isinstance(other, Namespace)
                and len(self) < len(other)
                and Namespace(other._nodes[:len(self)]) == self)

    def __len__(self) -> int:
        return len(self._nodes)

    def __str__(self) -> str:
        return self.path

    def __repr__(self) -> str:
        return self.path


@dataclass_json
@dataclass(frozen=True)
class Application:
    application_id: str
    name: str
    description: str


@dataclass_json
@dataclass(frozen=True)
class Permission:
    application: Application
    permission_id: str
    name: str
    description: str


@dataclass_json()
@dataclass(frozen=True)
class Organization:
    organization_id: str
    name: str
    namespace: Namespace = field(
        metadata=config(
            field_name='namespace',
            encoder=str,
            decoder=Namespace,
        )
    )


@dataclass_json
@dataclass(frozen=True)
class Authorization:
    authorization_id: str
    name: str
    description: str
    organization: Organization
    inheritance: bool
    matching: Matching


@dataclass_json
@dataclass(frozen=True)
class Role:
    role_id: str
    name: str
    description: str
    organization: Organization
    inheritance: bool


@dataclass_json
@dataclass(frozen=True)
class Identity:
    identity_id: str
    name: str
    provider_id: str
    email: str
    user: Optional[User]
    blocked: bool


@dataclass_json
@dataclass(frozen=True)
class User:
    user_id: str
    name: str
    uuid: str
    is_superuser: bool


@dataclass_json
@dataclass(frozen=True)
class Member:
    member_id: str
    user: User
    organization: Organization


@dataclass_json
@dataclass(frozen=True)
class Account:
    account_id: str
    application: Application
    user: User
    enabled: bool
    data: dict


@dataclass_json
@dataclass(frozen=True)
class Cookie:
    name: str
    value: str
    domain: str
    max_age: int
    secure: bool
    http_only: bool

    def __str__(self):
        return f'Cookie"{self.name}={self.value}"'
