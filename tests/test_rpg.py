import pytest
import os
from rpg_tree import GameDecisionTree, load_story  # Import student functions

@pytest.fixture
def setup_tree():
    """Sets up a game tree from a sample story.txt file."""
    test_story = """1 | Start in a spaceship. 1) Search bridge 2) Explore cargo | 2 | 3
2 | The bridge is dark. 1) Turn on lights 2) Check console | 4 | 5
3 | The cargo hold has strange artifacts. 1) Inspect 2) Leave | -1 | -1
4 | Lights flicker and reveal a hidden hatch. | -1 | -1
5 | The console is broken beyond repair. | -1 | -1
"""
    with open("story.txt", "w") as file:
        file.write(test_story)

    tree = GameDecisionTree()
    load_story("story.txt", tree)
    return tree

def test_tree_construction(setup_tree):
    """Test if the tree is built correctly."""
    tree = setup_tree
    assert tree.root is not None
    assert tree.root.event_number == 1
    assert tree.root.left.event_number == 2
    assert tree.root.right.event_number == 3

def test_story_file_exists():
    """Check if story.txt exists before running tests."""
    assert os.path.exists("story.txt")

def test_leaf_nodes(setup_tree):
    """Ensure the tree correctly assigns leaf nodes."""
    tree = setup_tree
    assert tree.nodes[3].left is None
    assert tree.nodes[3].right is None

def test_invalid_choice_handling(monkeypatch, capsys, setup_tree):
    """Simulate invalid input to ensure the game reprompts."""
    tree = setup_tree

    inputs = iter(["hello", "5", "1"])  # Invalid inputs followed by a valid one
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    tree.play_game()
    captured = capsys.readouterr()
    assert "Invalid choice" in captured.out