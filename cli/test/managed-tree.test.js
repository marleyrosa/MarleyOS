import test from "node:test";
import assert from "node:assert/strict";
import os from "node:os";
import path from "node:path";
import fse from "fs-extra";
import {
    applyUpdatePlan,
    createUpdatePlan,
    installFreshTree,
    listBackups,
    loadManifest,
    restoreBackup,
} from "../lib/managed-tree.js";

const makeTempProject = async (t) => {
    const root = await fse.mkdtemp(path.join(os.tmpdir(), "ag-kit-test-"));
    t.after(async () => fse.remove(root));
    return root;
};

const writeFiles = async (root, files) => {
    for (const [relativePath, content] of Object.entries(files)) {
        const destination = path.join(root, relativePath);
        await fse.ensureDir(path.dirname(destination));
        await fse.writeFile(destination, content, "utf8");
    }
};

test("fresh install writes a managed-file manifest", async (t) => {
    const projectDir = await makeTempProject(t);
    const incomingDir = path.join(projectDir, "incoming");
    const currentDir = path.join(projectDir, ".agents");
    await writeFiles(incomingDir, {
        "agent/orchestrator.md": "orchestrator-v1",
        "skills/example/SKILL.md": "skill-v1",
    });

    const report = await installFreshTree({
        projectDir,
        incomingDir,
        currentDir,
        toolkitVersion: "1.0.0",
        runId: "install-test",
    });

    assert.equal(report.strategy, "install");
    const manifest = await loadManifest(currentDir);
    assert.equal(manifest.toolkitVersion, "1.0.0");
    assert.deepEqual(Object.keys(manifest.files).sort(), [
        "agent/orchestrator.md",
        "skills/example/SKILL.md",
    ]);
});

test("merge updates clean files, preserves local files, and reports true conflicts", async (t) => {
    const projectDir = await makeTempProject(t);
    const incomingV1 = path.join(projectDir, "incoming-v1");
    const incomingV2 = path.join(projectDir, "incoming-v2");
    const currentDir = path.join(projectDir, ".agents");

    await writeFiles(incomingV1, {
        "a.txt": "a-v1",
        "b.txt": "b-v1",
        "obsolete.txt": "remove-me",
    });
    await installFreshTree({
        projectDir,
        incomingDir: incomingV1,
        currentDir,
        toolkitVersion: "1.0.0",
        runId: "v1",
    });

    await writeFiles(currentDir, {
        "b.txt": "b-local",
        "user-notes.md": "keep me",
    });
    await writeFiles(incomingV2, {
        "a.txt": "a-v2",
        "b.txt": "b-upstream",
        "new.txt": "new-file",
    });

    const manifest = await loadManifest(currentDir);
    const plan = await createUpdatePlan({
        currentDir,
        incomingDir: incomingV2,
        strategy: "merge",
        manifest,
    });

    assert.deepEqual(
        plan.actions.map((item) => [item.type, item.file]),
        [
            ["update", "a.txt"],
            ["add", "new.txt"],
            ["delete", "obsolete.txt"],
        ],
    );
    assert.deepEqual(plan.conflicts.map((item) => item.file), ["b.txt"]);
    assert.ok(plan.preserved.some((item) => item.file === "user-notes.md"));

    const report = await applyUpdatePlan({
        projectDir,
        currentDir,
        incomingDir: incomingV2,
        plan,
        toolkitVersion: "2.0.0",
        runId: "merge-test",
    });

    assert.equal(await fse.readFile(path.join(currentDir, "a.txt"), "utf8"), "a-v2");
    assert.equal(await fse.readFile(path.join(currentDir, "b.txt"), "utf8"), "b-local");
    assert.equal(await fse.readFile(path.join(currentDir, "new.txt"), "utf8"), "new-file");
    assert.equal(await fse.readFile(path.join(currentDir, "user-notes.md"), "utf8"), "keep me");
    assert.equal(await fse.pathExists(path.join(currentDir, "obsolete.txt")), false);
    assert.equal(
        await fse.readFile(
            path.join(currentDir, ".ag-kit", "conflicts", "merge-test", "b.txt.incoming"),
            "utf8",
        ),
        "b-upstream",
    );
    assert.equal(report.summary.conflicts, 1);
    assert.ok(await fse.pathExists(report.backupDir));
    assert.ok(await fse.pathExists(report.reportPath));

    const updatedManifest = await loadManifest(currentDir);
    assert.equal(updatedManifest.toolkitVersion, "2.0.0");
    assert.ok(updatedManifest.files["b.txt"]);
});

