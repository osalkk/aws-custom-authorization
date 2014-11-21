#!/usr/bin/env python
import boto,boto.ec2,boto.ec2.autoscale

key="AKIAJA3HSJ2AV7OL7NKA"
secret="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"
conn = boto.ec2.connect_to_region("eu-west-1",aws_access_key_id=key,aws_secret_access_key=secret)
conn_as = boto.ec2.autoscale.connect_to_region("eu-west-1",aws_access_key_id=key,aws_secret_access_key=secret)


def get_demand_instance_list():
    print "#######################GET_DEMAND_INSTANCE_LIST()#######################################"        
    demand_inst_count=0
    group = conn_as.get_all_groups()
    if len(group)!=0:
        for gr in group:
            if gr.name=="Yemek_ASG_demand_v7_02092014":
                if len(gr.instances)>=0:
                    demand_inst_count=len(gr.instances)
                for inst in gr.instances:
                    reservations = conn.get_all_instances(instance_ids=[inst.instance_id])
                    instance = reservations[0].instances[0]
                    print instance
                    print instance.private_ip_address
                    print "-------------------------------------------"

if __name__ == "__main__":
    try:
        get_demand_instance_list()
    except:
        raise 
