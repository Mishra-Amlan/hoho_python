// server/index.ts
import express from "express";
import { createProxyMiddleware } from "http-proxy-middleware";
import { spawn } from "child_process";
import { execSync } from "child_process";
import path from "path";
var app = express();
var PORT = process.env.PORT || 5e3;
console.log("\u{1F680} Hotel Audit System - Python Backend with Proxy");
console.log("==================================================");
try {
  console.log("\u{1F527} Cleaning up existing processes...");
  execSync('pkill -f "python.*main.py" || true', { stdio: "ignore" });
  execSync('pkill -f "uvicorn" || true', { stdio: "ignore" });
} catch (error) {
}
console.log("\u{1F40D} Starting Python FastAPI server...");
var pythonProcess = spawn("python", ["main.py"], {
  cwd: "python_backend",
  stdio: "pipe"
});
var pythonReady = false;
pythonProcess.stdout?.on("data", (data) => {
  const output = data.toString();
  console.log(output);
  if (output.includes("Uvicorn running")) {
    pythonReady = true;
    console.log("\u2705 Python backend is ready");
  }
});
pythonProcess.stderr?.on("data", (data) => {
  console.error("Python Error:", data.toString());
});
app.use(express.static(path.join(process.cwd(), "client")));
app.use("/api", createProxyMiddleware({
  target: "http://localhost:8000",
  changeOrigin: true,
  pathRewrite: {
    "^/api": "/api"
  },
  onError: (err, req, res) => {
    console.error("Proxy Error:", err.message);
    res.status(500).json({
      error: "Python backend not available",
      message: "Make sure Python FastAPI server is running on port 8000"
    });
  }
}));
app.get("*", (req, res) => {
  res.sendFile(path.join(process.cwd(), "client/index.html"));
});
app.listen(PORT, "0.0.0.0", () => {
  console.log(`\u{1F310} Proxy server running on http://0.0.0.0:${PORT}`);
  console.log(`\u{1F517} API proxying to Python backend on port 8000`);
  console.log(`\u{1F4CD} Frontend served from client/ directory`);
});
process.on("SIGINT", () => {
  console.log("\n\u{1F6D1} Shutting down...");
  pythonProcess.kill("SIGINT");
  process.exit(0);
});
process.on("SIGTERM", () => {
  pythonProcess.kill("SIGTERM");
  process.exit(0);
});
