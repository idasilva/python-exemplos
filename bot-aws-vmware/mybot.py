import os

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler
from aws.ec2  import ec2_all_instances
from aws.ec2 import ec2_start
from aws.ec2 import ec2_stop
from config_bot import main as config_bot
from vmware.vcenter import  login_vmware
from vmware.vcenter import list_vms
from vmware.vcenter import poweroff_vm
from vmware.vcenter import poweron_vm
from vmware.vcenter import create_vm_deafult
from vmware.vcenter import delete_vm
from vmware.vcenter import update_cpu
from vmware.vcenter import get_cluster_id
from vmware.vcenter import get_folder_id
from vmware.vcenter import get_datastore_id

def start(update, context):
    message = 'Seja bem vindo ao Desafio Python'
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

def echo(update, context):
    message = 'Uma menssagem qualquer'
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)


def unknown(update, context):
    message = 'Command unknow'
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

def aws_ec2_all(update, context):
    instances  = ec2_all_instances()
    for instance in instances:
        instance_id = instance['instance_id']
        instance_name = instance['instance_name']
        instance_state_name = instance['instance_state_name']
        message = f'----> Instace Id: {instance_id}  - Instance Name: {instance_name} - Instance State :{instance_state_name} \n'
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)


def aws_ec2_stop_instance(update, context):
    try:
        instance_id  = context.args[0]
        action = ec2_stop(instance_id)
        message = action
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)

    except:
        message = "InstanceIds is missing"
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)

def aws_ec2_start_instance(update, context):
    try:
        instance_id  = context.args[0]
        action = ec2_start(instance_id)
        message = action
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)

    except:
        message = "InstanceIds is missing"
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)

def vcenter_list_vms(update, context):
    token_vmware = login_vmware()
    vms = list_vms(token)
    message = []
    for vm in vms:
        vm_id = vm['vm_id']
        vm_name = vm['vm_name']
        vm_power_state = vm['vm_power_count']
        vm_cpu_count = vm['vm_cpu_count']
        message += f'-----> Id :{vm_id} - Name: {vm_name} - State: {vm_power_state} - CPU: {vm_cpu_count}\n'
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

def vcenter_poweroff_vm(update, context):
    try:
        token_vmware = login_vmware()
        vmid = context.args[0]
        message = poweroff_vm(token_vmware,vmid)
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    except:
        message = "power of not working"
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)

def vcenter_poweron_vm(update, context):
    try:
        token_vmware = login_vmware()
        vmid = context.args[0]
        message = poweron_vm(token_vmware,vmid)
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    except:
        message = "power on not working"
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)

def vcenter_update_cpu(update,context):
    try:
        token_vmware = login_vmware()
        vmid = context.args[0]
        cpu = context.args[1]
        message = update_cpu(token_vmware,vmid,cpu)
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    except:
        message = "VM Id or CPU count is missing"
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)
   

def vcenter_create_vm_default(update, context):
    try:
        token_vmware = login_vmware()
        vmname = context.args[0]
        cluster_id = get_cluster_id(token_vmware)
        datastore_id = get_datastore_id(token_vmware,datastore_name='Please,create')
        folder_id = get_folder_id(token_vmware, folder_name='Please,create')
        message = create_vm_deafult(token_vmware,vmname,cluster_id,datastore_id,folder_id)
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    except:
        message = "create vm not working"
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)


def vcenter_delete_vm_default(update, context):
    try:
        token_vmware = login_vmware()
        vmid= context.args[0]
        message = delete_vm(token_vmware,vmid)
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    except:
        message = "delete vm not working"
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)


token = os.getenv("TOKEN_TG")


def main():
    bot_conf = config_bot()
    updater = Updater(token=token,use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start',start))
    dispatcher.add_handler(CommandHandler('aws_ec2_all',aws_ec2_all))
    dispatcher.add_handler(CommandHandler('aws_ec2_stop_instance',aws_ec2_stop_instance))
    dispatcher.add_handler(CommandHandler('aws_ec2_start_instance',aws_ec2_start_instance))
    dispatcher.add_handler(CommandHandler('vcenter_list_vms',vcenter_list_vms))
    dispatcher.add_handler(CommandHandler('vcenter_poweroff_vm',vcenter_poweroff_vm))
    dispatcher.add_handler(CommandHandler('vcenter_poweron_vm',vcenter_poweron_vm))
    dispatcher.add_handler(CommandHandler('vcenter_update_cpu',vcenter_update_cpu))
    dispatcher.add_handler(CommandHandler('vcenter_create_vm_default',vcenter_create_vm_default))
    dispatcher.add_handler(CommandHandler('vcenter_delete_vm_default',vcenter_delete_vm_default))    

    dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), echo))
    dispatcher.add_handler(MessageHandler(Filters.command,unknown))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
