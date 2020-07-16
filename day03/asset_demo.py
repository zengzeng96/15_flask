#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020-03-12 22:50:24
# @Author  : ZENG JIA (zengjia42@126.com)
# @Link    : https://weibo.com/5504445825/profile?topnav=1&wvr=6


# here import the lib
import sys
import os
import re


def num_div(num1,num2):
    # assert 断言   后面是一个表达式 如果返回真 则断言成功  程序能够继续往下执行
    # 返回假 断言失败 assert 会抛出 assertionError 终止程序
    assert isinstance(num1, int)
    assert isinstance(num2, int)
    assert num2 != 0
    
    print(num1/num2)


def main():
    num_div(100, 2)
    # num_div("a", "b")
    # num_div(50, "b")
    # num_div(50, 0)




if __name__ == "__main__":
    main()
    
    
    