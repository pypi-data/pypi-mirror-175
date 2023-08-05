import asyncio
import aiohttp
import xmltodict
import re
import copy

DEVICE_DEFS = ['device_sn', 'prod_sn', 'device_name', 'device_type', 'eth_mac', 't', 'name', 'id', 'type', 'i']

async def get_devices(httpsession, wunda_ip, wunda_user, wunda_pass):
    """ Returns a list of active devices connected to the Wundasmart controller """

    devices = {}

    """ Query the getdevices API, which returns a list of all devices connected to the controller. Data is formatted in XML """
    wunda_url = f"http://{wunda_ip}/getdevices.cgi" 
    try: 
        resp = await httpsession.get(
            wunda_url, auth=aiohttp.BasicAuth(wunda_user, wunda_pass)
        )
        status = resp.status

        if status == 200:
            xml_data = await resp.text()
            xml_dict = xmltodict.parse(xml_data, attr_prefix='')["devices"]["dev"]
            for device in xml_dict:
                device_id = device["id"]
                devices[device_id] = { 
                                            "type" : device["type"],
                                            "id"   : f'{device["type"]}.{device["id"]}'
                                        }
                if "sn" in device: devices[device_id]["sn"] = device["sn"]
        else:
            return {"state": False, "code": status}
    except (asyncio.TimeoutError, aiohttp.ClientError):
        return {"state": False, "code": 500, "message": "HTTP client error"}

    """ Query the syncvalues API, which returns a list of all sensor values for all devices. Data is formatted as semicolon-separated k;v pairs """
    wunda_url = f"http://{wunda_ip}/syncvalues.cgi?v=2"
    try:
        resp = await httpsession.get(
            wunda_url, auth=aiohttp.BasicAuth(wunda_user, wunda_pass)
        )
        status = resp.status
        if status == 200:
            data = await resp.text()
            for device_state in data.splitlines():
                device_state_split = dict(x.split(":") for x in device_state.split(";") if ":" in x)
                device_id = str(device_state.split(";")[0])
                devices[device_id]["state"] = {}
                for device_state_key in device_state_split:
                    if device_state_key in DEVICE_DEFS:
                        devices[device_id][device_state_key] = device_state_split[device_state_key]
                    else:
                        devices[device_id]["state"][device_state_key] = device_state_split[device_state_key]
        else:
            return {"state": False, "code": status}
    except (asyncio.TimeoutError, aiohttp.ClientError):
        return {"state": False, "code": 500, "message": "HTTP client error"}

    """ Query the cmd API, which returns a list of rooms configured on the controller. Data is formatted in JSON """
    wunda_url = f"http://{wunda_ip}/cmd.cgi"
    try:
        resp = await httpsession.get(
            wunda_url, auth=aiohttp.BasicAuth(wunda_user, wunda_pass)
        )
        status = resp.status

        if status == 200:
            data = await resp.json()
            for room in data["rooms"]:
                for room_key in room:
                    room_id = str(room["i"])
                    if room_key == "t": devices[room_id]["state"]["room_temp"] = room[room_key]
                    if room_key in DEVICE_DEFS:
                        devices[room_id][room_key] = room[room_key]
                    else:
                        devices[room_id]["state"][room_key] = room[room_key]
        else:
            return {"state": False, "code": status}
    except (asyncio.TimeoutError, aiohttp.ClientError):
        return {"state": False, "code": 500}

    #devices_list = []

    #for device in devices:
    #    devices_list.append(devices[device])

    return {"state": True, "devices": devices}

async def put_state(httpsession, wunda_ip, wunda_user, wunda_pass, wunda_id, wunda_key, wunda_val):
    response = {}
    wunda_url = f"http://{wunda_ip}/setregister.cgi"
    try:
        params = f"{wunda_id}@{wunda_key}={wunda_val}"
        resp = await httpsession.get(
            wunda_url, auth=aiohttp.BasicAuth(wunda_user, wunda_pass), params=params
        )
        status = resp.status
        if status == 200:
            # the setregister.cgi API returns XML formatted response, e.g. <cmd status="ok"><device id="0"><reg vid="121" tid="temp_pre" v="1" status="ok"/></device></cmd>
            xml_data = await resp.text()
            xml_dict = xmltodict.parse(xml_data, attr_prefix='')
            if xml_dict["cmd"]["status"] == "ok":
                if xml_dict["cmd"]["device"]["reg"]["status"] == "ok":
                    response[xml_dict["cmd"]["device"]["reg"]["tid"]] = xml_dict["cmd"]["device"]["reg"]["v"]
                else:
                    return {"state": False, "code": 500, "message": xml_dict["cmd"]["device"]["reg"]["status"]}
            else:
                return {"state": False, "code": 500, "message": xml_dict["cmd"]["status"]}
        else:
            return {"state": False, "code": status}
    except (asyncio.TimeoutError, aiohttp.ClientError):
        return {"state": False, "code": 500, "message": "HTTP client error"}

    return {"state": True, "response": response}
