import pytest

from tk_grid_helper import grid_manager


def test_grid_manager(mocker):
    default_root_wrapper = mocker.Mock()
    mocker.patch("tk_grid_helper.tk_grid_helper.default_root_wrapper", default_root_wrapper)

    old_default_root = mocker.Mock(name="old default_root")
    default_root_wrapper.default_root = old_default_root

    with pytest.raises(ValueError):
        with grid_manager(mocker.Mock(name="parent")) as obj:
            assert default_root_wrapper.default_root == obj.parent
            raise ValueError

    assert default_root_wrapper.default_root == old_default_root