test("legacy installation never overwrites an existing differing file", async (t) => {
    const projectDir = await makeTempProject(t);
    const currentDir = path.join(projectDir, ".agents");
    const incomingDir = path.join(projectDir, "incoming");
    await writeFiles(currentDir, { "rules/local.md": "local-version" });
    await writeFiles(incomingDir, {
        "rules/local.md": "upstream-version",
        "rules/new.md": "new-rule",
    });

    const plan = await createUpdatePlan({
        currentDir,
        incomingDir,
        strategy: "merge",
        manifest: null,
    });

    assert.deepEqual(plan.conflicts.map((item) => item.file), ["rules/local.md"]);
    assert.deepEqual(plan.actions.map((item) => item.file), ["rules/new.md"]);

    await applyUpdatePlan({
        projectDir,
        currentDir,
        incomingDir,
        plan,
        toolkitVersion: "2.0.0",
        runId: "legacy-test",
    });

    assert.equal(
        await fse.readFile(path.join(currentDir, "rules/local.md"), "utf8"),
        "local-version",
    );
    assert.equal(
        await fse.readFile(path.join(currentDir, "rules/new.md"), "utf8"),
        "new-rule",
    );
});


test("malformed manifest paths are rejected before planning file operations", async (t) => {
    const projectDir = await makeTempProject(t);
    const currentDir = path.join(projectDir, ".agents");
    await writeFiles(currentDir, { "safe.txt": "safe" });
    await fse.ensureDir(path.join(currentDir, ".ag-kit"));
    await fse.writeJson(path.join(currentDir, ".ag-kit", "manifest.json"), {
        schemaVersion: 1,
        files: {
            "../../outside.txt": "0".repeat(64),
        },
    });

    assert.equal(await loadManifest(currentDir), null);
});

test("replace creates a backup that can be rolled back", async (t) => {
    const projectDir = await makeTempProject(t);
    const currentDir = path.join(projectDir, ".agents");
    const incomingDir = path.join(projectDir, "incoming");
    await writeFiles(currentDir, {
        "old.txt": "old",
        "local-only.txt": "local",
    });
    await writeFiles(incomingDir, { "new.txt": "new" });

    const plan = await createUpdatePlan({
        currentDir,
        incomingDir,
        strategy: "replace",
        manifest: null,
    });
    await applyUpdatePlan({
        projectDir,
        currentDir,
        incomingDir,
        plan,
        toolkitVersion: "2.0.0",
        runId: "replace-test",
    });

    assert.equal(await fse.pathExists(path.join(currentDir, "old.txt")), false);
    assert.equal(await fse.pathExists(path.join(currentDir, "local-only.txt")), false);
    assert.equal(await fse.readFile(path.join(currentDir, "new.txt"), "utf8"), "new");

    const backups = await listBackups(projectDir);
    assert.equal(backups[0].id, "replace-test");

    await restoreBackup({
        projectDir,
        agentDir: currentDir,
        backupId: "replace-test",
        keepCurrent: false,
        runId: "rollback-test",
    });

    assert.equal(await fse.readFile(path.join(currentDir, "old.txt"), "utf8"), "old");
    assert.equal(await fse.readFile(path.join(currentDir, "local-only.txt"), "utf8"), "local");
    assert.equal(await fse.pathExists(path.join(currentDir, "new.txt")), false);
});
