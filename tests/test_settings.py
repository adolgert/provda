import pytest
import provda


class TestBasic(object):
    def test_read(self):
        parameters = provda.get_parameters("provda.tests.sample")
        provda.read_json(open("sample.settings"))
        assert parameters["risk"]=="smoking"

        subparams = provda.get_parameters("provda.tests.submodule")
        assert subparams["algorithm"]=="steepest descent"

    def test_hierarchical(self):
        parameters = provda.get_parameters("provda.tests.sample")
        provda.read_json(open("sample.settings"))
        assert parameters["runlimit"]==10

    def test_defaults(self):
        import sample
        assert sample.parameters["risk"] == "highdiving"


@pytest.fixture
def exampleimp():
    import minipackage
    return minipackage

def test_main(exampleimp):
    assert len(exampleimp.param["demog"]) == 4

def test_sub(exampleimp):
    import minipackage.sub.examplemod
    print(minipackage.sub.examplemod.params())
    assert len(minipackage.sub.examplemod.params())>0
