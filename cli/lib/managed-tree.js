import crypto from "node:crypto";
import path from "node:path";
import fse from "fs-extra";

export const MANIFEST_SCHEMA_VERSION = 1;
export const METADATA_DIR = ".ag-kit";
export const MANIFEST_FILE = path.join(METADATA_DIR, "manifest.json");
export const BACKUP_ROOT = ".ag-kit-backups";

const INTERNAL_PREFIXES = [
    `${METADATA_DIR}/`,
    ".git/",
    "node_modules/",
    ".next/",
];

const INTERNAL_FILES = new Set([".DS_Store"]);

const normalizeRelative = (value) => value.split(path.sep).join("/");

const isSafeRelativePath = (value) => {
    if (typeof value !== "string" || !value || value.includes("\0")) return false;
    const normalized = normalizeRelative(value);
    if (path.posix.isAbsolute(normalized) || path.win32.isAbsolute(value)) return false;
    const segments = normalized.split("/");
    return !segments.some((segment) => segment === ".." || segment === "");
};

const shouldIgnore = (relativePath) => {
    const normalized = normalizeRelative(relativePath);
    if (INTERNAL_FILES.has(path.posix.basename(normalized))) return true;
    return INTERNAL_PREFIXES.some((prefix) => normalized.startsWith(prefix));
};

export const createRunId = (date = new Date()) => {
    const pad = (value, size = 2) => String(value).padStart(size, "0");
    return [
        date.getUTCFullYear(),
        pad(date.getUTCMonth() + 1),
        pad(date.getUTCDate()),
        "-",
        pad(date.getUTCHours()),
        pad(date.getUTCMinutes()),
        pad(date.getUTCSeconds()),
        "-",
        pad(date.getUTCMilliseconds(), 3),
    ].join("");
};

export const hashFile = async (filePath) => {
    const hash = crypto.createHash("sha256");
    const data = await fse.readFile(filePath);
    hash.update(data);
    return hash.digest("hex");
};

export const snapshotTree = async (rootDir) => {
    const snapshot = {};

    if (!(await fse.pathExists(rootDir))) return snapshot;

    const visit = async (currentDir) => {
        const entries = await fse.readdir(currentDir, { withFileTypes: true });
        entries.sort((a, b) => a.name.localeCompare(b.name));

        for (const entry of entries) {
            const absolutePath = path.join(currentDir, entry.name);
            const relativePath = normalizeRelative(path.relative(rootDir, absolutePath));

            if (shouldIgnore(relativePath)) continue;

            if (entry.isDirectory()) {
                await visit(absolutePath);
            } else if (entry.isFile()) {
                snapshot[relativePath] = await hashFile(absolutePath);
            }
        }
    };

    await visit(rootDir);
    return snapshot;
};

export const loadManifest = async (agentDir) => {
    const manifestPath = path.join(agentDir, MANIFEST_FILE);
    if (!(await fse.pathExists(manifestPath))) return null;

    try {
        const manifest = await fse.readJson(manifestPath);
        if (
            manifest?.schemaVersion !== MANIFEST_SCHEMA_VERSION ||
            typeof manifest?.files !== "object" ||
            Array.isArray(manifest.files)
        ) {
            return null;
        }
        const entries = Object.entries(manifest.files);
        if (entries.some(([file, hash]) => !isSafeRelativePath(file) || !/^[0-9a-f]{64}$/.test(hash))) {
            return null;
        }
        return manifest;
    } catch {
        return null;
    }
};

export const writeManifest = async (
    agentDir,
    incomingSnapshot,
    { toolkitVersion = "unknown", previousManifest = null, runId = createRunId() } = {},
) => {
    const metadataDir = path.join(agentDir, METADATA_DIR);
    await fse.ensureDir(metadataDir);

    const now = new Date().toISOString();
    const manifest = {
        schemaVersion: MANIFEST_SCHEMA_VERSION,
        toolkitVersion,
        installedAt: previousManifest?.installedAt || now,
        updatedAt: now,
        lastRunId: runId,
        files: incomingSnapshot,
    };

    await fse.writeJson(path.join(agentDir, MANIFEST_FILE), manifest, { spaces: 2 });
    return manifest;
};

const action = (type, file, reason) => ({ type, file, reason });

