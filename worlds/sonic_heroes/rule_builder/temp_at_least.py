import dataclasses
from typing import Iterable, override, Any, Mapping, Self

from BaseClasses import CollectionState
from NetUtils import JSONMessagePart
from rule_builder.field_resolvers import FieldResolver, resolve_field
from rule_builder.options import OptionFilter
from rule_builder.rules import NestedRule, TWorld, Rule, True_, False_, Has, HasAll, HasAllCounts, HasAny, HasAnyCount
from worlds.AutoWorld import World





@dataclasses.dataclass(init=False)
class And(NestedRule[TWorld], game="Sonic Heroes"):
    """A rule that only returns true when all child rules evaluate as true"""

    @override
    def _instantiate(self, world: TWorld) -> Rule.Resolved:
        return And.from_resolved(world, [c.resolve(world) for c in self.children])

    @classmethod
    def from_resolved(cls, world: TWorld, children_to_process: list[Rule.Resolved]) -> Rule.Resolved:
        clauses: list[Rule.Resolved] = []
        items: dict[str, int] = {}
        true_rule: Rule.Resolved | None = None

        while children_to_process:
            child = children_to_process.pop(0)
            if child.always_false:
                # false always wins
                return child
            if child.always_true:
                # dedupe trues
                true_rule = child
                continue
            if isinstance(child, And.Resolved):
                children_to_process.extend(child.children)
                continue

            if isinstance(child, Has.Resolved):
                if child.item_name not in items or items[child.item_name] < child.count:
                    items[child.item_name] = child.count
            elif isinstance(child, HasAll.Resolved):
                for item in child.item_names:
                    if item not in items:
                        items[item] = 1
            elif isinstance(child, HasAllCounts.Resolved):
                for item, count in child.item_counts:
                    if item not in items or items[item] < count:
                        items[item] = count
            else:
                clauses.append(child)

        if not clauses and not items:
            return true_rule or True_().resolve(world)

        if len(items) == 1:
            item, count = next(iter(items.items()))
            clauses.append(Has(item, count).resolve(world))
        elif items and all(count == 1 for count in items.values()):
            clauses.append(HasAll(*items).resolve(world))
        elif items:
            clauses.append(HasAllCounts(items).resolve(world))

        if len(clauses) == 1:
            return clauses[0]

        return And.Resolved(
            tuple(clauses),
            player=world.player,
            caching_enabled=getattr(world, "rule_caching_enabled", False),
        )

    class Resolved(NestedRule.Resolved):
        @override
        def _evaluate(self, state: CollectionState) -> bool:
            for rule in self.children:
                if not rule(state):
                    return False
            return True

        @override
        def explain_json(self, state: CollectionState | None = None) -> list[JSONMessagePart]:
            messages: list[JSONMessagePart] = [{"type": "text", "text": "("}]
            for i, child in enumerate(self.children):
                if i > 0:
                    messages.append({"type": "text", "text": " & "})
                messages.extend(child.explain_json(state))
            messages.append({"type": "text", "text": ")"})
            return messages

        @override
        def explain_str(self, state: CollectionState | None = None) -> str:
            clauses = " & ".join([c.explain_str(state) for c in self.children])
            return f"({clauses})"

        @override
        def __str__(self) -> str:
            clauses = " & ".join([str(c) for c in self.children])
            return f"({clauses})"


@dataclasses.dataclass(init=False)
class Or(NestedRule[TWorld], game="Sonic Heroes"):
    """A rule that returns true when any child rule evaluates as true"""

    @override
    def _instantiate(self, world: TWorld) -> Rule.Resolved:
        return Or.from_resolved(world, [c.resolve(world) for c in self.children])

    @classmethod
    def from_resolved(cls, world: TWorld, children_to_process: list[Rule.Resolved]) -> Rule.Resolved:
        clauses: list[Rule.Resolved] = []
        items: dict[str, int] = {}

        while children_to_process:
            child = children_to_process.pop(0)
            if child.always_true:
                # true always wins
                return child
            if child.always_false:
                # falses can be ignored
                continue
            if isinstance(child, Or.Resolved):
                children_to_process.extend(child.children)
                continue

            if isinstance(child, Has.Resolved):
                if child.item_name not in items or child.count < items[child.item_name]:
                    items[child.item_name] = child.count
            elif isinstance(child, HasAny.Resolved):
                for item in child.item_names:
                    items[item] = 1
            elif isinstance(child, HasAnyCount.Resolved):
                for item, count in child.item_counts:
                    if item not in items or count < items[item]:
                        items[item] = count
            else:
                clauses.append(child)

        if not clauses and not items:
            return False_().resolve(world)

        if len(items) == 1:
            item, count = next(iter(items.items()))
            clauses.append(Has(item, count).resolve(world))
        elif items and all(count == 1 for count in items.values()):
            clauses.append(HasAny(*items).resolve(world))
        elif items:
            clauses.append(HasAnyCount(items).resolve(world))

        if len(clauses) == 1:
            return clauses[0]

        return Or.Resolved(
            tuple(clauses),
            player=world.player,
            caching_enabled=getattr(world, "rule_caching_enabled", False),
        )

    class Resolved(NestedRule.Resolved):
        @override
        def _evaluate(self, state: CollectionState) -> bool:
            for rule in self.children:
                if rule(state):
                    return True
            return False

        @override
        def explain_json(self, state: CollectionState | None = None) -> list[JSONMessagePart]:
            messages: list[JSONMessagePart] = [{"type": "text", "text": "("}]
            for i, child in enumerate(self.children):
                if i > 0:
                    messages.append({"type": "text", "text": " | "})
                messages.extend(child.explain_json(state))
            messages.append({"type": "text", "text": ")"})
            return messages

        @override
        def explain_str(self, state: CollectionState | None = None) -> str:
            clauses = " | ".join([c.explain_str(state) for c in self.children])
            return f"({clauses})"

        @override
        def __str__(self) -> str:
            clauses = " | ".join([str(c) for c in self.children])
            return f"({clauses})"





