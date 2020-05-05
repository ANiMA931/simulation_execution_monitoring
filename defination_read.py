import sys


def register_round_method(xml_dom) -> dict:
    """
    注册轮方法
    :param xml_dom: 仿真定义文件dom
    :param round_method_label_name: 轮方法标签名
    :return: 轮方法函数字典
    """
    round_methods = {
        'primitiveRoundMethod': None,
        'collectiveRoundMethod': None,
        'adviserRoundMethod': None,
        'monitorRoundMethod': None,
    }
    label_names = ['primitiveRoundMethod', 'adviserRoundMethod', 'monitorRoundMethod', 'collectiveRoundMethod']
    for label_name in label_names:
        round_method_label = xml_dom.getElementsByTagName(label_name)[0]
        if round_method_label:
            round_method_dict = {
                'name': round_method_label.getAttribute('name'),
                'ID': round_method_label.getAttribute('ID'),
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
            round_methods[label_name] = round_method_dict
    return round_methods


def register_global_attribute_method(xml_dom) -> dict:
    global_attribute_method_labels = xml_dom.getElementsByTagName('globalAttributeRecursionMethod')
    global_attribute_dict = {}
    for one_global_attribute_method_label in global_attribute_method_labels:
        one_global_attribute_dict = {
            one_global_attribute_method_label.getAttribute('aName'): {
                'fName': one_global_attribute_method_label.getAttribute('fName'),
                'path': one_global_attribute_method_label.getAttribute('path'),
                'type': one_global_attribute_method_label.getAttribute('type'),
                'attribute_type': {},
                'attributes': {}
            }
        }
        for one_attribute_label in one_global_attribute_method_label.getElementsByTagName('attribute'):
            one_global_attribute_dict[one_global_attribute_method_label.getAttribute('aName')]['attribute_type'].update(
                {
                    one_attribute_label.getAttribute('name'): one_attribute_label.getAttribute('type')
                })
            one_global_attribute_dict[one_global_attribute_method_label.getAttribute('aName')]['attributes'].update({
                one_attribute_label.getAttribute('name'): None,
            })
        # if one_global_attribute_method_label.getAttribute('path') not in sys.path:
        #     sys.path.append(one_global_attribute_method_label.getAttribute('path'))
        global_attribute_dict.update(one_global_attribute_dict)
    return global_attribute_dict

# if __name__ == '__main__':
#     globals()[primitiveRoundMethod_dict['name']](**primitiveRoundMethod_dict['attributes'])
#     globals()[collectiveRoundMethod_dict['name']](**collectiveRoundMethod_dict['attributes'])
#     globals()[adviserRoundMethod_dict['name']](**adviserRoundMethod_dict['attributes'])
#     globals()[monitorRoundMethod_dict['name']](**monitorRoundMethod_dict['attributes'])
#     global_attribute_dict['globalAttribute2']['attributes']['f1'] = 0.94
#     for one_global_attribute_name in global_attribute_dict.keys():
#         print(1, globals()[one_global_attribute_name])
#         globals()[one_global_attribute_name] = globals()[
#             global_attribute_dict[one_global_attribute_name]['fName']
#         ](**global_attribute_dict[one_global_attribute_name]['attributes'])
#         print(2, globals()[one_global_attribute_name])
