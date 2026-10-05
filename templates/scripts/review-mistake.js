/* QuickAdd user script: record one review without rewriting the rest of the card. */
"use strict";

const STAGES = ["当天", "次日", "第 3 天", "第 7 天", "第 30 天"];
const INTERVALS = [1, 2, 4, 23, 30];
const RESULTS = { wrong: "仍做不对", aided: "提示后做对", independent: "独立做对" };
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
    if (pendingLines.length > 1) throw new Error("复习记录中有多条待办，请先整理为唯一一条下次复习任务。");
    if (pendingLines.length && [0, 3].includes(Number(mastery.value))) throw new Error("挂起或已归档的错题不应有复习待办，请先核对掌握度与排期。");
    if (!pendingLines.length && [1, 2].includes(Number(mastery.value))) throw new Error("未掌握或待复习的错题缺少下次复习任务，请先修复排期。");
    let pending = null;
    if (pendingLines.length) {
        const line = pendingLines[0];
        const match = /^- \[ \] 错题复习（(当天|次日|第\s*3\s*天|第\s*7\s*天|第\s*30\s*天)） 📅 (\d{4}-\d{2}-\d{2})\s*$/.exec(line.text);
        if (!match) throw new Error("复习待办格式不正确，请使用「- [ ] 错题复习（次日） 📅 YYYY-MM-DD」。");
        parseDate(match[2]);
        pending = { line, stage: STAGES.findIndex(stage => stage.replace(/\s/g, "") === match[1].replace(/\s/g, "")), due: match[2] };
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
    return { text, lines, mastery: Number(mastery.value), masteryLine: mastery.line, modifyLine: modify.line,
        pending, records, insertAt, newline: lines.find(line => line.newline)?.newline || "\n" };
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
    const stage = card.pending?.stage ?? 0;
    let next = null;
    if (!archive) {
        if (result !== "independent") next = { stage: 1, due: addDays(today, 1) };
        else if (sameDay && card.pending) next = { stage: card.pending.stage, due: card.pending.due };
        else next = { stage: Math.min(stage + 1, STAGES.length - 1), due: addDays(today, INTERVALS[stage]) };
    }
    const completed = `- [x] 错题复习（${STAGES[stage]}） ✅ ${today} —— ${RESULTS[result]}${safeRemark ? `；${safeRemark}` : ""}${sameDay ? "（补记）" : ""} <!-- review-result: ${result} -->`;
    const pending = next ? `- [ ] 错题复习（${STAGES[next.stage]}） 📅 ${next.due}` : null;
    const mastery = archive ? 3 : result === "independent" ? 2 : 1;
    const propertyPatch = (line, value) => ({ start: line.start, end: line.end,
        value: line.text.replace(/^([^:]+:\s*)[^#]*?(\s+#.*)?$/, (_, prefix, comment) => `${prefix}${value}${comment || ""}`) });
    const patches = [propertyPatch(card.masteryLine, mastery), propertyPatch(card.modifyLine, today)];
    const content = [completed, pending].filter(Boolean).join(card.newline);
    if (card.pending) patches.push({ start: card.pending.line.start, end: card.pending.line.end, value: content });
    else {
        const prefix = card.insertAt > 0 && !card.text.slice(0, card.insertAt).endsWith("\n") ? card.newline : "";
        patches.push({ start: card.insertAt, end: card.insertAt, value: prefix + content + card.newline });
    }
    let text = card.text;
    for (const patch of patches.sort((a, b) => b.start - a.start)) text = text.slice(0, patch.start) + patch.value + text.slice(patch.end);
    return { text, mastery, next, result, today, supplement: sameDay };
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
        const action = await quickAddApi.suggester(["补记（独立做对保留排期；仍错或需提示则改为明天）", "取消"], ["supplement", "cancel"], `今天已记过 ${file.basename || path}`);
        if (action !== "supplement") return { status: "cancelled" };
    }
    const result = await quickAddApi.suggester(Object.values(RESULTS), Object.keys(RESULTS), `记录本次复习：${file.basename || path}`);
    if (result == null) return { status: "cancelled" };
    const remark = await quickAddApi.inputPrompt("一句复盘（可留空；取消则不保存本次记录）", "例如：仍漏初值；独立完成，用时 8 分钟", "", { optional: true });
    if (remark == null) return { status: "cancelled" };
    let archive = false;
    if (canArchive(card, result, today)) {
        const action = await quickAddApi.suggester(["继续复习，保留下次排期", "归档（不同日期已连续两次独立做对）", "取消本次记录"], ["continue", "archive", "cancel"], "已达到归档条件");
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
    await quickAddApi.infoDialog("本次复习已记录", plan.next ? `${RESULTS[result]}；下次复习：${plan.next.due}（${STAGES[plan.next.stage]}）。` : "已归档；复习历史全部保留。");
    return { status: "saved", ...plan };
}

module.exports = async params => runReview(params);
// Pure helpers and an injectable clock keep regression tests independent of Obsidian.
Object.assign(module.exports, { parseCard, planReview, canArchive, localDate, addDays, runReview });
