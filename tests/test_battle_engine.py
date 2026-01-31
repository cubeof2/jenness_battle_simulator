import pytest
from battle_engine import select_actor, get_living_members
from pcs import PC
from npcs import NPC

def test_get_living_members():
    p1 = PC("Alice")
    p2 = PC("Bob")
    p2.take_damage(10) # Kill Bob
    
    living = get_living_members([p1, p2])
    assert len(living) == 1
    assert living[0].name == "Alice"

def test_select_actor_priority():
    p1 = PC("Alice", expertise_attack=False)
    p2 = PC("Bob", expertise_attack=True)
    team = [p1, p2]
    
    # Both active, expert should be picked
    actor = select_actor(team, set())
    assert actor.name == "Bob"
    
    # If Bob already acted, Alice should be picked
    actor = select_actor(team, {p2})
    assert actor.name == "Alice"

def test_select_actor_empty_team():
    with pytest.raises(IndexError):
        select_actor([], set())
