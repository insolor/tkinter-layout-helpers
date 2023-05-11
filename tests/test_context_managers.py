import pytest

from tkinter_layout_helpers import grid_manager, pack_manager, set_parent


@pytest.mark.parametrize("context_manager", [set_parent, grid_manager, pack_manager])
def test_context_managers(context_manager, mocker):
    default_root_wrapper = mocker.Mock()
    mocker.patch("tkinter_layout_helpers.parent_manager._default_root_wrapper", default_root_wrapper)

    old_default_root = mocker.Mock(name="old default_root")
    default_root_wrapper.default_root = old_default_root

    with pytest.raises(ValueError):
        with context_manager(mocker.Mock(name="parent")) as obj:
            assert (
                default_root_wrapper.default_root == obj  # case for set_parent
                or default_root_wrapper.default_root == obj.parent
            )
            raise ValueError

    assert default_root_wrapper.default_root == old_default_root
