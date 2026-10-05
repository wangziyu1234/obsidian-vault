/* QuickAdd user script: record one review without rewriting the rest of the card. */
"use strict";

const RESULTS = { wrong: "仍做不对", aided: "提示后做对", independent: "独立做对" };
const STAGES = ["次日", "第 3 天", "第 7 天", "第 30 天"];
const OFFSETS = [1, 3, 7, 30];
const REVIEW_HEADING = /^####\s+⏱\uFE0F?\s+复习记录\s*$/u;

function localDate(date = new Date()) {
    if (!(date instanceof Date) || Number.isNaN(date.getTime())) throw new Error("复习日期无效。");
    return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, "0")}-${String(date.getDate()).padStart(2, "0")}`;
}

function parseDate(value) {
    if (!/^\d{4}-\d{2}-\d{2}$/.test(value)) throw new Error(`日期格式无效：${value}`);
    const [year, month, day] = value.split("-").map(Number);
    const date = new Date(year, month - 1, day, 12);
    if (localDate(date) !== value) throw new Error(`日期不存在：${value}`);
    return date;
}

function addDays(value, days) {
    const date = parseDate(value);
    date.setDate(date.getDate() + days);
    return localDate(date);
}

function reviewSchedule(today) {
    return STAGES.map((stage, index) => ({ stage, due: addDays(today, OFFSETS[index]) }));
}

function lineSpans(text) {
    const lines = [];
    const pattern = /([^\r\n]*)(\r\n|\n|$)/g;
    let match;
    while ((match = pattern.exec(text)) && match[0]) {
        lines.push({ text: match[1], start: match.index, end: match.index + match[1].length, newline: match[2] });
    }
    return lines;
}

function parseCard(text) {
    const lines = lineSpans(text);
    if (!lines.length || lines[0].text.replace(/^\uFEFF/, "") !== "---") throw new Error("错题缺少 frontmatter。");
    const frontEnd = lines.findIndex((line, index) => index > 0 && line.text === "---");
    if (frontEnd < 0) throw new Error("错题 frontmatter 未闭合。");
    const field = (key) => {
        const matches = lines.slice(1, frontEnd).filter(line => new RegExp(`^${key}:`).test(line.text));
        if (matches.length !== 1) throw new Error(`错题属性 ${key} 必须且只能出现一次。`);
        const value = matches[0].text.slice(key.length + 1).split(/\s+#/)[0].trim().replace(/^(["'])(.*)\1$/, "$2");
        return { line: matches[0], value };
    };
    if (field("type").value !== "mistake") throw new Error("当前笔记不是 type: mistake 错题卡。");
    const mastery = field("mastery");
    if (!/^[0-3]$/.test(mastery.value)) throw new Error("mastery 必须是 0、1、2 或 3。");
    const modify = field("modify");
    if (lines.slice(1, frontEnd).some(line => /^review:/.test(line.text))) throw new Error("仍有旧 review 属性，请先完成错题格式迁移。");
    if (lines.slice(1, frontEnd).some(line => /^review-start:/.test(line.text))) throw new Error("仍有 review-start 属性，请先迁移为四轮复习任务。");
    // Examples in fenced code must not be mistaken for real headings or tasks.
    let fence = null;
    const visible = new Set();
    for (let index = frontEnd + 1; index < lines.length; index++) {
        const marker = /^ {0,3}(`{3,}|~{3,})(.*)$/.exec(lines[index].text);
        if (fence) {
            if (marker && marker[1][0] === fence[0] && marker[1].length >= fence.length && !marker[2].trim()) fence = null;
        } else if (marker) fence = marker[1];
        else visible.add(lines[index]);
    }
    const headings = lines.map((line, index) => visible.has(line) && REVIEW_HEADING.test(line.text) ? index : -1).filter(index => index > frontEnd);
    if (headings.length !== 1) throw new Error("错题必须且只能有一个「#### ⏱️ 复习记录」小节。");
    const start = headings[0] + 1;
    let end = lines.findIndex((line, index) => index >= start && visible.has(line) && /^#{1,4}\s/.test(line.text));
    if (end < 0) end = lines.length;
    const section = lines.slice(start, end).filter(line => visible.has(line));
    const pendingLines = section.filter(line => /^\s*[-*+]\s+\[ \]/.test(line.text));
    if (pendingLines.length > 4) throw new Error("复习待办最多保留次日、第 3、7、30 天四轮。");
    if (pendingLines.length && [0, 3].includes(Number(mastery.value))) throw new Error("挂起或已归档的错题不应有复习待办，请先核对掌握度与排期。");
    const pending = pendingLines.map(line => {
        const match = /^- \[ \] 错题复习（(次日|第\s*3\s*天|第\s*7\s*天|第\s*30\s*天)） 📅 (\d{4}-\d{2}-\d{2})\s*$/.exec(line.text);
        if (!match) throw new Error("复习待办格式无效；使用「- [ ] 错题复习（次日） 📅 YYYY-MM-DD」，不安排当天复习。");
        parseDate(match[2]);
        const stageIndex = STAGES.findIndex(stage => stage.replace(/\s/g, "") === match[1].replace(/\s/g, ""));
        return { line, stage: STAGES[stageIndex], stageIndex, due: match[2] };
    }).sort((a, b) => a.stageIndex - b.stageIndex);
    for (let index = 1; index < pending.length; index++) {
        if (pending[index].stageIndex === pending[index - 1].stageIndex) throw new Error("未完成复习任务的阶段不能重复。");
        if (pending[index].due <= pending[index - 1].due) throw new Error("未完成复习任务的日期须随阶段严格递增且不能重复。");
    }
    // Untagged old checkmarks have no reliable result and never prove mastery.
    const records = section.filter(line => /^- \[[xX]\]/.test(line.text)).map(line => {
        const marker = /<!-- review-result: (independent|aided|wrong) -->\s*$/.exec(line.text);
        const date = /✅ (\d{4}-\d{2}-\d{2})/.exec(line.text);
        if (date) parseDate(date[1]);
        return { result: marker && date ? marker[1] : null, date: date ? date[1] : null };
    });
    let insertAt = end < lines.length ? lines[end].start : text.length;
    for (let index = end - 1; index >= start && !lines[index].text.trim(); index--) insertAt = lines[index].start;
    const snapshot = section.find(line => /^>\s*\[!note\]-\s*旧复习计划/.test(line.text));
    let snapshotEnd = null;
    if (snapshot) {
        insertAt = snapshot.start;
        let index = lines.indexOf(snapshot);
        while (index < end && /^>/.test(lines[index].text)) {
            snapshotEnd = lines[index].end + lines[index].newline.length;
            index++;
        }
    }
    return { text, lines, mastery: Number(mastery.value), masteryLine: mastery.line, modifyLine: modify.line,
        pending, records, insertAt, snapshotEnd,
        newline: lines.find(line => line.newline)?.newline || "\n" };
}

