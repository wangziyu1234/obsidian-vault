"use strict";
const test = require("node:test");
const assert = require("node:assert/strict");
const script = require("../../templates/scripts/review-mistake.js");
const { parseCard, planReview, canArchive, reviewSchedule, runReview } = script;

const pending = (stage = "次日", due = "2026-10-04") => `- [ ] 错题复习（${stage}） 📅 ${due}`;
const fourRounds = (today = "2026-10-01") => reviewSchedule(today).map(task => pending(task.stage, task.due)).join("\n");
const record = (date, result = "independent") => `- [x] 错题复盘 ✅ ${date} —— ${result} <!-- review-result: ${result} -->`;
function card({ mastery = 1, history = "", task = fourRounds(), newline = "\n", bom = "" } = {}) {
    return bom + ["---", "create: 2026-10-01", "modify: 2026-10-01 # 留下注释", "tags:", "  - 错题", "type: mistake", `mastery: ${mastery}`, "---", "", "# 一题", "", "$$\\frac{1}{x}+\\Phi_{\\mathrm{r}}x$$", "", "#### ⏱️ 复习记录", "", history, task.replace(/\r?\n/g, newline), "", "#### 其他内容", "", "正文原样保留。", ""].filter((line, index, array) => line !== "" || array[index - 1] !== "").join(newline);
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

test("可选独立记录完成最早一轮，余下排期逐行原样保留", () => {
    const result = plan(card());
    assert.equal(result.next, "2026-10-04");
    assert.equal(result.pending.length, 3);
    assert.match(result.text, /- \[x\] 错题复盘 ✅ 2026-10-05 —— 独立做对/);
    assert.doesNotMatch(result.text, /- \[ \] 错题复习（次日）/);
    for (const task of reviewSchedule("2026-10-01").slice(1)) assert.ok(result.text.includes(pending(task.stage, task.due)));
    assert.match(result.text, /modify: 2026-10-05 # 留下注释/);
    assert.equal(result.mastery, 2);
});
test("提前生成次日、第3、第7、第30天四轮，无当天任务", () => {
    assert.deepEqual(reviewSchedule("2026-10-05"), [
        { stage: "次日", due: "2026-10-06" }, { stage: "第 3 天", due: "2026-10-08" },
        { stage: "第 7 天", due: "2026-10-12" }, { stage: "第 30 天", due: "2026-11-04" }
    ]);
});
test("正常复习只需直接打勾，余下提醒自然保留，四轮勾完不自动归档", () => {
    let text = card();
    for (let count = 3; count >= 0; count--) {
        text = text.replace("- [ ] 错题复习", "- [x] 错题复习");
        const parsed = parseCard(text);
        assert.equal(parsed.pending.length, count);
        assert.equal(parsed.mastery, 1);
        assert.equal(parsed.records.length, 4 - count);
        assert.equal(canArchive(parsed, "independent", "2026-11-02"), false);
    }
});
test("仍错和提示后做对从实际日重排全部四轮，mastery 1，旧历史完整保留", () => {
    for (const result of ["wrong", "aided"]) {
        const history = "- [x] 2026-09-30 当天重做 —— 旧笔记原话";
        const output = plan(card({ mastery: 2, history }), { result });
        assert.equal(output.mastery, 1);
        assert.equal(output.next, "2026-10-06");
        assert.deepEqual(output.pending, reviewSchedule("2026-10-05"));
        assert.ok(output.text.includes(fourRounds("2026-10-05")));
        assert.ok(output.text.includes(history));
        assert.doesNotMatch(output.text, /📅 2026-10-02|📅 2026-10-04|📅 2026-10-31/);
        assert.equal(parseCard(output.text).pending.length, 4);
    }
});
test("真实旧计划快照前重排四轮，原快照不变且前后真空行，邻接删除不吞新行", () => {
    const snapshot = [
        "> [!note]- 旧复习计划（迁移留存）",
        "> 以下是旧排期快照；当前提醒以上方未勾选的复习任务为准，当天重做已取消。",
        "> 原未完成计划：",
        "> - 2026-10-01 当天重做",
        "> - 2026-10-02 次日",
        "> - 2026-10-04 第 3 天",
        "> - 2026-10-08 第 7 天",
        "> - 2026-10-31 第 30 天",
        "> 原属性中的日期：2026-10-01、2026-10-02、2026-10-04、2026-10-08、2026-10-31。"
    ].join("\n");
    for (const newline of ["\n", "\r\n"]) for (const gap of ["\n", "\n\n"]) {
        const history = "- [x] 2026-09-30 次日 ✅ 2026-10-01 —— 旧复盘原话";
        const source = card({ history }).replace("\n\n#### 其他内容", gap + snapshot + "\n#### 其他内容").replace(/\n/g, newline);
        const parsed = parseCard(source);
        assert.equal(parsed.insertAt, source.indexOf("> [!note]- 旧复习计划"));
        if (gap === "\n") {
            const last = parsed.pending.at(-1).line;
            assert.equal(last.end + last.newline.length, parsed.insertAt);
        }
        const result = plan(source, { result: "wrong" });
        const text = result.text.replace(/\r\n/g, "\n");
        assert.ok(result.text.includes(snapshot.replace(/\n/g, newline)));
        assert.ok(text.includes(fourRounds("2026-10-05") + "\n\n" + snapshot));
        assert.ok(text.includes(snapshot + "\n\n#### 其他内容"));
        assert.ok(text.includes(history));
        assert.equal(parseCard(result.text).pending.length, 4);
        assert.equal((text.match(/错题复盘 ✅ 2026-10-05/g) || []).length, 1);
        assert.equal(parseCard(result.text).records.at(-1).result, "wrong");
        assert.doesNotMatch(text.slice(text.indexOf(snapshot)), /- \[ \]/);
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
test("明确归档清除剩余待办并保留历史；未选择归档保留余下轮次", () => {
    const text = card({ history: record("2026-10-04") });
    const result = plan(text, { archive: true });
    assert.equal(result.mastery, 3);
    assert.equal(result.next, null);
    assert.ok(result.text.includes(record("2026-10-04")));
    assert.equal((result.text.match(/- \[ \]/g) || []).length, 0);
    assert.equal(plan(text).mastery, 2);
});
test("同日补记不连跳下一轮，失败可重排且同日不能归档", () => {
    const text = card({ history: record("2026-10-05") });
    assert.throws(() => plan(text), /明确选择补记/);
    const result = plan(text, { supplement: true });
    assert.equal(result.pending.length, 4);
    assert.equal(result.next, "2026-10-02");
    assert.match(result.text, /（补记）/);
    assert.equal(plan(text, { supplement: true, result: "aided" }).next, "2026-10-06");
    assert.throws(() => plan(text, { supplement: true, archive: true }), /归档需要/);
});
test("挂起和归档恢复时补四轮，活动错题允许0到4条待办", () => {
    for (const mastery of [0, 3]) {
        const result = plan(card({ mastery, task: "" }));
        assert.equal(result.mastery, 2);
        assert.equal(result.next, "2026-10-06");
        assert.equal(result.pending.length, 4);
    }
    for (const mastery of [0, 3]) assert.throws(() => parseCard(card({ mastery })), /不应有复习待办/);
    for (const mastery of [1, 2]) for (let count = 0; count <= 4; count++) {
        const tasks = reviewSchedule("2026-10-01").slice(0, count).map(task => pending(task.stage, task.due)).join("\n");
        assert.equal(parseCard(card({ mastery, task: tasks })).pending.length, count);
    }
});
test("四轮已勾完后补记独立结果不再自动增加任何任务", () => {
    const result = plan(card({ task: "" }));
    assert.equal(result.mastery, 2);
    assert.equal(result.next, null);
    assert.deepEqual(result.pending, []);
    assert.doesNotMatch(result.text, /- \[ \]/);
});
test("代码围栏中的标题、完成记录和待办均不参与解析", () => {
    for (const fence of ["```", "~~~~"]) {
        const example = `${fence}markdown\n#### ⏱️ 复习记录\n${pending()}\n${record("2026-10-07")}\n${fence}`;
        const text = card({ history: example });
        const result = plan(text);
        assert.ok(result.text.includes(example));
        assert.equal(parseCard(result.text).records.length, 1);
        assert.equal(result.next, "2026-10-04");
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
test("任务不得重复阶段、重复或逆序日期、超过四轮或安排当天", () => {
    assert.throws(() => parseCard(card({ task: `${pending()}\n${pending("次日", "2026-10-06")}` })), /阶段不能重复/);
    assert.throws(() => parseCard(card({ task: `${pending()}\n${pending("第 3 天")}` })), /日期须随阶段严格递增/);
    assert.throws(() => parseCard(card({ task: `${pending()}\n${pending("第 3 天", "2026-10-03")}` })), /日期须随阶段严格递增/);
    assert.throws(() => parseCard(card({ task: fourRounds() + "\n" + pending() })), /最多保留/);
    assert.throws(() => parseCard(card({ task: pending("当天") })), /不安排当天复习/);
    assert.throws(() => parseCard(card({ task: pending("次日", "2026-02-29") })), /日期不存在/);
    assert.throws(() => parseCard(card({ task: "- [ ] 2026-10-05 次日" })), /待办格式无效/);
});
test("错类型、旧 review 属性与多小节均安全拒绝", () => {
    assert.throws(() => parseCard(card().replace("type: mistake", "type: index")), /不是 type/);
    assert.throws(() => parseCard(card().replace("mastery: 1", "mastery: 1\nreview: []")), /旧 review/);
    assert.throws(() => parseCard(card().replace("mastery: 1", "mastery: 1\nreview-start: 2026-10-01")), /review-start 属性/);
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
test("交互中必须明确选择归档，否则保留余下轮次", async () => {
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
    assert.equal(result.next, "2026-10-02");
    assert.equal(mock.prompts.length, 3);
});
test("填写期间跨越午夜时不写入错误日期", async () => {
    const mock = fixture(); let calls = 0;
    await assert.rejects(runReview(mock.params, () => new Date(2026, 9, ++calls === 1 ? 5 : 6, 0)), /日期已改变/);
    assert.equal(mock.writes(), 0);
});
