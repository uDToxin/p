from pyrogram import Client, filters
import requests

api_id = 28452154
api_hash = "a14cc1a01dd79ada014d774332fd2285"
bot_token = "7891280232:AAF2Vvlokjxyh3oYJ03IQozrvOH_dVDx-MU"
API_URL = "http://localhost:5000"

app = Client("vpsbot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

@app.on_message(filters.command("create_vps"))
async def create(client, message):
    try:
        _, name, ram, cpu, disk = message.text.split()
        ram, cpu, disk = int(ram), int(cpu), int(disk)
        res = requests.post(f"{API_URL}/create", json={"name": name,"ram":ram,"cpu":cpu,"disk":disk})
        data = res.json()
        await message.reply(f"✅ VPS Created!\nName: {data['name']}\nRoot Password: {data['root_password']}")
    except Exception as e:
        await message.reply(f"❌ Error: {e}")

@app.on_message(filters.command("list_vps"))
async def list_vms(client, message):
    res = requests.get(f"{API_URL}/list")
    await message.reply(str(res.json()))

@app.on_message(filters.command("delete_vps"))
async def delete_vms(client, message):
    try:
        _, name = message.text.split()
        requests.post(f"{API_URL}/delete", json={"name": name})
        await message.reply(f"✅ VPS Deleted: {name}")
    except Exception as e:
        await message.reply(f"❌ Error: {e}")

app.run()
