import paramiko
import pm4py

import pandas as pd
from pm4py.algo.conformance.tokenreplay import algorithm as token_replay

from celery import shared_task
from io import StringIO
from .models import ConformanceChecking

@shared_task(name='conformance_cheking_task')
def conformance_cheking_task(conformance_checking_id):
    #Obtencion de objeto
    conformance_checking=ConformanceChecking.objects.get(id=conformance_checking_id)
    #Configurando llave
    pkey=paramiko.RSAKey.from_private_key(StringIO(conformance_checking.ssh_pub_key))
    #Configurando parametros
    user_ip=conformance_checking.user_ip
    os_user=conformance_checking.os_user
    log_file=conformance_checking.log_file
    process=conformance_checking.process.name
    username=conformance_checking.process.user
    #Apertura de cliente
    ssh=paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=user_ip,username=os_user,pkey=pkey)
    print('Connectado')
    #Lectura de archivo
    sftp_client = ssh.open_sftp()
    remote_file = sftp_client.open(log_file)
    remote_file.prefetch()
    event_log = pd.read_csv(remote_file,sep=';')
    print(event_log.columns)
    event_log = pm4py.format_dataframe(
        event_log, case_id='case_id', activity_key='activity', timestamp_key='timestamp')
    #Ejecucion Conformance Checking
    petri_net_model,initial_marking,final_marking=pm4py.read_petri_net('main/assets/{}/{}/process.ptn'.format(username, process))
    replayed_traces = token_replay.apply(event_log, petri_net_model, initial_marking, final_marking)
    #Cierre de cliente
    ssh.close()