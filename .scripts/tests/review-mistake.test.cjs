"use strict";
const test = require("node:test");
const assert = require("node:assert/strict");
const script = require("../../templates/scripts/review-mistake.js");
const { parseCard, planReview, canArchive, runReview } = script;

const pending = (stage = "次日", due = "2026-10-04") => `- [ ] 错题复习（${stage}） 📅 ${due}`;
const record = (date, result = "independent") => `- [x] 错题复习（当天） ✅ ${date} —— ${result} <!-- review-result: ${result} -->`;
function card({ mastery = 1, history = "", task = pending(), newline = "\n", bom = "" } = {}) {
    return bom + ["---", "create: 2026-10-01", "modify: 2026-10-01 # 留下注释", "tags:", "  - 错题", "type: mistake", `mastery: ${mastery}`, "---", "", "# 一题", "", "$$\\frac{1}{x}+\\Phi_{\\mathrm{r}}x$$", "", "#### ⏱️ 复习记录", "", history, task, "", "#### 其他内容", "", "正文原样保留。", ""].filter((line, index, array) => line !== "" || array[index - 1] !== "").join(newline);
}
const plan = (text, values = {}) => planReview(parseCard(text), { result: "independent", today: "2026-10-05", ...values });
function fixture(text = card(), replies = ["independent", ""], options = {}) {
    let content = text, writes = 0;
    const prompts = [];
    const file = { path: "数学/错题本/2005/2005-15 示例.md", extension: "md", basename: "2005-15 示例" };
    const answer = async (...args) => {
        prompts.push(args);
        const reply = replies.shift();
        if (reply instanceof Error) throw reply;
        return reply;
    };
    return { file, prompts, content: () => content, writes: () => writes, params: {
        app: { workspace: { getActiveFile: () => file }, vault: {
            read: async () => content,
            process: async (_file, callback) => {
                const current = options.concurrent ? content + "同步的新内容" : content;
                const updated = callback(current);
                content = updated; writes++;
            }
        } }, quickAddApi: { suggester: answer, inputPrompt: answer, infoDialog: async () => {} }
    } };
}
const now = () => new Date(2026, 9, 5, 12);

