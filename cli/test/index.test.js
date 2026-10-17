import test from "node:test";
import assert from "node:assert/strict";
import { buildProgram } from "../bin/index.js";

test("CLI exposes safe lifecycle commands", () => {
    const program = buildProgram();
    const commands = new Map(program.commands.map((command) => [command.name(), command]));

    assert.deepEqual([...commands.keys()], ["init", "update", "rollback", "status"]);
    assert.ok(commands.get("update").options.some((option) => option.long === "--strategy"));
    assert.ok(commands.get("update").options.some((option) => option.long === "--dry-run"));
    assert.ok(commands.get("rollback").options.some((option) => option.long === "--backup"));
});

test("CLI runs when invoked through an npm bin symlink", async (t) => {
    const { mkdtemp, mkdir, symlink, rm } = await import("node:fs/promises");
    const { tmpdir } = await import("node:os");
    const path = await import("node:path");
    const { execFile } = await import("node:child_process");
    const { promisify } = await import("node:util");
    const run = promisify(execFile);

    const dir = await mkdtemp(path.join(tmpdir(), "ag-kit-symlink-"));
    t.after(() => rm(dir, { recursive: true, force: true }));

    const binDir = path.join(dir, ".bin");
    await mkdir(binDir);
    const link = path.join(binDir, "ag-kit");
    await symlink(path.resolve("bin/index.js"), link);

    const { stdout } = await run(process.execPath, [link, "--version"]);
    assert.match(stdout.trim(), /^\d{4}\.\d+\.\d+$/);
});
