#!/usr/bin/python

import boto.ec2
import datetime
import time
from time import mktime

signature = "_daily_ami_"
retention = 1 #in_minutes



key="AKIAJ5LCAFFF4UU3CGKQ"
secret="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"
r = boto.ec2.get_region('eu-central-1')
conn = boto.connect_ec2(key,secret,region=r)


reservations = conn.get_all_reservations(filters = {'tag:Backup':"daily", 'instance-state-name':'*'})
if ( len(reservations) == 0 ):
    print "ERROR"

else:
    print "Connected to AWS"

print "Script started at " + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + "\n"
# loop through reservations and instances
for reservation in reservations:
    for instance in reservation.instances:
        instance_name = instance.tags['Name']
        instance_id = instance.id
        current_datetime = datetime.datetime.now()
        date_stamp = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")
        status = instance.update()
        states=['running','stopping','stopped']
        try:
            if status in states:
                ami_name = instance_name + signature + date_stamp
                #description="daily ami of " + instance_name
                ami_id = instance.create_image(ami_name, description="Created by script", no_reboot=True, dry_run=False)
                print "\n"+ ami_name + " creation started"
        except Exception, e:
            raise e

        images = conn.get_all_images(image_ids = ami_id)
        image = images[0]
        image.add_tag("Name", ami_name)

        # Deregister of Ami's according to the retention period
        images = conn.get_all_images(filters = {'tag:Name':instance_name + signature + '*'})

        for image in images:
            image_name = image.tags['Name']
            image_stamp = image_name.replace(instance_name + signature, "")
            image_timestamp = mktime(time.strptime(image_stamp, "%Y-%m-%d_%H-%M-%S"))
            current_timestamp = mktime(current_datetime.timetuple())
            diff_minutes = (current_timestamp - image_timestamp) / 60

            if ( diff_minutes > retention ):
                print diff_minutes
                image.deregister(delete_snapshot=True, dry_run=False)
                print image_name + " will be deleted"

            else:
                print image_name + " will be kept"



# iteration finished
print "\nScript completed at " + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
