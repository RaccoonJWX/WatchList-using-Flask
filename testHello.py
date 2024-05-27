import unittest
from hello import sayhello


# 测试用例继承 unittest.TestCase 类，在这个类中创建的以 test_ 开头的方法将会被视为测试方法。
class SayHelloTestCase(unittest.TestCase):  # 测试用例
    # setUp() 方法会在每个测试方法执行前被调用，而 tearDown() 方法则会在每一个测试方法执行后被调用
    def setUp(self):    # 测试固件
        pass

    def tearDown(self):  # 测试固件
        pass

    def test_sayhello(self):  # 第 1 个测试
        rv = sayhello()
        self.assertEqual(rv, 'Hello!')  # 使用断言方法判断程序功能是否正常

    def test_sayhello_to_somebody(self):    # 第 2 个测试
        rv = sayhello(to='Grey')
        self.assertEqual(rv, 'Hello, Grey!')


if __name__ == '__main__':
    unittest.main()
