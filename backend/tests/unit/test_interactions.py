from app.routers.interactions import _filter_by_item_id
import pytest

def test_filter_excludes_interaction_with_different_learner_id():
    """Test that filtering by item_id=1 excludes interactions with item_id=1 but different learner_id"""
    class MockInteraction:
        def __init__(self, item_id, learner_id):
            self.item_id = item_id
            self.learner_id = learner_id

    interactions = [
        MockInteraction(item_id=1, learner_id=1),
        MockInteraction(item_id=1, learner_id=2),
        MockInteraction(item_id=2, learner_id=1),
        MockInteraction(item_id=3, learner_id=3),
    ]

    result = _filter_by_item_id(interactions, item_id=1)

    assert len(result) == 2
    
    for interaction in result:
        assert interaction.item_id == 1

def test_filter_by_item_id_with_none_value():
    """Test that filtering with item_id=None returns all interactions (edge case)"""
    class MockInteraction:
        def __init__(self, item_id, learner_id):
            self.item_id = item_id
            self.learner_id = learner_id
    
    interactions = [
        MockInteraction(item_id=1, learner_id=1),
        MockInteraction(item_id=2, learner_id=2),
        MockInteraction(item_id=3, learner_id=3),
    ]
    
    result = _filter_by_item_id(interactions, item_id=None)
    
    assert len(result) == 3
    assert result == interactions


def test_filter_by_item_id_empty_list():
    """Test that filtering an empty list returns empty list (boundary case)"""
    result = _filter_by_item_id([], item_id=1)
    assert result == []


def test_filter_by_item_id_no_matches():
    """Test filtering when no interactions match the item_id"""
    class MockInteraction:
        def __init__(self, item_id, learner_id):
            self.item_id = item_id
            self.learner_id = learner_id
    
    interactions = [
        MockInteraction(item_id=2, learner_id=1),
        MockInteraction(item_id=3, learner_id=2),
        MockInteraction(item_id=4, learner_id=3),
    ]
    
    result = _filter_by_item_id(interactions, item_id=1)
    assert len(result) == 0


def test_filter_by_item_id_multiple_learners_same_item():
    """Test filtering when multiple learners interacted with the same item"""
    class MockInteraction:
        def __init__(self, item_id, learner_id):
            self.item_id = item_id
            self.learner_id = learner_id
    
    interactions = [
        MockInteraction(item_id=5, learner_id=1),
        MockInteraction(item_id=5, learner_id=2),
        MockInteraction(item_id=5, learner_id=3),
        MockInteraction(item_id=6, learner_id=1),
    ]
    
    result = _filter_by_item_id(interactions, item_id=5)
    
    assert len(result) == 3
    for interaction in result:
        assert interaction.item_id == 5
    learner_ids = [i.learner_id for i in result]
    assert set(learner_ids) == {1, 2, 3}


def test_filter_by_item_id_preserves_order():
    """Test that filtering preserves the original order of interactions"""
    class MockInteraction:
        def __init__(self, item_id, learner_id):
            self.item_id = item_id
            self.learner_id = learner_id
    
    interactions = [
        MockInteraction(item_id=1, learner_id=3),
        MockInteraction(item_id=2, learner_id=2),
        MockInteraction(item_id=1, learner_id=1),
        MockInteraction(item_id=3, learner_id=4),
        MockInteraction(item_id=1, learner_id=5),
    ]
    
    result = _filter_by_item_id(interactions, item_id=1)
    
    assert len(result) == 3
    assert result[0].learner_id == 3
    assert result[1].learner_id == 1
    assert result[2].learner_id == 5