function canArchive(card, result, today) {
    parseDate(today);
    const last = card.records.at(-1);
    return result === "independent" && last?.result === "independent" && last.date < today
        && !card.records.some(record => record.date >= today);
}

function planReview(card, { result, today, remark = "", archive = false, supplement = false }) {
    parseDate(today);
    if (!Object.hasOwn(RESULTS, result)) throw new Error("请选择有效的本次表现。");
    if (card.records.some(record => record.date > today)) throw new Error("复习历史中存在未来日期，请先核对设备日期与记录。");
    const sameDay = card.records.some(record => record.date === today);
    if (sameDay && !supplement) throw new Error("今天已有记录，请明确选择补记或取消。");
    if (archive && (sameDay || !canArchive(card, result, today))) throw new Error("归档需要不同日期连续两次明确记录独立做对。");
    if (typeof remark !== "string" || /[\r\n]/.test(remark)) throw new Error("复盘备注请写在一行内。");
    // Escape HTML delimiters so a remark cannot forge machine-readable result markers.
    const safeRemark = remark.trim().replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
    const restart = !archive && (result !== "independent" || [0, 3].includes(card.mastery));
    const removed = archive || restart ? card.pending : sameDay ? [] : card.pending.slice(0, 1);
    const added = restart ? reviewSchedule(today) : [];
    const pending = restart ? added : card.pending.filter(task => !removed.includes(task)).map(({ stage, due }) => ({ stage, due }));
    const next = pending[0]?.due ?? null;
    const completed = `- [x] 错题复盘 ✅ ${today} —— ${RESULTS[result]}${safeRemark ? `；${safeRemark}` : ""}${sameDay ? "（补记）" : ""} <!-- review-result: ${result} -->`;
    const mastery = archive ? 3 : result === "independent" ? 2 : 1;
    const propertyPatch = (line, value) => ({ start: line.start, end: line.end,
        value: line.text.replace(/^([^:]+:\s*)[^#]*?(\s+#.*)?$/, (_, prefix, comment) => `${prefix}${value}${comment || ""}`) });
    const patches = [propertyPatch(card.masteryLine, mastery), propertyPatch(card.modifyLine, today)];
    for (const task of removed) patches.push({ start: task.line.start, end: task.line.end + task.line.newline.length, value: "" });
    let beforeInsert = card.text.slice(0, card.insertAt);
    // Measure spacing after removals; the last old task can end at insertAt.
    for (const task of [...removed].sort((a, b) => b.line.start - a.line.start)) {
        const end = task.line.end + task.line.newline.length;
        if (end <= card.insertAt) beforeInsert = beforeInsert.slice(0, task.line.start) + beforeInsert.slice(end);
    }
    let prefix = beforeInsert && !beforeInsert.endsWith("\n") ? card.newline : "";
    let suffix = card.newline;
    if (card.snapshotEnd !== null) {
        if (beforeInsert && !(beforeInsert + prefix).endsWith(card.newline + card.newline)) prefix += card.newline;
        suffix += card.newline;
        const beforeEnd = card.text.slice(0, card.snapshotEnd);
        const afterEnd = card.text.slice(card.snapshotEnd);
        const separator = !beforeEnd.endsWith("\n") ? card.newline + card.newline : afterEnd.startsWith(card.newline) ? "" : card.newline;
        if (separator) patches.push({ start: card.snapshotEnd, end: card.snapshotEnd, value: separator });
    }
    const content = [completed, ...added.map(task => `- [ ] 错题复习（${task.stage}） 📅 ${task.due}`)].join(card.newline);
    patches.push({ start: card.insertAt, end: card.insertAt, value: prefix + content + suffix });
    let text = card.text;
    for (const patch of patches.sort((a, b) => b.start - a.start)) text = text.slice(0, patch.start) + patch.value + text.slice(patch.end);
    return { text, mastery, pending, next, result, today, supplement: sameDay };
}

async function runReview({ app, quickAddApi }, now = () => new Date()) {
    const file = app.workspace.getActiveFile();
    if (!file || file.extension !== "md" || !/^数学\/错题本\/.+\.md$/.test(file.path)) {
        throw new Error("请先打开「数学/错题本」中的一篇错题卡，再记录本次复习。");
    }
    const path = file.path;
    const original = await app.vault.read(file);
    const card = parseCard(original);
    const today = localDate(now());
    if (card.records.some(record => record.date > today)) throw new Error("复习历史中存在未来日期，请先核对设备日期与记录。");
    const sameDay = card.records.some(record => record.date === today);
    if (sameDay) {
        const action = await quickAddApi.suggester(["补记（独立做对保留待办；仍错或需提示则重新排四轮）", "取消"], ["supplement", "cancel"], `今天已记过 ${file.basename || path}`);
        if (action !== "supplement") return { status: "cancelled" };
    }
    const result = await quickAddApi.suggester(Object.values(RESULTS), Object.keys(RESULTS), `记录本次复习：${file.basename || path}`);
    if (result == null) return { status: "cancelled" };
    const remark = await quickAddApi.inputPrompt("一句复盘（可留空；取消则不保存本次记录）", "例如：仍漏初值；独立完成，用时 8 分钟", "", { optional: true });
    if (remark == null) return { status: "cancelled" };
    let archive = false;
    if (canArchive(card, result, today)) {
        const action = await quickAddApi.suggester(["继续复习，保留余下任务", "归档（不同日期已连续两次独立做对）", "取消本次记录"], ["continue", "archive", "cancel"], "已达到归档条件");
        if (action == null || action === "cancel") return { status: "cancelled" };
        archive = action === "archive";
    }
    const plan = planReview(card, { result, today, remark, archive, supplement: sameDay });
    if (localDate(now()) !== today) throw new Error("记录期间日期已改变，请重新运行，按新的实际日期记账。");
    // Vault.process serializes the check and write with concurrent vault updates.
    await app.vault.process(file, current => {
        if (file.path !== path || current !== original) throw new Error("错题在填写期间已被编辑或同步更新，本次没有写入；请重新运行。");
        return plan.text;
    });
    await quickAddApi.infoDialog("本次复盘已记录", plan.mastery === 3 ? "已归档；复习历史全部保留。" : plan.next ? `${RESULTS[result]}；下次复习：${plan.next}。做得没问题时直接勾选对应任务即可。` : `${RESULTS[result]}；当前已无待复习任务。`);
    return { status: "saved", ...plan };
}

module.exports = async params => runReview(params);
// Pure helpers and an injectable clock keep regression tests independent of Obsidian.
Object.assign(module.exports, { parseCard, planReview, canArchive, localDate, addDays, reviewSchedule, runReview });
