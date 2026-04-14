import React from "react";

export function Panel({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <section style={{ border: "1px solid #374151", borderRadius: 12, padding: 12, background: "#1f2937" }}>
      <h3 style={{ marginTop: 0 }}>{title}</h3>
      {children}
    </section>
  );
}
