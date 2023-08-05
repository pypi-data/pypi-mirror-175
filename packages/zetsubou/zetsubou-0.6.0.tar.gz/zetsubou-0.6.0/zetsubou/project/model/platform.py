from typing import List, Optional, Union
from enum import Enum
from dataclasses import dataclass, field

from zetsubou.project.model.filter import TargetFilter
from zetsubou.project.model.target import TargetData
from zetsubou.project.model.toolchain import ECompilerFamily
from bentoudev.dataclass.base import loaded_from_file


class EArch(Enum):
    x64 = 1
    x86 = 2


class ESystem(Enum):
    Windows = 1
    Linux = 2


class EVersionSelector(Enum):
    all = 1,
    latest = 2


@dataclass
class PlatformData(TargetData):
    filter: TargetFilter = field(default_factory=TargetFilter)


@dataclass
class IPlatformToolchain:
    family: ECompilerFamily
    version: Union[EVersionSelector, List[str]]


@dataclass
class IWindowsToolchain(IPlatformToolchain):
    toolset: Union[EVersionSelector, List[str]]


@dataclass
class ILinuxToolchain(IPlatformToolchain):
    libcxx: List[str]


@dataclass
@loaded_from_file
class Platform(TargetData):
    platform: str = None
    host_system: ESystem = None
    host_arch: EArch = None
    target_arch: EArch = None
    filters: Optional[List[PlatformData]] = field(default_factory=list)
    toolchains: List[Union[IPlatformToolchain, IWindowsToolchain, ILinuxToolchain]] = field(default_factory=list)
