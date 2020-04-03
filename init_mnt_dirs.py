"""
@author : xinwen
@Time : 2020/3/30 15:55
@File : init_mnt_dirs.py
@contact : coderWen@163.com
@desc :
"""
from collections import namedtuple
import os

mnt_dirs = '''
- mnt
    - run
    - var
        - celery
        - log
            - gunicorn
            - supervisor
        - media
'''

Node = namedtuple('Node', ('name', 'childs', 'sp_count', 'parent_path'))
head = Node('', [], -4, os.path.dirname(os.path.abspath(__file__)))
last_node = head
parent_nodes = {
    -4: last_node
}

lines = mnt_dirs.splitlines(keepends=False)

for line, raw_text in enumerate(lines, start=0):
    if not raw_text:
        continue
    text = raw_text.rstrip(' ')
    sp_count = text.count(' ') - 1
    if (sp_count % 4):
        print(f'ERROR: {line}: {raw_text} has {sp_count} spaces')
        exit(-1)
    parent_node = parent_nodes[sp_count - 4]
    node = Node(text.rsplit(' ', 1)[1], [], sp_count,
                os.path.join(parent_node.parent_path, parent_node.name))
    parent_node.childs.append(node)
    parent_nodes[sp_count] = node
    last_node = node

fifo = head.childs[::-1]

while fifo:
    node = fifo.pop()
    fifo[0:0] = node.childs[::-1]
    path_name = os.path.join(node.parent_path, node.name)

    try:
        os.mkdir(path_name)
        print(f'INFO: Checking {path_name}... Create')
    except FileExistsError:
        print(f'INFO: Checking {path_name}... Exists')