class AtLeast(NestedRule[TWorld], game="Sonic Heroes"):
    """A rule that returns true when at least N child rules evaluate as true"""

    count: int | FieldResolver

    def __init__(
        self,
        count: int | FieldResolver,
        *children: Rule[TWorld],
        options: Iterable[OptionFilter] = (),
        filtered_resolution: bool = False,
    ) -> None:
        super().__init__(*children, options=options, filtered_resolution=filtered_resolution)
        self.count = count

    @override
    def _instantiate(self, world: TWorld) -> Rule.Resolved:
        count = resolve_field(self.count, world, int)
        if count == 0:
            return True_().resolve(world)

        children_to_process = [c.resolve(world) for c in self.children]
        return AtLeast.from_resolved(count, world, children_to_process)

    @classmethod
    def from_resolved(cls, count: int, world: TWorld, children_to_process: list[Rule.Resolved]) -> Rule.Resolved:
        clauses: list[Rule.Resolved] = []

        while children_to_process:
            child = children_to_process.pop(0)
            if child.always_true:
                if count == 1:
                    return child
                count -= 1
                continue
            if child.always_false:
                # falses can be ignored
                continue

            clauses.append(child)

        if len(clauses) < count:
            return False_().resolve(world)
        if count == 1:
            # Switch to Or which has more optimized handling
            return Or.from_resolved(world, clauses)
        if count == len(clauses):
            # Switch to And which has more optimized handling
            return And.from_resolved(world, clauses)
        return AtLeast.Resolved(
            tuple(clauses),
            count=count,
            player=world.player,
            caching_enabled=getattr(world, "rule_caching_enabled", False),
        )

    @override
    def to_dict(self) -> dict[str, Any]:
        output = super().to_dict()
        count = self.count
        output["count"] = count.to_dict() if isinstance(count, FieldResolver) else count
        return output

    @override
    @classmethod
    def from_dict(cls, data: Mapping[str, Any], world_cls: "type[World]") -> Self:
        args = cls._parse_field_resolvers(data, world_cls.game)
        options = OptionFilter.multiple_from_dict(data.get("options", ()))
        children = [world_cls.rule_from_dict(c) for c in data.get("children", ())]
        return cls(
            args.pop("count"),
            *children,
            options=options,
            filtered_resolution=data.get("filtered_resolution", False),
        )

    class Resolved(NestedRule.Resolved):
        count: int

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            count = self.count
            for rule in self.children:
                if rule(state):
                    if count == 1:
                        return True
                    count -= 1
            return False

        @override
        def explain_json(self, state: CollectionState | None = None) -> list[JSONMessagePart]:
            messages: list[JSONMessagePart] = []
            if state is None:
                messages = [
                    {"type": "text", "text": "At least "},
                    {"type": "color", "color": "cyan", "text": str(self.count)},
                    {"type": "text", "text": " of ("},
                ]
            else:
                satisfied_count = sum(1 if child(state) else 0 for child in self.children)
                messages = [
                    {"type": "text", "text": "At least "},
                    {"type": "color", "color": "cyan", "text": f"{satisfied_count}/{self.count}"},
                    {"type": "text", "text": " of ("},
                ]
            for i, child in enumerate(self.children):
                if i > 0:
                    messages.append({"type": "text", "text": ", "})
                messages.extend(child.explain_json(state))
            messages.append({"type": "text", "text": ")"})
            return messages

        @override
        def explain_str(self, state: CollectionState | None = None) -> str:
            clauses = ", ".join([c.explain_str(state) for c in self.children])
            if state is None:
                return f"At least {self.count} of ({clauses})"
            satisfied_count = sum(1 if child(state) else 0 for child in self.children)
            return f"At least {satisfied_count}/{self.count} of ({clauses})"

        @override
        def __str__(self) -> str:
            clauses = ", ".join([str(c) for c in self.children])
            return f"At least {self.count} of ({clauses})"
