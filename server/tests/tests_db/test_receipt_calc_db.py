import unittest
from src.db.src.receipt_calc import *
from src.db.src.db_utils import *
from .db_test_utils import *

class TestReceiptCalc(unittest.TestCase):
    def setUp(self):
        """builds tables and inserts test data
        """        
        rebuildTablesWithTestData()

    def test_build_tables(self):
        """tests table building and seeding test data
        """        
        user_count = exec_get_one('SELECT COUNT(*) FROM users')
        item_count = exec_get_one('SELECT COUNT(*) FROM items')
        owner_count = exec_get_one('SELECT COUNT(*) FROM owners')

        actual = user_count[0]
        expected = 3
        self.assertEqual(actual, expected)

        actual = item_count[0]
        expected = 3
        self.assertEqual(actual, expected)

        actual = owner_count[0]
        expected = 2
        self.assertEqual(actual, expected)
    
    def test_add_user(self):
        """tests adding a user
        """        
        addUser("Mike")
        
        actual = getUserName(4)
        expected = "Mike"
        self.assertEqual(actual,expected)

    def test_add_item(self):
        """tests adding an item
        """        
        addItem("CVS","Tylenol",8,7.99)
        
        actual = getItem(4)
        expected = ({'cost_per_user': 8.62,'id': 4,'name': 'Tylenol','store': 'CVS','tax': 8,'total_cost': 8.62},)
        self.assertEqual(actual,expected)
    
    def test_remove_item(self):
        """tests removal of an item
        """
        removeItem(3)

        item_count = exec_get_one('SELECT COUNT(*) FROM items')
        owner_count = exec_get_one('SELECT COUNT(*) FROM owners')

        actual = item_count[0]
        expected = 2
        self.assertEqual(actual, expected)

        actual = owner_count[0]
        expected = 0
        self.assertEqual(actual, expected)

    def test_assign_owner(self):
        """tests assigning a user to an item
        """
        assignOwner(1,2)
        assignOwner(2,2)

        owner_count = exec_get_one('SELECT COUNT(*) FROM owners')

        actual = owner_count[0]
        expected = 4
        self.assertEqual(actual, expected)

        actual = getItemCostPerUser(2)
        expected = 3.44
        self.assertEqual(actual, expected)
    
    def test_assign_owner_exists(self):
        """tests assigning an owner assignment that exists
        """
        actual = assignOwner(1,3)
        expected = "Owner assignment already exists"
        self.assertEqual(actual, expected)
    
    def test_remove_owner(self):
        """tests removal of an owner assignment that exists
        """
        removeOwner(2)

        actual = getOwnerAssignment(2)
        expected = []
        self.assertEqual(actual, expected)

        actual = getItemCostPerUser(3)
        expected = 23.67
        self.assertEqual(actual, expected)
        
    def test_get_user_total(self):
        """tests retrieval of user total
        """        
        assignOwner(1,1)

        actual = getUserTotal(1)
        expected = 26.34
        self.assertEqual(actual, expected)

    def test_remove_user(self):
        """tests removal of a user
        """
        removeUser(1)

        actual = getItemCostPerUser(3)
        expected = 23.67
        self.assertEqual(actual, expected)
        
    def test_edit_user(self):
        """tests editing info of a user
        """                
        res = editUser(1,"Bobster")

        actual = res
        expected = "Bobster"
        self.assertEqual(actual, expected)
    
    def test_edit_item(self):
        """tests editing info of an item
        """
        editItem(2, "Target", "Potats", 8, 9.99, 9.99)

        actual = getItem(2)
        expected = ({'cost_per_user': 9.99,'id': 2,'name': 'Potats','store': 'Target','tax': 8,'total_cost': 9.99},)
        self.assertEqual(actual, expected)
        



