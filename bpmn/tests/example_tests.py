
# FIXTURES ============================================
# @pytest.fixture(scope='module')
# def db():
#     print('*****SETUP*****')
#     db = StudentData()
#     db.connect('data.json')
#     yield db
#     print('******TEARDOWN******')
#     db.close()

# def test_hello_world(client):
    # assert 1 == 1

# def test_scott_data(db):
#     scott_data = db.get_data('Joseph')
#     assert scott_data['id'] == 1
#     assert scott_data['name'] == 'Joseph'
#     assert scott_data['result'] == 'pass'

# def test_mark_data(db):
#     mark_data = db.get_data('Jaden')
#     assert mark_data['id'] == 2
#     assert mark_data['name'] == 'Jaden'
#     assert mark_data['result'] == 'fail'

# SETUP TEARDOWN=========================================

# def setup_module(module):
    # print('*****SETUP*****')
    # global db
    # db = StudentData()
    # db.connect('data.json')
# def teardown_module(module):
    # print('******TEARDOWN******')
    # db.close()
# def test_scott_data():
    # scott_data = db.get_data('Joseph')
    # assert scott_data['id'] == 1
    # assert scott_data['name'] == 'Joseph'
    # assert scott_data['result'] == 'pass'
# def test_mark_data():
    # mark_data = db.get_data('Jaden')
    # assert mark_data['id'] == 2
    # assert mark_data['name'] == 'Jaden'
    # assert mark_data['result'] == 'fail'