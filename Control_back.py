import sys


class ControlBack(object):
    def __init__(self, member_xml_path=None, program_path=None, record_path=None, generation=0, version=None,
                 ex_id=None):
        """
        定义函数
        :param member_xml_path: 成员xml文件地址
        :param program_path: 程序入口地址
        :param record_path: 记录生成路径
        :param generation: 迭代数
        :param version: 版本
        :param ex_id: 仿真ID
        """
        self.member_xml_path = member_xml_path
        self.program_path = program_path
        self.record_path = record_path
        self.generation = generation
        self.version = version
        self.ex_id = ex_id
        sys.path.append(member_xml_path)

    def import_setting_module(self):
        try:
            from 一个特定的名字 import 一个特定的入口函数，入口函数要有返回值，用来返回迭代进度，迭代进度需要自行计算
        except ModuleNotFoundError:
            print(
                'External module path: "' + self.member_xml_path + '" has no current module. Please check module name according Docs.')
            input('\nPress "enter" to exit.\n')
            exit()

    def self_check(self):
        return self.ex_id != None and self.version != None and self.generation != 0 and self.program_path != None and self.member_xml_path != None

    def run_main(self):
        if self.self_check():
            try:
                一个特定的入口函数，特定的入口函数需要的参数都在control_back里，但是现在的问题是怎么把迭代数给返回出来
            except Exception:
                input('main function error，input any word to exit')
                raise
        else:
            print('item is not complete.')
