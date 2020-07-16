# coding:utf-8

import unittest
import time
from author_book import Author, db, app


class DatabaseTest(unittest.TestCase):
    """数据库测试"""

    def setUp(self):
        app.testing = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:root@127.0.0.1:3306/flask_test"
        db.drop_all()
        db.create_all()

    def test_add_author(self):
        """测试添加作者的数据库操作"""
        author = Author(name="巴金", email="bajinsichuan@qq.com")
        db.session.add(author)
        db.session.commit()

        
        time.sleep(10)

        result_author=Author.query.filter_by(name="巴金").first()
        self.assertIsNotNone(result_author)

    def tearDown(self):
        """所有的测试执行后被执行 通常用来进行清理操作"""
        db.session.remove()
        db.drop_all()


if __name__ == '__main__':
    unittest.main()


