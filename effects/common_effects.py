from ..effect_system import Effect, Timing

def create_damage_boost_effect(amount: int) -> Effect:
    return Effect(
        name="Damage Boost",
        timing=Timing.ON_ATTACK,
        condition=lambda state: True,
        action=lambda state: setattr(
            state.current_attack,
            "damage",
            state.current_attack.damage + amount
        )
    )

def create_damage_reduction_effect(amount: int) -> Effect:
    return Effect(
        name="Damage Reduction",
        timing=Timing.ON_DEFEND,
        condition=lambda state: True,
        action=lambda state: setattr(
            state.current_attack,
            "damage",
            max(0, state.current_attack.damage - amount)
        )
    )

def create_heal_effect(amount: int) -> Effect:
    return Effect(
        name="Heal",
        timing=Timing.START_OF_TURN,
        condition=lambda state: True,
        action=lambda state: state.owner.heal(amount)
    ) 