export const createUpdatePlan = async ({
    currentDir,
    incomingDir,
    strategy = "merge",
    manifest = null,
}) => {
    if (!new Set(["merge", "replace"]).has(strategy)) {
        throw new Error(`Unsupported update strategy: ${strategy}`);
    }

    const current = await snapshotTree(currentDir);
    const incoming = await snapshotTree(incomingDir);
    const previous = manifest?.files || {};
    const hasManifest = Boolean(manifest);
    const allFiles = [...new Set([
        ...Object.keys(current),
        ...Object.keys(incoming),
        ...Object.keys(previous),
    ])].sort();

    const actions = [];
    const conflicts = [];
    const preserved = [];
    const unchanged = [];

    if (strategy === "replace") {
        for (const file of allFiles) {
            const currentHash = current[file];
            const incomingHash = incoming[file];

            if (incomingHash === undefined && currentHash !== undefined) {
                actions.push(action("delete", file, "not present in incoming toolkit"));
            } else if (incomingHash !== undefined && currentHash === undefined) {
                actions.push(action("add", file, "new incoming toolkit file"));
            } else if (incomingHash !== currentHash) {
                actions.push(action("update", file, "replace strategy"));
            } else {
                unchanged.push(file);
            }
        }

        return { strategy, current, incoming, previous, actions, conflicts, preserved, unchanged };
    }

    for (const file of allFiles) {
        const currentHash = current[file];
        const incomingHash = incoming[file];
        const oldHash = previous[file];
        const wasManaged = oldHash !== undefined;

        if (!hasManifest) {
            if (currentHash === undefined && incomingHash !== undefined) {
                actions.push(action("add", file, "new incoming file on legacy installation"));
            } else if (currentHash !== undefined && incomingHash === undefined) {
                preserved.push({ file, reason: "local-only file on legacy installation" });
            } else if (currentHash === incomingHash) {
                unchanged.push(file);
            } else {
                conflicts.push({
                    file,
                    reason: "legacy installation has no baseline and file differs from incoming",
                    currentHash,
                    incomingHash,
                    oldHash: null,
                });
            }
            continue;
        }

        if (!wasManaged) {
            if (currentHash === undefined && incomingHash !== undefined) {
                actions.push(action("add", file, "new upstream managed file"));
            } else if (currentHash !== undefined && incomingHash === undefined) {
                preserved.push({ file, reason: "user-owned file" });
            } else if (currentHash === incomingHash) {
                unchanged.push(file);
            } else {
                conflicts.push({
                    file,
                    reason: "user-owned file collides with new upstream file",
                    currentHash,
                    incomingHash,
                    oldHash: null,
                });
            }
            continue;
        }

        if (currentHash === undefined) {
            if (incomingHash === undefined) {
                unchanged.push(file);
            } else if (incomingHash === oldHash) {
                preserved.push({ file, reason: "locally deleted managed file" });
            } else {
                conflicts.push({
                    file,
                    reason: "file deleted locally and changed upstream",
                    currentHash: null,
                    incomingHash,
                    oldHash,
                });
            }
            continue;
        }

        if (incomingHash === undefined) {
            if (currentHash === oldHash) {
                actions.push(action("delete", file, "removed upstream and unchanged locally"));
            } else {
                conflicts.push({
                    file,
                    reason: "file changed locally but removed upstream",
                    currentHash,
                    incomingHash: null,
                    oldHash,
                });
            }
            continue;
        }

        if (currentHash === incomingHash) {
            unchanged.push(file);
        } else if (currentHash === oldHash) {
            actions.push(action("update", file, "changed upstream and unchanged locally"));
        } else if (incomingHash === oldHash) {
            preserved.push({ file, reason: "changed locally only" });
        } else {
            conflicts.push({
                file,
                reason: "changed both locally and upstream",
                currentHash,
                incomingHash,
                oldHash,
            });
        }
    }

    return { strategy, current, incoming, previous, actions, conflicts, preserved, unchanged };
};

export const createBackup = async ({ projectDir, agentDir, runId = createRunId() }) => {
    if (!(await fse.pathExists(agentDir))) return null;

    const backupDir = path.join(projectDir, BACKUP_ROOT, runId);
    await fse.ensureDir(backupDir);
    await fse.copy(agentDir, path.join(backupDir, ".agents"), {
        overwrite: true,
        errorOnExist: false,
    });
    await fse.writeJson(
        path.join(backupDir, "backup.json"),
        {
            schemaVersion: 1,
            createdAt: new Date().toISOString(),
            source: agentDir,
        },
        { spaces: 2 },
    );
    return backupDir;
};

const copyIncomingFile = async (incomingDir, currentDir, relativePath) => {
    const source = path.join(incomingDir, relativePath);
    const destination = path.join(currentDir, relativePath);
    await fse.ensureDir(path.dirname(destination));
    await fse.copyFile(source, destination);
};

const removeEmptyParents = async (filePath, stopDir) => {
    let current = path.dirname(filePath);
    const resolvedStop = path.resolve(stopDir);

    while (path.resolve(current).startsWith(`${resolvedStop}${path.sep}`)) {
        const entries = await fse.readdir(current);
        if (entries.length > 0) break;
        await fse.remove(current);
        current = path.dirname(current);
    }
};

