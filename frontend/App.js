import React, { useState, useEffect } from "react";
import axios from "axios";

function App() {
  const [vms, setVms] = useState([]);
  const [name, setName] = useState("");
  const [ram, setRam] = useState(1024);
  const [cpu, setCpu] = useState(1);
  const [disk, setDisk] = useState(10);

  const fetchVms = async () => {
    const res = await axios.get("http://localhost:5000/list");
    setVms(res.data);
  };

  const createVps = async () => {
    const res = await axios.post("http://localhost:5000/create", { name, ram, cpu, disk });
    alert(`VPS Created: ${res.data.name}\nRoot Password: ${res.data.root_password}`);
    fetchVms();
  };

  const deleteVps = async (name) => {
    await axios.post("http://localhost:5000/delete", { name });
    fetchVms();
  };

  useEffect(() => { fetchVms(); }, []);

  return (
    <div style={{ padding: "20px" }}>
      <h1>Mini Cloud VPS Panel</h1>
      <input placeholder="VPS Name" value={name} onChange={e=>setName(e.target.value)} />
      <input placeholder="RAM MB" value={ram} onChange={e=>setRam(e.target.value)} />
      <input placeholder="CPU" value={cpu} onChange={e=>setCpu(e.target.value)} />
      <input placeholder="Disk GB" value={disk} onChange={e=>setDisk(e.target.value)} />
      <button onClick={createVps}>Create VPS</button>

      <h2>Existing VPS</h2>
      <ul>
        {vms.map(v=>(
          <li key={v.name}>{v.name} <button onClick={()=>deleteVps(v.name)}>Delete</button></li>
        ))}
      </ul>
    </div>
  );
}

export default App;
