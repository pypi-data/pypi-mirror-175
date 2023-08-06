from __future__ import annotations
import copy
from dataclasses import dataclass, field
from typing import List, Union, Dict, Set
from enum import Enum, auto

import numpy as np
from scipy.special import comb

from .attribute import (AttributeType, Uniformity, Configuration, PositionType,
                        AngularPosition, PlanarPosition)
from .entity import Entity


class ComponentType(Enum):
    NONE = auto()
    LEFT = auto()
    RIGHT = auto()
    UP = auto()
    DOWN = auto()
    OUT = auto()
    IN = auto()


class LayoutType(Enum):
    CENTER = auto()
    GRID_FOUR = auto()
    GRID_FIVE = auto()
    GRID_NINE = auto()


@dataclass
class PositionHistory:
    available: int
    sampled: List[Set[int]]


@dataclass(init=False)
class AttributeHistory:
    number: List[int]
    position: Dict[int, PositionHistory]
    shape: List[int]
    size: List[int]
    color: List[int]
    angle: List[int]

    def __init__(self, constraints):
        self.number = []
        self.position = {}
        self.shape = []
        self.size = []
        self.color = []
        self.angle = []
        for i in range(constraints.number.min + 1, constraints.number.max + 2):
            self.position[i] = PositionHistory(available=comb(
                constraints.positions.shape[0], i),
                                               sampled=[])


@dataclass
class Bounds:
    min: int
    max: int


@dataclass
class Constraints:
    number: Bounds
    shape: Bounds
    size: Bounds
    color: Bounds
    angle: Bounds
    uniformity: Bounds
    position_type: PositionType
    positions: Union[List[AngularPosition], List[PlanarPosition]]

    def __post_init__(self):
        self.positions = np.array(self.positions)


@dataclass
class Component:
    component_type: ComponentType
    layout_type: LayoutType
    constraints: Constraints
    config: Configuration = field(init=False)
    uniformity: Uniformity = field(init=False)
    history: AttributeHistory = field(init=False)
    entities: List[Entity] = field(init=False)
    initial_constraints: Constraints = field(init=False)

    def __post_init__(self):
        self.config = Configuration(self.constraints)
        self.uniformity = Uniformity(self.constraints)
        self.history = AttributeHistory(self.constraints)
        self.entities = []
        self.initial_constraints = copy.deepcopy(self.constraints)

    def setting_of(self, attr):
        return self.attr(attr).setting

    def attr(self, attr):
        return getattr(self.entity, attr.name.lower())

    @property
    def entity(self):
        return self.entities[0]

    def make_uniform(self, attr):
        setting = self.setting_of(attr)
        for entity in self.entities[1:]:
            entity_attr = getattr(entity, attr.name.lower())
            entity_attr.setting = setting

    def set_uniform(self, attr, setting):
        for entity in self.entities:
            entity_attr = getattr(entity, attr.name.lower())
            entity_attr.setting = setting

    def set_position(self):
        for entity, bbox in zip(self.entities, self.config.position.value):
            entity.bbox = bbox

    def sample(self,
               sample_position=False,
               sample_number=False,
               carryover=True,
               uniform=None):
        if sample_position or sample_number:
            if sample_number:
                self.config.number.sample(self.constraints)
            self.config.position.sample(self.config.number.value)
        if uniform is None:
            uniform = self.uniformity.value
        if uniform:
            if len(self.entities) > 0 and carryover:
                self.entities = [self.entities[0]]
            else:
                self.entities = [
                    Entity(name=str(0),
                           bbox=self.config.position.value[0],
                           constraints=self.constraints)
                ]
            for i, bbox in enumerate(self.config.position.value[1:]):
                entity = copy.deepcopy(self.entities[0])
                entity.name = str(i)
                entity.bbox = bbox
                self.entities.append(entity)
        else:
            self.entities = [
                Entity(name=str(i), bbox=bbox, constraints=self.constraints)
                for i, bbox in enumerate(self.config.position.value)
            ]

    def sample_unique(self, attr, history, initial_constraints):
        if attr is AttributeType.NUMBER:
            self.config.sample_unique(initial_constraints,
                                      history,
                                      inplace=True)
            self.sample(carryover=False)
        elif attr is AttributeType.POSITION:
            self.config.position.sample_unique(self.config.number.value,
                                               history,
                                               inplace=True)
            self.set_position()
        elif attr is AttributeType.ANGLE or \
                attr is AttributeType.UNIFORMITY:
            raise ValueError(f"unsupported operation attribute: {attr!s}")
        elif attr in AttributeType:
            if self.uniformity.value:
                self.attr(attr).sample_unique(initial_constraints,
                                              history,
                                              inplace=True)
                self.make_uniform(attr)
            else:
                for entity in self.entities:
                    entity_attr = getattr(entity, attr.name.lower())
                    entity_attr.sample_unique(initial_constraints,
                                              history,
                                              inplace=True)
        else:
            raise ValueError("unsupported operation")


def make_component(component_type, layout_type, position_type, positions, *,
                   number_min, number_max, shape_min, shape_max, size_min,
                   size_max, color_min, color_max, angle_min, angle_max,
                   uniformity_min, uniformity_max):
    return Component(component_type=component_type,
                     layout_type=layout_type,
                     constraints=Constraints(number=Bounds(min=number_min,
                                                           max=number_max),
                                             shape=Bounds(min=shape_min,
                                                          max=shape_max),
                                             size=Bounds(min=size_min,
                                                         max=size_max),
                                             color=Bounds(min=color_min,
                                                          max=color_max),
                                             angle=Bounds(min=angle_min,
                                                          max=angle_max),
                                             uniformity=Bounds(
                                                 min=uniformity_min,
                                                 max=uniformity_max),
                                             position_type=position_type,
                                             positions=positions))