export const applyUpdatePlan = async ({
    projectDir,
    currentDir,
    incomingDir,
    plan,
    toolkitVersion = "unknown",
    backup = true,
    runId = createRunId(),
    conflictReportPath = null,
}) => {
    const backupDir = backup
        ? await createBackup({ projectDir, agentDir: currentDir, runId })
        : null;

    for (const item of plan.actions) {
        const destination = path.join(currentDir, item.file);
        if (item.type === "delete") {
            await fse.remove(destination);
            await removeEmptyParents(destination, currentDir);
        } else {
            await copyIncomingFile(incomingDir, currentDir, item.file);
        }
    }

    const conflictRoot = path.join(currentDir, METADATA_DIR, "conflicts", runId);
    for (const conflict of plan.conflicts) {
        if (conflict.incomingHash) {
            const source = path.join(incomingDir, conflict.file);
            const destination = path.join(conflictRoot, `${conflict.file}.incoming`);
            await fse.ensureDir(path.dirname(destination));
            await fse.copyFile(source, destination);
        }
    }

    const report = {
        schemaVersion: 1,
        runId,
        strategy: plan.strategy,
        toolkitVersion,
        createdAt: new Date().toISOString(),
        backupDir,
        summary: {
            actions: plan.actions.length,
            conflicts: plan.conflicts.length,
            preserved: plan.preserved.length,
            unchanged: plan.unchanged.length,
        },
        actions: plan.actions,
        conflicts: plan.conflicts,
        preserved: plan.preserved,
    };

    const defaultReportPath = path.join(
        currentDir,
        METADATA_DIR,
        "reports",
        `update-${runId}.json`,
    );
    const resolvedReportPath = conflictReportPath
        ? path.resolve(projectDir, conflictReportPath)
        : defaultReportPath;
    await fse.ensureDir(path.dirname(resolvedReportPath));
    await fse.writeJson(resolvedReportPath, report, { spaces: 2 });

    const previousManifest = await loadManifest(currentDir);
    await writeManifest(currentDir, plan.incoming, {
        toolkitVersion,
        previousManifest,
        runId,
    });

    return { ...report, reportPath: resolvedReportPath };
};

export const installFreshTree = async ({
    projectDir,
    incomingDir,
    currentDir,
    toolkitVersion = "unknown",
    runId = createRunId(),
}) => {
    await fse.copy(incomingDir, currentDir, { overwrite: false, errorOnExist: true });
    const incomingSnapshot = await snapshotTree(incomingDir);
    await writeManifest(currentDir, incomingSnapshot, { toolkitVersion, runId });

    return {
        schemaVersion: 1,
        runId,
        strategy: "install",
        toolkitVersion,
        createdAt: new Date().toISOString(),
        backupDir: null,
        summary: {
            actions: Object.keys(incomingSnapshot).length,
            conflicts: 0,
            preserved: 0,
            unchanged: 0,
        },
        reportPath: null,
        projectDir,
    };
};

export const listBackups = async (projectDir) => {
    const root = path.join(projectDir, BACKUP_ROOT);
    if (!(await fse.pathExists(root))) return [];

    const entries = await fse.readdir(root, { withFileTypes: true });
    const backups = [];
    for (const entry of entries) {
        if (!entry.isDirectory()) continue;
        const backupPath = path.join(root, entry.name);
        let createdAt = "";
        try {
            const metadata = await fse.readJson(path.join(backupPath, "backup.json"));
            createdAt = metadata.createdAt || "";
        } catch {
            // Legacy backups without metadata fall back to their directory name.
        }
        backups.push({ id: entry.name, path: backupPath, createdAt });
    }

    return backups.sort((a, b) => {
        const dateOrder = b.createdAt.localeCompare(a.createdAt);
        return dateOrder || b.id.localeCompare(a.id);
    });
};

export const restoreBackup = async ({
    projectDir,
    agentDir,
    backupId = null,
    keepCurrent = true,
    runId = createRunId(),
}) => {
    const backups = await listBackups(projectDir);
    const selected = backupId
        ? backups.find((item) => item.id === backupId)
        : backups[0];

    if (!selected) {
        throw new Error(backupId ? `Backup not found: ${backupId}` : "No backups found");
    }

    const source = path.join(selected.path, ".agents");
    if (!(await fse.pathExists(source))) {
        throw new Error(`Backup is incomplete: ${selected.id}`);
    }

    let safetyBackupDir = null;
    if (keepCurrent && (await fse.pathExists(agentDir))) {
        safetyBackupDir = await createBackup({ projectDir, agentDir, runId: `pre-rollback-${runId}` });
    }

    await fse.remove(agentDir);
    await fse.copy(source, agentDir, { overwrite: true });

    return {
        restoredBackupId: selected.id,
        restoredFrom: source,
        safetyBackupDir,
    };
};
