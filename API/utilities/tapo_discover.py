import asyncio
import logging
import json
from plugp100.common.credentials import AuthCredential
from plugp100.discovery.tapo_discovery import TapoDiscovery

async def example_discovery(credentials: AuthCredential):
    discovered = await TapoDiscovery.scan(timeout=30)
    devices = []
    errors = []
    for discovered_device in discovered:
        try:
            device = await discovered_device.get_tapo_device(credentials)
            await device.update()
            devices.append({
                'type': str(type(device)),
                'protocol': device.protocol_version,
                'raw_state': device.raw_state
            })
            await device.client.close()
        except Exception as e:
            error_message = {
                "message": f"Failed to update {discovered_device.ip} {discovered_device.device_type}",
                "error": str(e)
            }
            errors.append(error_message)
            logging.error(error_message, exc_info=e)

    output = {
        "discovered": len(discovered),
        "devices": devices,
        "errors": errors
    }
    print(json.dumps(output, indent=4))

async def main():
    credentials = AuthCredential("annnna6633@gmail.com", "a12345678")
    await example_discovery(credentials)

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
    loop.run_until_complete(asyncio.sleep(0.1))
    loop.close()