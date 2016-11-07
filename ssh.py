# encoding: utf-8

"""
ssh.py
Created by Peng Xiao on 2016-10-15.
"""
# All rights reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from __future__ import print_function
from subprocess import Popen, PIPE
import logging
import os
import re
import shlex
import sys

from cliff.app import App
from cliff.lister import Lister
from cliff.commandmanager import CommandManager

HOME_PATH = os.path.expanduser("~")
SSH_PATH = os.path.join(HOME_PATH, '.ssh/')


def create_path_if_not_exist(path):
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path))


class SSHConfig(object):
    """ Read and Write ~/.ssh/config file.
    """

    SETTINGS_REGEX = re.compile(r'(\w+)(?:\s*=\s*|\s+)(.+)')

    def __init__(self, ssh_conf_file=None):

        self.ssh_conf_file = ssh_conf_file or os.path.expanduser("~/.ssh/config")
        create_path_if_not_exist(self.ssh_conf_file)
        self._config = []

    def load(self):

        host = {"host": ['*'], "config": {}}
        with open(self.ssh_conf_file) as file_obj:
            for line in file_obj:

                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                match = re.match(self.SETTINGS_REGEX, line)
                if not match:
                    raise Exception("Unparsable line %s" % line)
                key = match.group(1).lower()
                value = match.group(2)

                if key == 'host':
                    self._config.append(host)
                    host = {
                        'host': self._get_hosts(value),
                        'config': {}
                    }
                elif key == 'proxycommand' and value.lower() == 'none':
                    # Store 'none' as None; prior to 3.x, it will get stripped out
                    # at the end (for compatibility with issue #415). After 3.x, it
                    # will simply not get stripped, leaving a nice explicit marker.
                    host['config'][key] = None
                else:
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]

                    # identityfile, localforward, remoteforward keys are special
                    # cases, since they are allowed to be specified multiple times
                    # and they should be tried in order of specification.
                    if key in ['identityfile', 'localforward', 'remoteforward']:
                        if key in host['config']:
                            host['config'][key].append(value)
                        else:
                            host['config'][key] = [value]
                    elif key not in host['config']:
                        host['config'][key] = value
        self._config.append(host)
        return self._config

    def _get_hosts(self, host):
        """
        Return a list of host_names from host value.
        """
        try:
            return shlex.split(host)
        except ValueError:
            raise Exception("Unparsable host %s" % host)

    def dump(self):
        pass

    def reformat(self):
        pass


class SSHKeyManager(object):
    """SSH KEY managemnt.
    """

    def __init__(self):
        create_path_if_not_exist(SSH_PATH)

    @classmethod
    def generate(cls, key_name):
        """Generate SSH key file through ssh-keygen command.
        """
        key_path = os.path.join(SSH_PATH, key_name)
        if os.path.exists(key_path):
            print("SSH key name '%s' already existed" % key_name)
            sys.exit()
        cmd = "ssh-keygen -t rsa -N '' -f %s" % key_path
        p = Popen(shlex.split(cmd), stdout=PIPE)
        stdout = p.communicate()[0]
        if p.returncode != 0:
            print("Error handling would be nice, eh?")
        print(stdout.strip())
        return key_path

    @classmethod
    def list(cls):
        """List all valid SSH key.
        """
        ssh_key_file_list = []
        file_list = os.listdir(SSH_PATH)
        for _file in file_list:
            with open(os.path.join(SSH_PATH, _file)) as f:
                if 'BEGIN RSA PRIVATE KEY' in f.read():
                    ssh_key_file_list.append(_file)
        return ssh_key_file_list

    @classmethod
    def delete(cls, key_name):
        """Delete a SSH key pair, and check if this key used in .ssh/config file.
        """
        pass


class ListCommand(Lister):
    """Show a list of files in the current directory.
    The file name and size are printed by default.
    """

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(ListCommand, self).get_parser(prog_name)
        parser.add_argument('object', nargs='?', default='key', help='the object will list: key or host')
        return parser

    def take_action(self, parsed_args):
        if parsed_args.object == 'key':
            return (('Private Key Name',), ((key_name,) for key_name in SSHKeyManager.list()))
        elif parsed_args.object == 'host':
            ssh_config = SSHConfig().load()
            header = ('host', 'hostname', 'user', 'identityfile')
            return (
                header,
                ((
                    config['host'],
                    config['config'].get('hostname') or config['host'],
                    config['config'].get('user'),
                    config['config'].get('identityfile')) for config in ssh_config[1:]))
        else:
            self.log.error("only can list 'key' or 'host'")
            sys.exit()


class SSHApp(App):

    def __init__(self):
        command = CommandManager('sshapp.app')
        super(SSHApp, self).__init__(
            description='Small and smart SSH configuration tool.',
            version='0.1',
            command_manager=command,
            deferred_help=True,
            )
        commands = {
            'list': ListCommand,
        }
        for k, v in commands.iteritems():
            command.add_command(k, v)

    def initialize_app(self, argv):
        self.LOG.debug('initialize_app')

    def prepare_to_run_command(self, cmd):
        self.LOG.debug('prepare_to_run_command %s', cmd.__class__.__name__)

    def clean_up(self, cmd, result, err):
        self.LOG.debug('clean_up %s', cmd.__class__.__name__)
        if err:
            self.LOG.debug('got an error: %s', err)


def main(argv=sys.argv[1:]):
    myapp = SSHApp()
    return myapp.run(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
