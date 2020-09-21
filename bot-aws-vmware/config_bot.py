import os
from telegram import BotCommand, Bot


token = os.getenv('TOKEN_TG')
bot = Bot(token=token)

def main():
    commands = [
            BotCommand('start', 'Init Bot'),
            BotCommand('aws_ec2_all', 'List ec2'),
            BotCommand('aws_ec2_stop_instance', 'Stop ec2'),
            BotCommand('aws_ec2_start_instance', 'Start ec2'),
            BotCommand('vcenter_list_vms', 'list vms'),
            BotCommand('vcenter_poweroff_vm', 'turn of vm'),
            BotCommand('vcenter_poweron_vm', 'turn on vm'),
            BotCommand('vcenter_update_cpu', 'update cpu'),
            BotCommand('vcenter_create_vm_default', 'create a vm default'),
            BotCommand('vcenter_delete_vm_default', 'delete a vm default'),

    ]
    set_commands = bot.set_my_commands(commands=commands)
    return set_commands