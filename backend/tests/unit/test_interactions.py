import pytest
from app.routers.interactions import _filter_by_item_id

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