import pytest
import provda


class TestBasic(object):

    def test_defaults(self):
        import sample
        param = provda.get_parameters("provda.tests.sample")
        assert param["use_x"] == True


@pytest.fixture
def exampleimp():
    import minipackage
    return minipackage

def test_main(exampleimp):
    assert len(exampleimp.param["demog"]) == 4

def test_sub(exampleimp):
    import minipackage.sub.examplemod
    print(provda.parameters.Parameters.manager)
    print(minipackage.sub.examplemod.params())
    assert len(minipackage.sub.examplemod.params())>0
