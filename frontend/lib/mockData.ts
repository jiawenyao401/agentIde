export const toolTrace = [
  { step: "analyze", tool: "filesystem.write", status: "done" },
  { step: "schema", tool: "filesystem.write", status: "done" },
  { step: "codegen", tool: "filesystem.write", status: "done" },
  { step: "tests", tool: "shell.run", status: "done" },
  { step: "pr", tool: "git.commit", status: "done" }
];