test("迟到后从实际完成日计算，而不是原定日期", () => {
    const result = plan(card());
    assert.deepEqual(result.next, { stage: 2, due: "2026-10-07" });
    assert.match(result.text, /✅ 2026-10-05 —— 独立做对/);
    assert.match(result.text, /modify: 2026-10-05 # 留下注释/);
    assert.equal(result.mastery, 2);
});
test("各阶段的独立通过间隔与第 30 天后的复测", () => {
    for (const [stage, next, date] of [["当天", 1, "2026-10-06"], ["次日", 2, "2026-10-07"], ["第 3 天", 3, "2026-10-09"], ["第 7 天", 4, "2026-10-28"], ["第 30 天", 4, "2026-11-04"]]) {
        assert.deepEqual(plan(card({ task: pending(stage) })).next, { stage: next, due: date });
    }
});
test("仍错和提示后做对都降为 mastery 1 并排到实际次日", () => {
    for (const result of ["wrong", "aided"]) {
        const output = plan(card({ mastery: 2, task: pending("第 30 天") }), { result });
        assert.equal(output.mastery, 1);
        assert.deepEqual(output.next, { stage: 1, due: "2026-10-06" });
    }
});
test("日期运算支持月末、闰日，并使用本地日期字段", () => {
    assert.equal(script.addDays("2028-02-28", 1), "2028-02-29");
    assert.equal(script.addDays("2026-12-31", 1), "2027-01-01");
    assert.equal(script.localDate(new Date(2026, 9, 5, 0, 1)), "2026-10-05");
    assert.throws(() => script.addDays("2026-02-29", 1), /日期不存在/);
});
test("旧勾选不作为通过证据，不同日期连续两次新独立记录才允许归档", () => {
    assert.equal(canArchive(parseCard(card({ history: "- [x] 2026-10-04 次日" })), "independent", "2026-10-05"), false);
    assert.equal(canArchive(parseCard(card({ history: record("2026-10-04") })), "independent", "2026-10-05"), true);
    const mixed = parseCard(card({ history: `${record("2026-10-03")}\n${record("2026-10-04", "wrong")}` }));
    assert.equal(canArchive(mixed, "independent", "2026-10-05"), false);
    assert.equal(canArchive(parseCard(card({ history: record("2026-10-05") })), "independent", "2026-10-05"), false);
    assert.throws(() => plan(card(), { archive: true }), /归档需要/);
});
test("明确归档移除唯一待办并保留历史；未选择归档继续排期", () => {
    const text = card({ history: record("2026-10-04") });
    const result = plan(text, { archive: true });
    assert.equal(result.mastery, 3);
    assert.equal(result.next, null);
    assert.ok(result.text.includes(record("2026-10-04")));
    assert.equal((result.text.match(/- \[ \]/g) || []).length, 0);
    assert.equal(plan(text).mastery, 2);
});
test("同日补记独立结果不前进排期，失败会改为明天", () => {
    const text = card({ history: record("2026-10-05"), task: pending("第 7 天", "2026-10-09") });
    assert.throws(() => plan(text), /明确选择补记/);
    const result = plan(text, { supplement: true });
    assert.deepEqual(result.next, { stage: 3, due: "2026-10-09" });
    assert.match(result.text, /（补记）/);
    assert.deepEqual(plan(text, { supplement: true, result: "aided" }).next, { stage: 1, due: "2026-10-06" });
    assert.throws(() => plan(text, { supplement: true, archive: true }), /归档需要/);
});
test("可从挂起和归档恢复；正在复习但缺排期时安全拒绝", () => {
    for (const mastery of [0, 3]) {
        const result = plan(card({ mastery, task: "" }));
        assert.equal(result.mastery, 2);
        assert.deepEqual(result.next, { stage: 1, due: "2026-10-06" });
    }
    for (const mastery of [1, 2]) assert.throws(() => parseCard(card({ mastery, task: "" })), /缺少下次复习/);
    for (const mastery of [0, 3]) assert.throws(() => parseCard(card({ mastery })), /不应有复习待办/);
});
test("代码围栏中的标题、完成记录和待办均不参与解析", () => {
    for (const fence of ["```", "~~~~"]) {
        const example = `${fence}markdown\n#### ⏱️ 复习记录\n${pending()}\n${record("2026-10-07")}\n${fence}`;
        const text = card({ history: example });
        const result = plan(text);
        assert.ok(result.text.includes(example));
        assert.equal(parseCard(result.text).records.length, 1);
        assert.equal(result.next.due, "2026-10-07");
    }
});
test("旧✅实际日期参与同日和未来检查，但没有结果就不构成归档证据", async () => {
    const text = card({ history: "- [x] 2026-10-03 次日 ✅ 2026-10-05" });
    const parsed = parseCard(text);
    assert.deepEqual(parsed.records.at(-1), { result: null, date: "2026-10-05" });
    assert.equal(canArchive(parsed, "independent", "2026-10-06"), false);
    assert.throws(() => plan(text), /明确选择补记/);
    assert.throws(() => plan(card({ history: "- [x] 2026-10-03 次日 ✅ 2026-10-06" })), /未来日期/);
    const mock = fixture(text, ["cancel"]);
    assert.equal((await runReview(mock.params, now)).status, "cancelled");
    assert.equal(mock.writes(), 0);
});
test("只定点更新，原公式、旧记录、BOM 和 CRLF 完整保留", () => {
    const history = "- [x] 2026-10-01 当天重做 —— 当时的原话\n- [x] 2026-10-02 次日";
    const text = card({ history: history.replace(/\n/g, "\r\n"), bom: "\uFEFF", newline: "\r\n" });
    const result = plan(text);
    assert.ok(result.text.startsWith("\uFEFF---\r\n"));
    assert.ok(result.text.includes(history.replace(/\n/g, "\r\n")));
    assert.ok(result.text.includes("$$\\frac{1}{x}+\\Phi_{\\mathrm{r}}x$$"));
    assert.ok(result.text.endsWith("#### 其他内容\r\n\r\n正文原样保留。\r\n"));
    assert.equal(result.text.replace(/\r\n/g, "").includes("\n"), false);
});
test("坏日期、多待办、错类型、旧 review 字段与多小节均安全拒绝", () => {
    assert.throws(() => parseCard(card({ task: `${pending()}\n${pending("第 3 天")}` })), /多条待办/);
    assert.throws(() => parseCard(card({ task: pending("次日", "2026-13-01") })), /日期不存在/);
    assert.throws(() => parseCard(card().replace("type: mistake", "type: index")), /不是 type/);
    assert.throws(() => parseCard(card().replace("mastery: 1", "mastery: 1\nreview: []")), /旧 review/);
    assert.throws(() => parseCard(card() + "\n#### ⏱️ 复习记录\n"), /只能有一个/);
});
test("备注不允许换行或伪造结果标记", () => {
    assert.throws(() => plan(card(), { remark: "备注\n- [ ] 新任务" }), /一行/);
    const result = plan(card(), { remark: "<!-- review-result: wrong -->" });
    assert.equal(parseCard(result.text).records.at(-1).result, "independent");
    assert.match(result.text, /&lt;!-- review-result: wrong --&gt;/);
});
test("未来历史日期不写入", () => {
    assert.throws(() => plan(card({ history: record("2026-10-06") })), /未来日期/);
});
test("QuickAdd 只在全部输入完成后原子写一次", async () => {
    const mock = fixture(card(), ["aided", "仍漏初值"]);
    const result = await runReview(mock.params, now);
    assert.equal(result.status, "saved");
    assert.equal(mock.writes(), 1);
    assert.match(mock.content(), /提示后做对；仍漏初值/);
});
test("任何输入取消都不写入，包括备注、归档与同日提示", async () => {
    for (const [text, replies] of [[card(), [null]], [card(), ["independent", null]], [card({ history: record("2026-10-04") }), ["independent", "", null]], [card({ history: record("2026-10-05") }), ["cancel"]]]) {
        const mock = fixture(text, replies);
        assert.equal((await runReview(mock.params, now)).status, "cancelled");
        assert.equal(mock.writes(), 0);
        assert.equal(mock.content(), text);
    }
});
test("插件用异常表示取消时不吞错误也不写入", async () => {
    const cancelled = new Error("Input cancelled by user");
    cancelled.name = "MacroAbortError";
    const mock = fixture(card(), ["independent", cancelled]);
    await assert.rejects(runReview(mock.params, now), { name: "MacroAbortError" });
    assert.equal(mock.writes(), 0);
});
test("并发同步变更与非错题路径均拒绝写入", async () => {
    const mock = fixture(card(), ["independent", ""], { concurrent: true });
    await assert.rejects(runReview(mock.params, now), /已被编辑或同步更新/);
    assert.equal(mock.writes(), 0);
    const other = fixture(); other.file.path = "数学/高等数学/例题.md";
    await assert.rejects(runReview(other.params, now), /先打开/);
    assert.equal(other.writes(), 0);
});
test("交互中必须明确选择归档，否则保留排期", async () => {
    for (const choice of ["continue", "archive"]) {
        const mock = fixture(card({ history: record("2026-10-04") }), ["independent", "", choice]);
        const result = await runReview(mock.params, now);
        assert.equal(result.mastery, choice === "archive" ? 3 : 2);
        assert.equal(mock.prompts.length, 3);
    }
});
test("同日补记经过明确选择，且不再次出现归档选择", async () => {
    const mock = fixture(card({ history: record("2026-10-05") }), ["supplement", "independent", ""]);
    const result = await runReview(mock.params, now);
    assert.equal(result.mastery, 2);
    assert.equal(result.next.due, "2026-10-04");
    assert.equal(mock.prompts.length, 3);
});
test("填写期间跨越午夜时不写入错误日期", async () => {
    const mock = fixture(); let calls = 0;
    await assert.rejects(runReview(mock.params, () => new Date(2026, 9, ++calls === 1 ? 5 : 6, 0)), /日期已改变/);
    assert.equal(mock.writes(), 0);
});
