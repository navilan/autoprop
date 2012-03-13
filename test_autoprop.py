from autoprop import AutoProp

class TestClass(AutoProp):


    @AutoProp.default
    def source(self):
        return 'source'


def test_auto():
    t = TestClass()
    assert t.source == 'source'

def test_override():
    t = TestClass()
    t.source = 'source1'
    assert t.source == 'source1'
    t.source = 'source2'
    assert t.source == 'source2'
    t.source = None
    assert t.source == 'source'