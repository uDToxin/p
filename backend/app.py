from flask import Flask, request, jsonify
import libvirt, shutil, random, string, os

app = Flask(__name__)
conn = libvirt.open('qemu:///system')
TEMPLATE = os.path.join(os.path.dirname(__file__), "vps_templates/ubuntu22.qcow2")
VPS_DIR = "/var/lib/libvirt/images/"

def generate_password(length=12):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def create_vps(name, ram, cpu, disk):
    disk_path = os.path.join(VPS_DIR, f"{name}.qcow2")
    shutil.copy(TEMPLATE, disk_path)
    
    xml = f"""
    <domain type='kvm'>
      <name>{name}</name>
      <memory unit='MiB'>{ram}</memory>
      <vcpu>{cpu}</vcpu>
      <os><type arch='x86_64'>hvm</type></os>
      <devices>
        <disk type='file' device='disk'>
          <driver name='qemu' type='qcow2'/>
          <source file='{disk_path}'/>
          <target dev='vda' bus='virtio'/>
        </disk>
        <interface type='network'>
          <source network='default'/>
          <model type='virtio'/>
        </interface>
      </devices>
    </domain>
    """
    vm = conn.defineXML(xml)
    vm.create()
    root_pass = generate_password()
    return {"name": name, "root_password": root_pass}

@app.route("/create", methods=["POST"])
def api_create():
    data = request.json
    vps = create_vps(data['name'], data['ram'], data['cpu'], data['disk'])
    return jsonify(vps)

@app.route("/list", methods=["GET"])
def api_list():
    domains = conn.listAllDomains()
    vms = [{"name": d.name(), "id": d.ID()} for d in domains]
    return jsonify(vms)

@app.route("/delete", methods=["POST"])
def api_delete():
    data = request.json
    name = data.get("name")
    vm = conn.lookupByName(name)
    disk_path = os.path.join(VPS_DIR, f"{name}.qcow2")
    vm.destroy()
    vm.undefine()
    os.remove(disk_path)
    return jsonify({"deleted": name})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
