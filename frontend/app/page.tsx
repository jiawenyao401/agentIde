"use client";

import { Panel } from "@/components/Panel";
import { toolTrace } from "@/lib/mockData";

const starterCode = `export const hello = () => "Agent Native IDE";`;

export default function HomePage() {
  return (
    <main style={{ padding: 16 }}>
      <h1>Agent Native AI Coding IDE</h1>
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "2fr 1fr",
          gap: 12,
          alignItems: "start"
        }}
      >
        <Panel title="Code Editor (secure fallback)">
          <textarea
            defaultValue={starterCode}
            style={{
              width: "100%",
              minHeight: "60vh",
              background: "#111827",
              color: "#e5e7eb",
              border: "1px solid #374151",
              borderRadius: 8,
              padding: 12,
              fontFamily: "ui-monospace, SFMono-Regular, Menlo, monospace",
              fontSize: 14
            }}
          />
        </Panel>

        <div style={{ display: "grid", gap: 12 }}>
          <Panel title="Chat 面板">
            <p>用户: 帮我做一个用户登录系统</p>
            <p>Agent: 已匹配 Skill build-rest-api，开始执行。</p>
          </Panel>

          <Panel title="Task Board">
            <ul>
              <li>1. 分析需求</li>
              <li>2. 设计数据库</li>
              <li>3. 生成API代码</li>
              <li>4. 编写测试</li>
              <li>5. 提交PR</li>
            </ul>
          </Panel>

          <Panel title="Tool Trace">
            <ul>
              {toolTrace.map((item) => (
                <li key={`${item.step}-${item.tool}`}>
                  {item.step} -&gt; {item.tool} ({item.status})
                </li>
              ))}
            </ul>
          </Panel>

          <Panel title="Memory 面板">
            <p>Episodic: 最近执行过登录系统任务。</p>
            <p>Semantic: 登录模块通常包含 JWT + refresh token。</p>
            <p>Personality: 偏好 FastAPI + pytest。</p>
          </Panel>
        </div>
      </div>
    </main>
  );
}
