from my_tools import read_xml
import sys


def register_round_method(xml_dom, round_method_label_name) -> dict:
    """
    注册轮方法
    :param xml_dom: 仿真定义文件dom
    :param round_method_label_name: 轮方法标签名
    :return: 轮方法函数字典
    """
    round_method_label = xml_dom.getElementsByTagName(round_method_label_name)[0]
    round_method_dict = {
        'name': round_method_label.getAttribute('name'),
        'ID': round_method_label.getAttribute('ID'),
        'path': round_method_label.getAttribute('path'),
        'attribute_type': {},
        'attributes': {},
    }
    for one_attribute_label in round_method_label.getElementsByTagName('attribute'):
        round_method_dict['attribute_type'].update({
            one_attribute_label.getAttribute('name'): one_attribute_label.getAttribute('type'),
        })
        round_method_dict['attributes'].update({
            one_attribute_label.getAttribute('name'): None,
        })
        sys.path.append(round_method_dict['path'])
    return round_method_dict


if __name__ == '__main__':
    xml_dom = read_xml('simulation_define/SimulationDefinition.xml')
    root = xml_dom.documentElement
    primitiveRoundMethod_dict = register_round_method(root, 'primitiveRoundMethod')
    collectiveRoundMethod_dict = register_round_method(root, 'collectiveRoundMethod')
    adviserRoundMethod_dict = register_round_method(root, 'adviserRoundMethod')
    monitorRoundMethod_dict = register_round_method(root,'monitorRoundMethod')
    from aa__ import *  # 一个特定的名字

    globals()[primitiveRoundMethod_dict['name']](**primitiveRoundMethod_dict['attributes'])
    globals()[collectiveRoundMethod_dict['name']](**collectiveRoundMethod_dict['attributes'])
    globals()[adviserRoundMethod_dict['name']](**adviserRoundMethod_dict['attributes'])
    globals()[monitorRoundMethod_dict['name']](**monitorRoundMethod_dict['attributes'])
