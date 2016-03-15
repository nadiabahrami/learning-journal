# -*- coding: utf-8 -*-

from testapp.models import MyModel, DBSession


def test_create_mymodel(dbtransaction):
    """Test for a change of state of the model."""
    new_model = MyModel(name="jill", value=42)
    assert new_model.id is None
    DBSession.add(new_model)
    DBSession.flush()
    assert new_model.id is not None
