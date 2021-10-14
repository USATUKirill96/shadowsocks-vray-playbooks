import json
import base64
import qrcode
import subprocess
import argparse
import urllib.parse

# Arguments
parser = argparse.ArgumentParser(description='Generate a QR code of the shadowsocks-libev\'s config.')

parser.add_argument('-c', '--config', type=str, help='Choose a specific config file.', nargs='?')
parser.add_argument('-s', '--save-path', type=str, help='Choose a specific QR code name & path to save.', nargs='?')
parser.add_argument('-p', '--profile', type=str, help='Save the QR code with specified profile name.', nargs='?', default='default')
parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', help='Show verbose output.')
parser.add_argument('--no-open', dest='prompt_open', action='store_false', help='Do not prompt to open the QR code.')

group = parser.add_mutually_exclusive_group()
group.add_argument('--ipv4', action='store_true', help='Using IPv4 IP address.')
group.add_argument('--ipv6', action='store_true', help='Using IPv6 IP address.')

args = parser.parse_args()

# Load shadowsocks configuration.
try:
    f = open(args.config)
except:
    f = open('config.json')
    print('== Config file not specified. Using default (./config.json).')

config = json.load(f)

if args.verbose:
    for l in f.readlines():
        print(l)

f.close()
encodestr = base64.b64encode((config['method'] + ':' + config['password']).encode()).decode()

# Confirm if it is ipv4 or ipv6.
if args.ipv4:
    srcstr = f"ss://{encodestr}@{config['server']}:{config['server_port']}"
    print(':: Using IPv4 IP address.')
elif args.ipv6:
    srcstr = f"ss://{encodestr}@[{config['server']}]:{config['server_port']}"
    print(':: Using IPv6 IP address.')
else:
    srcstr = f"ss://{encodestr}@{config['server']}:{config['server_port']}"
    print('== No specific IP address format. Using IPv4 IP address format.')

# Append the plugin and its params.
if "plugin" in config:
    srcstr += "?plugin=" + config['plugin']
    if "plugin_opts" in config:
        srcstr += urllib.parse.quote(';' + config['plugin_opts'])

# Append the profile name.
srcstr += "#" + args.profile

# For debug and verbose, print the final url string.
if args.verbose:
    print(srcstr)

# Create QR code.
try:
    qrcode.make(srcstr).save(args.save_path)
    print(f':: Image has been saved as {args.save_path} !')
except:
    qrcode.make(srcstr).save('image.png')
    print('== No specific image save path. Image has been saved as ./image.png !')

# Confirm if the user wants to open the QR code directly, using xdg-open.
def ifopen():
    answer = input('>> Open the QR Code? [Y/n] ')
    if answer == "n" or answer == "N":
        exit(0)
    elif answer == "y" or answer == "Y" or answer == "":
        try:
            if args.save_path is not None:
                subprocess.Popen('xdg-open ' + args.save_path, shell=True)
            else:
                subprocess.Popen('xdg-open image.png', shell=True)
        except:
            subprocess.Popen('xdg-open image.png', shell=True)
    else:
        print('!! Invalid option: ' + answer)
        ifopen()

if args.prompt_open:
    ifopen()
