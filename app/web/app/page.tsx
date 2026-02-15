"use client";

import { useCallback, useEffect, useMemo, useState } from "react";

type StatusPayload = {
  up: boolean;
  latency_ms: number;
};

type VersionPayload = {
  commit: string;
  build_time: string;
  environment: string;
};

const POLL_INTERVAL_MS = 5000;
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "";

async function fetchJson<T>(path: string): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, { cache: "no-store" });
  if (!response.ok) {
    throw new Error(`Request failed: ${path} (${response.status})`);
  }
  return (await response.json()) as T;
}

function Card({
  title,
  value,
  valueClassName = "",
  subtitle
}: {
  title: string;
  value: string;
  valueClassName?: string;
  subtitle?: string;
}) {
  return (
    <div className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
      <p className="text-sm text-slate-500">{title}</p>
      <p className={`mt-2 text-2xl font-semibold ${valueClassName}`}>{value}</p>
      {subtitle ? <p className="mt-2 text-xs text-slate-500">{subtitle}</p> : null}
    </div>
  );
}

export default function Home() {
  const [status, setStatus] = useState<StatusPayload | null>(null);
  const [version, setVersion] = useState<VersionPayload | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [lastUpdate, setLastUpdate] = useState<string | null>(null);

  const loadData = useCallback(async () => {
    try {
      const [statusPayload, versionPayload] = await Promise.all([
        fetchJson<StatusPayload>("/api/status"),
        fetchJson<VersionPayload>("/api/version")
      ]);
      setStatus(statusPayload);
      setVersion(versionPayload);
      setLastUpdate(new Date().toLocaleTimeString());
      setError(null);
    } catch (requestError) {
      const message =
        requestError instanceof Error ? requestError.message : "Unknown request error";
      setError(message);
      setStatus(null);
      setVersion(null);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    void loadData();
    const interval = window.setInterval(() => {
      void loadData();
    }, POLL_INTERVAL_MS);

    return () => {
      window.clearInterval(interval);
    };
  }, [loadData]);

  const statusLabel = status?.up ? "UP" : "DOWN";
  const statusColor = useMemo(
    () => (status?.up ? "text-emerald-600" : "text-rose-600"),
    [status?.up]
  );

  return (
    <main className="flex min-h-screen items-center justify-center p-6">
      <section className="w-full max-w-3xl rounded-2xl border border-slate-200 bg-slate-50/70 p-6 shadow-lg backdrop-blur">
        <header className="mb-6 text-center">
          <h1 className="text-3xl font-bold text-slate-900">Observability Dashboard</h1>
          <p className="mt-2 text-sm text-slate-600">
            Auto-refresh cada 5 segundos desde /api/status y /api/version
          </p>
          {lastUpdate ? (
            <p className="mt-1 text-xs text-slate-500">Ultima actualizacion: {lastUpdate}</p>
          ) : null}
        </header>

        {isLoading ? (
          <p className="mb-4 text-center text-sm text-slate-600">Cargando datos...</p>
        ) : null}

        {error ? (
          <p className="mb-4 rounded-lg border border-rose-200 bg-rose-50 p-3 text-center text-sm text-rose-700">
            Error consultando API: {error}
          </p>
        ) : null}

        <div className="grid gap-4 md:grid-cols-2">
          <Card title="Status" value={statusLabel} valueClassName={statusColor} />
          <Card
            title="Latency"
            value={status ? `${status.latency_ms} ms` : "--"}
            valueClassName="text-slate-900"
          />
          <Card
            title="Commit SHA"
            value={version?.commit ?? "--"}
            valueClassName="text-slate-900"
          />
          <Card
            title="Build time"
            value={version?.build_time ?? "--"}
            valueClassName="text-slate-900"
            subtitle={version ? `Environment: ${version.environment}` : undefined}
          />
        </div>
      </section>
    </main>
  );
}
