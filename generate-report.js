const fs = require("fs");
const path = require("path");
const { execSync } = require("child_process");

// Fix Allure 3.x path issues on Windows (force POSIX forward slashes)
const pluginDist = path.join(__dirname, "node_modules", "@allurereport", "plugin-awesome", "dist");

if (process.platform === "win32" && fs.existsSync(pluginDist)) {
    const fixes = [
        {
            file: "plugin.js",
            from: 'import { join } from "node:path";',
            to:   'import { join } from "node:path/posix";',
        },
        {
            file: "generators.js",
            from: 'import { basename, join } from "node:path";',
            to:   'import { basename } from "node:path";\nimport { join } from "node:path/posix";',
        },
    ];

    for (const { file, from, to } of fixes) {
        const filePath = path.join(pluginDist, file);
        if (!fs.existsSync(filePath)) continue;

        const content = fs.readFileSync(filePath, "utf8");
        
        if (content.includes(from)) {
            fs.writeFileSync(filePath, content.replace(from, to), "utf8");
            console.log(`[fix] ${file} — patched.`);
        } else if (!content.includes(to)) {
            console.warn(`[fix] ${file} — target string not found.`);
        }
    }
}

// Clean up previous report
const reportDir = path.join(__dirname, "allure-report");
if (fs.existsSync(reportDir)) {
    fs.rmSync(reportDir, { recursive: true, force: true });
}

// Ensure results directory exists before generation
const resultsDir = path.join(__dirname, "allure-results");
if (!fs.existsSync(resultsDir)) {
    console.error("[report] Error: 'allure-results' directory not found. Run tests first.");
    process.exit(1);
}

// Generate new report
try {
    execSync("allure awesome ./allure-results -o allure-report --single-file --lang ru", {
        stdio: "inherit",
    });
} catch (error) {
    console.error("[report] Generation failed:", error.message);
    process.exit(1);
}
