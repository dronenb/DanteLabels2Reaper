#! /usr/bin/env python3
import os
import sys
import xml.etree.ElementTree as ET

def main():
	reaper_resource_path = os.path.expanduser("~/Library/Application Support/REAPER/")
	dante_file_location = os.path.expanduser(sys.argv[1])
	dante_filehandle = open(dante_file_location, "r")
	dante_file = dante_filehandle.read()
	root = ET.fromstring(dante_file)
	outfile_name = ''
	devices = {}
	for root_child in root:
		if root_child.tag == 'name':
			outfile_name = root_child.text
		if root_child.tag == 'device':
			device_name = ''
			for device in root_child:
				if device.tag == 'name':
					device_name = device.text
					devices[device_name] = {'inputs' : {}, 'outputs' : {}}
				if device.tag == 'txchannel' and device_name:
					txchannel_children = list(device)
					label = device.attrib['danteId']
					for txchannel_child in txchannel_children:
						if txchannel_child.tag == 'label':
							label = txchannel_child.text
							break
					devices[device_name]['outputs'][device.attrib['danteId']] = label
				if device.tag == 'rxchannel' and device_name:
					rxchannel_children = list(device)
					label = device.attrib['danteId']
					for rxchannel_child in rxchannel_children:
						if rxchannel_child.tag == 'name':
							label = rxchannel_child.text
							break
					devices[device_name]['inputs'][device.attrib['danteId']] = label
	selected_device = ''
	if len(devices.keys()) == 0:
		sys.stder.write("Did not find any devices in config file!")
		return(1)
	elif len(devices.keys()) == 1:
		selected_device = list(devices.keys())[0]
	else:
		device_keys = devices.keys()
		for i in range(0, len(device_keys)):
			print("%d) %s" % (i, device_keys[i]))
		selected_device = device_keys[input("Select device number from list above")]
	reaper_input_chanmap = "[reaper_chanmap]\n"
	reaper_output_chanmap = reaper_input_chanmap
	for channel in devices[selected_device]['inputs'].keys():
		reaper_input_chanmap = reaper_input_chanmap + "ch%d=%s\n" % (int(channel) - 1, int(channel) - 1)
	reaper_input_chanmap = reaper_input_chanmap + "map_hwnch=%d\n" % (len(devices[selected_device]['inputs'].keys()))
	reaper_input_chanmap = reaper_input_chanmap + "map_size=%d\n" % (len(devices[selected_device]['inputs'].keys()))
	for channel in devices[selected_device]['inputs'].keys():
		reaper_input_chanmap = reaper_input_chanmap + "name%d=%s\n" % (int(channel) - 1, str(devices[selected_device]['inputs'][channel]))
	for channel in devices[selected_device]['outputs'].keys():
		reaper_output_chanmap = reaper_output_chanmap + "ch%d=%s\n" % (int(channel) - 1, int(channel) - 1)
	reaper_output_chanmap = reaper_output_chanmap + "map_hwnch=%d\n" % (len(devices[selected_device]['outputs'].keys()))
	reaper_output_chanmap = reaper_output_chanmap + "map_size=%d\n" % (len(devices[selected_device]['outputs'].keys()))
	for channel in devices[selected_device]['outputs'].keys():
		reaper_output_chanmap = reaper_output_chanmap + "name%d=%s\n" % (int(channel) - 1, str(devices[selected_device]['outputs'][channel]))
	with open(reaper_resource_path + 'ChanMaps/' + outfile_name + '_inputs.ReaperChanMap', 'w') as filehandle:
		filehandle.write(reaper_input_chanmap)
	with open(reaper_resource_path + 'ChanMaps/' + outfile_name + '_outputs.ReaperChanMap', 'w') as filehandle:
		filehandle.write(reaper_output_chanmap)

if __name__ == "__main__":
	exit(main())
