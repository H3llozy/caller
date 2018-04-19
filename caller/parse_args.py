import argparse


def parse_args():
    parse = argparse.ArgumentParser()
    parse.add_argument('-p', '--port', type=int, help='监听端口',
                       default=5000)
    parse.add_argument('--host', type=str, help='主机地址',
                       default='0.0.0.0')
    return parse.parse_args()
