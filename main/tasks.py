from email import message
import paramiko
import pm4py
import pandas as pd
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pm4py.algo.conformance.tokenreplay import algorithm as token_replay
from django.utils import timezone
from datetime import time
from celery import shared_task
from io import StringIO
from .models import ConformanceChecking, ConformanceCheckingDetail, StakeholderListDetail

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
    traces=[d['trace_is_fit'] for d in replayed_traces]
    indices = [i for i, x in enumerate(traces) if x == False]
    if indices:
        try:
            nodes=[(replayed_traces[i]['transitions_with_problems'][0].label) for i in indices]
        except:
            nodes=[]
            for var in indices:
                transitions=list(replayed_traces[var]['enabled_transitions_in_marking'])
                print(transitions)
                for var2 in transitions:
                    nodes.append(var2.label)
            print(nodes)
        nodes_detail=', '.join([str(elem) for elem in nodes])
        #Almacenamiento de detalle
        conformance_checking_detail=ConformanceCheckingDetail.objects.create(execution_time=timezone.now(),process=conformance_checking,status='Desviacion encontrada',node=nodes_detail)
        conformance_checking_detail.save()
        #Envio de correo
        #Inicializacion de objeto
        msg = MIMEMultipart()
        message='Error en el proceso {0} a la hora {1} en la actividad {2}'.format(process,timezone.now(),nodes_detail)
        recipients=list(StakeholderListDetail.objects.filter(list_name=conformance_checking.stakeholder_list))
        recipients_list=[i.stakeholder_name.email for i in recipients]
        #Configuracion de parametros
        print(recipients_list)
        password = "Upc12345"
        msg['From'] = "detprev2021218@gmail.com"
        msg['To'] = ", ".join(recipients_list)
        msg['Subject'] = "Anomalia detectada - DetPrev"
        # add in the message body
        msg.attach(MIMEText(message, 'plain'))
        #Encendido de server
        server = smtplib.SMTP('smtp.gmail.com: 587')
        server.starttls()
        # Login Credentials for sending the mail
        server.login(msg['From'], password)
        #Envio de mail
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        #Cierre de server
        server.quit()
    #Cierre de cliente
    else:
        #Almacenamiento de detalle
        conformance_checking_detail=ConformanceCheckingDetail.objects.create(execution_time=timezone.now(),process=conformance_checking,status='No se encontro desviaciones',node='No hubo errores')
        conformance_checking_detail.save()
    ssh.close()