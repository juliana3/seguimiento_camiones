"use client"


import {useEffect, useState} from "react"

export default function HomePage() {
  const[message, setMessage] = useState<string | null>(null);
  const[health, setHealth] = useState<string | null>(null);

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}`)
      .then((res) => res.json())
      .then((data) => setMessage(data.message))
      .catch(() => setMessage("Error al conectar con el Backend"))
  }, []);

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/health`)
      .then((res) => res.json())
      .then((data) => setHealth(data.status))
      .catch(() => setHealth("Error en el Healthcheck"))
  }, []);
  
  return (
    <main className="flex flex-col items-center justify-center min-h-screen py-8">
      <h1 className="text-3xl font-bold mb-4">Conexión del Frontend con el Backend</h1>

      <div className="space-y-3">
        <p>
          Mensaje del backend: <strong>{message || "Cargando..."}</strong>
        </p>
        <p>
          Estado de salud: <strong>{health || "Cargando..."}</strong>
        </p>
      </div>
    </main>
  );

}