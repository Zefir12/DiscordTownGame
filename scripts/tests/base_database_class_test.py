from scripts.database.data_types.base_classes.base_database_class import BaseDatabaseClass


class TestClass(BaseDatabaseClass):
    _prevent_parameters_from_inserting = ['x']
    _prevent_parameters_from_loading = ['y']

    def __init__(self):
        self.id = 0
        self.x = 0
        self.z = 0


test_data = {'_id': 1, 'x': 2, 'y': 3, 'z': 4}
print(f'[Raw data from database]: {test_data}')
A = TestClass()
print(f'[A object before loading]: {A.__dict__}')
A.load(test_data)
print(f'[A object  after loading]: {A.__dict__}')
data_inserted = A.json()
print(f'[Data inserted to database]: {data_inserted}')
