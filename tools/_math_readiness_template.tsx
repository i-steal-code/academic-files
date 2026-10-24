import {
  BarChart,
  Button,
  Callout,
  Card,
  CardBody,
  CardHeader,
  Checkbox,
  Divider,
  Grid,
  H1,
  H2,
  H3,
  LineChart,
  Pill,
  Row,
  Select,
  Spacer,
  Stack,
  Stat,
  Table,
  Text,
  Toggle,
  useCanvasState,
  useHostTheme,
} from "cursor/canvas";

type Pillar = "Pure" | "Statistics";

type Topic = {
  id: string;
  name: string;
  short: string;
  pillar: Pillar;
  weight: number;
  marksAvg: number;
  p1: number;
  p2a: number;
  p2b: number;
  yearsTested: number;
  nYears: number;
  minMarks: number;
  maxMarks: number;
  nt: number;
  ntRaw: number;
  ntMarks: number;
  totalMarks: number;
  ntTypes: Record<string, number>;
  ntExamples: string[];
};

type ItemStatus = "ready" | "noSoln" | "partial" | "missing";

type Item = {
  key: string;
  topicId: string;
  tier: "core" | "stretch";
  n: number;
  ref: string;
  marks: string;
  stem: string;
  status: ItemStatus;
  flags: string[];
  note: string;
};

type Acquire = {
  doc: string;
  kind: "questions" | "solutions" | "hardcopy" | "scan" | "timed";
  priority: "core" | "stretch";
  blocks: string[];
  note: string;
};

type Data = {
  topics: Topic[];
  years: string[];
  yearMarks: Record<string, number[]>;
  items: Item[];
  acquire: Acquire[];
  meta: {
    papers: number;
    taggedMarks: number;
    oosMarks: number;
    ntGlobal: number;
    shrinkK: number;
    worksheetDir: string;
  };
};

const DATA: Data = __DATA__;

type Section = "Readiness" | "Weightage" | "Topical" | "Acquire" | "Outlook";
type SeverityKey = "brutal" | "strict" | "linear";

/**
 * Share of a topic's marks secured at each confidence level, split into routine marks
 * and non-trivial marks (novel set-up, insight step, rigour, explanation, hidden hence).
 * Linear mirrors the physics sheet (20% floor, straight line to 100%) for comparison.
 */
const SEVERITY: Record<SeverityKey, { label: string; routine: number[]; hard: number[] }> = {
  brutal: {
    label: "Brutal (default)",
    routine: [0, 0.1, 0.35, 0.8, 0.97],
    hard: [0, 0, 0.05, 0.25, 0.55],
  },
  strict: {
    label: "Strict",
    routine: [0, 0.15, 0.45, 0.85, 0.97],
    hard: [0, 0, 0.1, 0.3, 0.6],
  },
  linear: {
    label: "Linear (physics-style, comparison only)",
    routine: [0.2, 0.4, 0.6, 0.8, 1],
    hard: [0.2, 0.4, 0.6, 0.8, 1],
  },
};

const CONF_LEVELS = [
  { v: 0, label: "Not started, or cannot start a standard question" },
  { v: 1, label: "Recognise the question type; cannot finish it" },
  { v: 2, label: "Can finish standard questions with notes or a worked example open" },
  { v: 3, label: "Can finish standard questions unaided and timed" },
  { v: 4, label: "Can finish unseen variants and most twists unaided" },
];

const GRADE_LINES = [
  { value: 70, label: "A (indicative)", tone: "success" as const },
  { value: 55, label: "C (indicative)", tone: "warning" as const },
  { value: 40, label: "E (indicative)", tone: "danger" as const },
];

const FLAG_LABEL: Record<string, string> = {
  reserved: "Uses a sealed RI paper",
  spent: "Already seen (RI 2024 P2)",
  skip: "Skip some parts",
  check: "Printed answer has an error",
};

function realised(t: Topic, level: number, sev: SeverityKey): number {
  const s = SEVERITY[sev];
  const L = Math.max(0, Math.min(4, Math.round(level)));
  return (1 - t.nt) * s.routine[L] + t.nt * s.hard[L];
}

function indicativeGrade(pct: number): string {
  if (pct >= 70) return "A";
  if (pct >= 60) return "B";
  if (pct >= 55) return "C";
  if (pct >= 50) return "D";
  if (pct >= 40) return "E";
  return "U";
}

function stdev(xs: number[]): number {
  const m = xs.reduce((a, b) => a + b, 0) / xs.length;
  return Math.sqrt(xs.reduce((a, x) => a + (x - m) ** 2, 0) / xs.length);
}

function defaultRatings(): Record<string, number> {
  return Object.fromEntries(DATA.topics.map((t) => [t.id, 0]));
}

function useModel() {
  const [ratingsRaw, setRatings] = useCanvasState<Record<string, number>>("ratings", defaultRatings());
  const [sevRaw, setSev] = useCanvasState<string>("severity", "brutal");
  const [done, setDone] = useCanvasState<Record<string, boolean>>("done", {});
  const sev: SeverityKey = sevRaw === "strict" || sevRaw === "linear" ? sevRaw : "brutal";
  const ratings = { ...defaultRatings(), ...(ratingsRaw ?? {}) };

  const setRating = (id: string, level: number) =>
    setRatings((prev) => ({ ...defaultRatings(), ...(prev ?? {}), [id]: level }));
  const toggleDone = (key: string, v: boolean) => setDone((prev) => ({ ...(prev ?? {}), [key]: v }));

  const perTopic = DATA.topics.map((t) => {
    const level = ratings[t.id] ?? 0;
    const r = realised(t, level, sev);
    const cap = realised(t, 4, sev);
    const core = DATA.items.filter((i) => i.topicId === t.id && i.tier === "core");
    const coreDone = core.filter((i) => done[i.key]).length;
    return {
      ...t,
      level,
      realised: r,
      cap,
      marks: 2 * t.weight * r,
      capMarks: 2 * t.weight * cap,
      coreTotal: core.length,
      coreDone,
    };
  });

  const expectedPct = perTopic.reduce((a, t) => a + t.weight * t.realised, 0);
  const ceilingPct = perTopic.reduce((a, t) => a + t.weight * t.cap, 0);
  const atThree = perTopic.reduce((a, t) => a + (t.level >= 3 ? t.weight : 0), 0);
  const leaks = [...perTopic]
    .map((t) => ({ ...t, leak: 2 * t.weight * (t.cap - t.realised) }))
    .sort((a, b) => b.leak - a.leak);

  const realisedById = Object.fromEntries(perTopic.map((t) => [t.id, t.realised]));
  const yearProjection = DATA.years.map((_, yi) =>
    DATA.topics.reduce((a, t) => a + (DATA.yearMarks[t.id]?.[yi] ?? 0) * realisedById[t.id], 0) / 2,
  );

  return {
    ratings,
    setRating,
    resetRatings: () => setRatings(defaultRatings()),
    sev,
    setSev,
    done,
    toggleDone,
    perTopic,
    expectedPct,
    ceilingPct,
    atThree,
    leaks,
    yearProjection,
  };
}

function HeaderStats() {
  const { expectedPct, ceilingPct, atThree, leaks, sev } = useModel();
  const top = leaks[0];
  return (
    <Stack gap={10}>
      <Stack gap={6}>
        <H1>H2 Mathematics readiness</H1>
        <Text tone="secondary">
          Expected-mark model for the 200-mark A-level (Paper 1 pure, Paper 2 Section A pure, Paper 2
          Section B statistics). Topic weights come from every in-syllabus mark on the 2017–2025
          A-level papers. There is no memory-decay term: rate what you can do today. Model:{" "}
          {SEVERITY[sev].label}.
        </Text>
      </Stack>
      <Grid columns={4} gap={16}>
        <Stat
          value={`${(2 * expectedPct).toFixed(0)} / 200`}
          label={`Expected mark · ${expectedPct.toFixed(0)}% · grade ${indicativeGrade(expectedPct)} (indicative)`}
          tone={expectedPct >= 70 ? "success" : expectedPct >= 55 ? "warning" : "danger"}
        />
        <Stat value={`${ceilingPct.toFixed(0)}%`} label="Ceiling if every topic is at level 4" tone="info" />
        <Stat value={`${atThree.toFixed(0)}%`} label="Share of paper weight rated 3 or higher" />
        <Stat
          value={top && top.leak > 0.05 ? `${top.leak.toFixed(1)} marks` : "none"}
          label={top && top.leak > 0.05 ? `Biggest leak: ${top.name}` : "Biggest leak"}
          tone={top && top.leak > 5 ? "warning" : undefined}
        />
      </Grid>
    </Stack>
  );
}

function SectionNav({ section, setSection }: { section: Section; setSection: (s: Section) => void }) {
  return (
    <Row gap={8} wrap>
      {(["Readiness", "Weightage", "Topical", "Acquire", "Outlook"] as Section[]).map((s) => (
        <span key={s}>
          <Pill active={section === s} onClick={() => setSection(s)}>
            {s}
          </Pill>
        </span>
      ))}
    </Row>
  );
}

function ReadinessSection() {
  const theme = useHostTheme();
  const { setRating, resetRatings, sev, setSev, perTopic, expectedPct } = useModel();
  const pillars: Pillar[] = ["Pure", "Statistics"];
  return (
    <Stack gap={16}>
      <Row align="center" gap={12} wrap>
        <H2 style={{ margin: 0 }}>Confidence sheet</H2>
        <Spacer />
        <Text size="small" tone="secondary">
          Scoring curve
        </Text>
        <Select
          value={sev}
          onChange={setSev}
          options={(Object.keys(SEVERITY) as SeverityKey[]).map((k) => ({ value: k, label: SEVERITY[k].label }))}
          style={{ width: 280 }}
        />
        <Button variant="secondary" onClick={resetRatings}>
          Reset ratings
        </Button>
      </Row>
      <Text tone="secondary">
        Each topic&apos;s marks are split into routine marks and non-trivial marks, using the share measured on
        past A-level papers. A rating secures{" "}
        <Text as="span" weight="medium">
          (1 − n) × routine[L] + n × hard[L]
        </Text>{" "}
        of the topic&apos;s weight, where n is the topic&apos;s non-trivial share. Levels 0–2 earn almost
        nothing because partial understanding rarely survives a multi-part question. Level 4 is capped below
        100% because non-trivial marks are lost about half the time even when the topic is solid.
      </Text>
      {pillars.map((p) => {
        const rows = perTopic.filter((t) => t.pillar === p);
        const w = rows.reduce((a, t) => a + t.weight, 0);
        const got = rows.reduce((a, t) => a + t.marks, 0);
        return (
          <Stack key={p} gap={8}>
            <Row align="center" gap={10}>
              <H3 style={{ margin: 0 }}>{p}</H3>
              <Text size="small" tone="secondary">
                {(2 * w).toFixed(0)} marks of 200 · expected {got.toFixed(1)}
              </Text>
            </Row>
            <Table
              striped
              headers={["Topic", "Weight", "Rating (0–4)", "Level-4 ceiling", "Secured now", "Marks / 200", "Core done"]}
              columnAlign={["left", "right", "left", "right", "right", "right", "right"]}
              rows={rows.map((t) => [
                <Stack gap={0}>
                  <Text size="small" weight="medium">
                    {t.name}
                  </Text>
                  <Text size="small" tone="tertiary">
                    P1 {t.p1.toFixed(1)} · P2A {t.p2a.toFixed(1)} · P2B {t.p2b.toFixed(1)} marks / yr
                  </Text>
                </Stack>,
                `${t.weight.toFixed(1)}%`,
                <Row gap={4}>
                  {CONF_LEVELS.map((l) => (
                    <span key={l.v}>
                      <Pill size="sm" active={t.level === l.v} title={l.label} onClick={() => setRating(t.id, l.v)}>
                        {l.v}
                      </Pill>
                    </span>
                  ))}
                </Row>,
                `${(100 * t.cap).toFixed(0)}%`,
                <Text
                  size="small"
                  weight="medium"
                  style={{ color: t.level <= 2 ? theme.text.tertiary : theme.text.primary }}
                >
                  {(100 * t.realised).toFixed(0)}%
                </Text>,
                `${t.marks.toFixed(1)} / ${(2 * t.weight).toFixed(1)}`,
                t.coreTotal ? `${t.coreDone} / ${t.coreTotal}` : "—",
              ])}
            />
          </Stack>
        );
      })}
      <Row gap={10} align="center">
        <Text size="small" tone="tertiary">
          0 cannot start · 1 recognise only · 2 with notes open · 3 unaided and timed · 4 unseen variants
        </Text>
        <Spacer />
        <Text weight="semibold">
          Projected: {(2 * expectedPct).toFixed(1)} / 200 ({expectedPct.toFixed(1)}%)
        </Text>
      </Row>
      <CurveCard />
    </Stack>
  );
}

function CurveCard() {
  const { sev } = useModel();
  const median = [...DATA.topics].sort((a, b) => a.nt - b.nt)[Math.floor(DATA.topics.length / 2)];
  const pct = (k: SeverityKey) =>
    [0, 1, 2, 3, 4].map((L) => Number((100 * realised(median, L, k)).toFixed(0)));
  return (
    <Card>
      <CardHeader trailing={<Pill size="sm">median topic, n = {(100 * median.nt).toFixed(0)}%</Pill>}>
        How much each rating is worth
      </CardHeader>
      <CardBody>
        <Stack gap={8}>
          <LineChart
            categories={["Level 0", "Level 1", "Level 2", "Level 3", "Level 4"]}
            series={[
              { name: SEVERITY.brutal.label, data: pct("brutal"), tone: sev === "brutal" ? "danger" : "neutral" },
              { name: SEVERITY.strict.label, data: pct("strict"), tone: sev === "strict" ? "warning" : "neutral" },
              { name: SEVERITY.linear.label, data: pct("linear"), tone: "info" },
            ]}
            valueSuffix="%"
            height={220}
            showValues
          />
          <Text size="small" tone="tertiary">
            Confidence level vs. share of the topic&apos;s marks secured (%), for the topic with the median
            non-trivial share ({median.name}). The linear curve is the physics sheet&apos;s rule.
          </Text>
        </Stack>
      </CardBody>
    </Card>
  );
}

function WeightageSection() {
  const topics = [...DATA.topics].sort((a, b) => b.weight - a.weight);
  const pure = DATA.topics.filter((t) => t.pillar === "Pure");
  const p1 = pure.reduce((a, t) => a + t.p1, 0);
  const p2a = pure.reduce((a, t) => a + t.p2a, 0);
  return (
    <Stack gap={24}>
      <Stack gap={8}>
        <H2>Marks per topic on the A-level</H2>
        <Text tone="secondary">
          Average marks per sitting across {DATA.meta.papers} A-level papers (2017–2025), counting only parts
          inside the 2026 syllabus. Pure topics are scaled to 140 marks and statistics to 60, matching the
          paper structure. {DATA.meta.oosMarks} marks on removed topics were excluded.
        </Text>
        <BarChart
          categories={topics.map((t) => t.short)}
          series={[
            { name: "Paper 1", data: topics.map((t) => Number(t.p1.toFixed(1))) },
            { name: "Paper 2 Section A", data: topics.map((t) => Number(t.p2a.toFixed(1))) },
            { name: "Paper 2 Section B", data: topics.map((t) => Number(t.p2b.toFixed(1))) },
          ]}
          stacked
          horizontal
          height={560}
          valueSuffix=" marks"
        />
        <Text size="small" tone="tertiary">
          Topic vs. average marks per year out of 200, stacked by paper section · Pure: P1 {p1.toFixed(0)} + P2A{" "}
          {p2a.toFixed(0)} marks · Source: TYS answer scripts 2017–2025, tagged per question part
        </Text>
      </Stack>

      <Stack gap={8}>
        <H2>Why level 4 is not 100%</H2>
        <Text tone="secondary">
          Every question part was tagged with the marks a student fluent in all standard question types could
          still lose: an unfamiliar set-up they must model themselves, a non-standard step, an edge condition
          (domain, exclusion, exact form), a wording-graded explanation, or a hidden &quot;hence&quot; link. The
          non-trivial share n is shrunk toward the paper-wide average ({(100 * DATA.meta.ntGlobal).toFixed(0)}%)
          by {DATA.meta.shrinkK} marks so thinly tested topics do not get extreme ceilings.
        </Text>
        <Table
          striped
          headers={["Topic", "Marks / yr", "Range", "Years tested", "Non-trivial share", "Main source of lost marks"]}
          columnAlign={["left", "right", "right", "right", "right", "left"]}
          rows={topics.map((t) => {
            const types = Object.entries(t.ntTypes).sort((a, b) => b[1] - a[1]);
            return [
              <Text size="small" weight="medium">
                {t.name}
              </Text>,
              t.marksAvg.toFixed(1),
              `${t.minMarks}–${t.maxMarks}`,
              `${t.yearsTested} / ${t.nYears}`,
              <Text size="small">
                {(100 * t.nt).toFixed(0)}%{" "}
                <Text as="span" size="small" tone="tertiary">
                  (raw {(100 * t.ntRaw).toFixed(0)}%)
                </Text>
              </Text>,
              <Text size="small" tone="secondary">
                {types.length
                  ? types
                      .slice(0, 2)
                      .map(([k, v]) => `${k.toLowerCase()} ${v}`)
                      .join(", ") + (t.ntExamples[0] ? ` — e.g. ${t.ntExamples[0]}` : "")
                  : "No non-trivial marks tagged"}
              </Text>,
            ];
          })}
        />
        <Text size="small" tone="tertiary">
          Range is the lowest and highest marks in a single sitting. Type counts are non-trivial marks summed over
          all sittings.
        </Text>
      </Stack>

      <Callout tone="warning" title="Limits of these weights">
        <Text size="small">
          Nine sittings is a small sample: a topic absent for two years can still carry 15 marks next year, so
          the range column matters as much as the average. Non-trivial marks were judged by reading questions
          and solutions, not from examiner reports, and part-level topic labels assign mixed parts to the topic
          that earns most of the marks. 2017–2024 papers were set on the old syllabus; only 2025 reflects the
          revised one. Simple nested binomials were scored as routine for 2017–2021 but as one non-trivial
          mark for 2022–2025, which makes the Binomial ceiling one to two points harsher than a single
          standard would.
        </Text>
      </Callout>
    </Stack>
  );
}

function statusPill(i: Item) {
  if (i.status === "missing") return <Pill size="sm">Not in corpus</Pill>;
  if (i.status === "noSoln") return <Pill size="sm">No mark scheme</Pill>;
  if (i.status === "partial") return <Pill size="sm">Partly transcribed</Pill>;
  return <Pill size="sm">Ready</Pill>;
}

function TopicalSection() {
  const theme = useHostTheme();
  const { done, toggleDone, perTopic } = useModel();
  const [topicId, setTopicId] = useCanvasState<string>("topicalTopic", DATA.topics[1]?.id ?? DATA.topics[0].id);
  const [showStretch, setShowStretch] = useCanvasState<boolean>("showStretch", false);
  const topic = perTopic.find((t) => t.id === topicId) ?? perTopic[0];
  const items = DATA.items.filter((i) => i.topicId === topic.id && (showStretch || i.tier === "core"));
  const totals = DATA.items.filter((i) => i.tier === "core");
  const totalDone = totals.filter((i) => done[i.key]).length;

  return (
    <Stack gap={16}>
      <Stack gap={6}>
        <H2>Topical practice</H2>
        <Text tone="secondary">
          The {totals.length} core and {DATA.items.length - totals.length} stretch questions from{" "}
          <Text as="span" weight="medium">
            H2 Math Revision Order.html
          </Text>
          , with the question text pulled from the paper corpus into one worksheet per chapter in{" "}
          <Text as="span" weight="medium">
            {DATA.meta.worksheetDir}
          </Text>
          . Tick a question once you have finished it unaided; the count feeds the &quot;Core done&quot; column.
        </Text>
      </Stack>
      <Row gap={12} align="center" wrap>
        <Select
          value={topic.id}
          onChange={setTopicId}
          options={perTopic.map((t) => ({
            value: t.id,
            label: `${t.name} · rating ${t.level} · ${t.coreDone}/${t.coreTotal} core`,
          }))}
          style={{ width: 380 }}
        />
        <Row gap={6} align="center">
          <Toggle checked={showStretch} onChange={setShowStretch} />
          <Text size="small" tone="secondary">
            Show stretch
          </Text>
        </Row>
        <Spacer />
        <Text size="small" tone="secondary">
          All core: {totalDone} / {totals.length} done
        </Text>
      </Row>
      <Table
        headers={["Done", "#", "Source", "Marks", "What it asks", "Status"]}
        columnAlign={["left", "right", "left", "right", "left", "left"]}
        rows={items.map((i) => [
          <Checkbox checked={!!done[i.key]} onChange={(v) => toggleDone(i.key, v)} disabled={i.status === "missing"} />,
          <Text size="small" tone={i.tier === "core" ? "primary" : "tertiary"}>
            {i.n}
            {i.tier === "stretch" ? "s" : ""}
          </Text>,
          <Text size="small" weight="medium">
            {i.ref}
          </Text>,
          i.marks || "—",
          <Stack gap={2}>
            <Text size="small" style={{ color: i.status === "missing" ? theme.text.tertiary : theme.text.primary }}>
              {i.stem}
            </Text>
            {i.flags.length || i.note ? (
              <Text size="small" tone="tertiary">
                {[...i.flags.map((f) => FLAG_LABEL[f] ?? f), i.note].filter(Boolean).join(" · ")}
              </Text>
            ) : null}
          </Stack>,
          statusPill(i),
        ])}
        rowTone={items.map((i) => (i.status === "missing" ? "warning" : undefined))}
      />
    </Stack>
  );
}

function AcquireSection() {
  const core = DATA.acquire.filter((a) => a.priority === "core" && a.kind !== "scan" && a.kind !== "timed");
  const stretch = DATA.acquire.filter((a) => a.priority === "stretch" && a.kind !== "scan" && a.kind !== "timed");
  const scans = DATA.acquire.filter((a) => a.kind === "scan");
  const timed = DATA.acquire.filter((a) => a.kind === "timed");
  const reserved = DATA.items.filter((i) => i.flags.includes("reserved"));
  const reservedCore = reserved.filter((i) => i.tier === "core");
  const coreMissing = DATA.items.filter((i) => i.tier === "core" && i.status === "missing").length;
  const kindLabel: Record<Acquire["kind"], string> = {
    questions: "Questions + solutions",
    solutions: "Mark scheme only",
    hardcopy: "Hardcopy to scan",
    scan: "Pages missing from scan",
    timed: "Timed paper incomplete",
  };
  const table = (rows: Acquire[]) => (
    <Table
      striped
      headers={["Document", "What is missing", "Items it unlocks", "Note"]}
      columnAlign={["left", "left", "left", "left"]}
      rows={rows.map((a) => [
        <Text size="small" weight="medium">
          {a.doc}
        </Text>,
        kindLabel[a.kind],
        <Text size="small">{a.blocks.join(", ")}</Text>,
        <Text size="small" tone="secondary">
          {a.note}
        </Text>,
      ])}
    />
  );
  return (
    <Stack gap={20}>
      <Stack gap={6}>
        <H2>Documents to acquire</H2>
        <Text tone="secondary">
          {coreMissing} core questions cannot be done from the corpus because their source document is not in
          the repository. Questions marked &quot;mark scheme only&quot; can be attempted now but cannot be
          self-marked.
        </Text>
      </Stack>
      {timed.length ? (
        <Stack gap={8}>
          <H3>Blocks timed rehearsal papers</H3>
          <Text size="small" tone="secondary">
            Dress rehearsals follow the revision order&apos;s ten timed sets. These sets cannot be sat or marked
            from the corpus as it stands.
          </Text>
          {table(timed)}
        </Stack>
      ) : null}
      <Stack gap={8}>
        <H3>Blocks core questions</H3>
        {table(core)}
      </Stack>
      {stretch.length ? (
        <Stack gap={8}>
          <H3>Blocks stretch questions only</H3>
          {table(stretch)}
        </Stack>
      ) : null}
      {scans.length ? (
        <Stack gap={8}>
          <H3>Incomplete scans of A-level papers</H3>
          <Text size="small" tone="secondary">
            These papers are in the corpus but pages are missing, so some question text was reconstructed from
            the solutions and a few mark splits used for the weights are estimates.
          </Text>
          {table(scans)}
        </Stack>
      ) : null}
      {reserved.length ? (
        <Callout tone="warning" title={`${reservedCore.length} core questions come from RI papers you sealed for timed gates`}>
          <Stack gap={6}>
            <Text size="small">
              The milestone plan keeps RI Prelim 2025, RI Prelim 2022 and RI Prelim 2024 P1 unseen for
              closed-book dress rehearsals. The revision order instead uses its own ten timed sets and draws{" "}
              {reserved.length} topical questions ({reservedCore.length} core) from those RI papers. Doing them
              as topicals spends those papers.
            </Text>
            <Text size="small" tone="secondary">
              Core items affected: {reservedCore.map((i) => i.ref).join(", ")}.
            </Text>
          </Stack>
        </Callout>
      ) : null}
    </Stack>
  );
}

function OutlookSection() {
  const { yearProjection, expectedPct, perTopic, sev } = useModel();
  const lo = Math.min(...yearProjection);
  const hi = Math.max(...yearProjection);
  const sd = stdev(yearProjection);
  const gains = perTopic
    .map((t) => {
      const to3 = t.level < 3 ? 2 * t.weight * (realised(t, 3, sev) - t.realised) : 0;
      const to4 = 2 * t.weight * (t.cap - Math.max(t.realised, t.level < 3 ? realised(t, 3, sev) : t.realised));
      const left = t.coreTotal - t.coreDone;
      return { ...t, to3, to4, left, perQ: left > 0 ? to3 / left : 0 };
    })
    .filter((t) => t.to3 > 0.05 || t.to4 > 0.05)
    .sort((a, b) => b.to3 - a.to3 || b.to4 - a.to4);
  const total3 = gains.reduce((a, t) => a + t.to3, 0);
  const caps = [...perTopic].sort((a, b) => a.cap - b.cap);

  return (
    <Stack gap={24}>
      <Stack gap={10}>
        <H2>Backtest against 2017–2025 A-level papers</H2>
        <Text tone="secondary">
          Current ratings applied to each sitting&apos;s own topic mix (in-syllabus parts only, rescaled to
          200). The spread of {(hi - lo).toFixed(0)} points shows how much the topic draw alone can move the
          result.
        </Text>
        <Grid columns={4} gap={16}>
          <Stat value={`${expectedPct.toFixed(0)}%`} label="Expected (average mix)" />
          <Stat value={`${lo.toFixed(0)}%`} label="Worst sitting" tone="danger" />
          <Stat value={`${hi.toFixed(0)}%`} label="Best sitting" tone="success" />
          <Stat value={`±${sd.toFixed(1)}`} label="Std. deviation across sittings (points)" />
        </Grid>
        <LineChart
          categories={DATA.years}
          series={[{ name: "Projected mark", data: yearProjection.map((v) => Number(v.toFixed(1))), tone: "info" }]}
          valueSuffix="%"
          height={220}
          showValues
          referenceLines={GRADE_LINES}
        />
        <Text size="small" tone="tertiary">
          A-level year vs. projected mark (%) · Grade lines are indicative · Source: tagged TYS answer scripts
        </Text>
      </Stack>

      <Stack gap={10}>
        <H2>Marks unlocked by topical work</H2>
        <Text tone="secondary">
          Raising every topic below level 3 to level 3 adds{" "}
          <Text as="span" weight="semibold">
            {total3.toFixed(1)} marks
          </Text>
          . Going from 3 to 4 is worth much less per topic because the ceiling caps it; that is the model
          saying breadth at level 3 beats depth at level 4.
        </Text>
        <Table
          headers={["Topic", "Rating", "To level 3", "Then to 4", "Core left", "Marks per core question"]}
          columnAlign={["left", "right", "right", "right", "right", "right"]}
          rows={gains.map((t) => [
            <Text size="small">{t.name}</Text>,
            t.level,
            t.to3 > 0 ? `+${t.to3.toFixed(1)}` : "—",
            `+${t.to4.toFixed(1)}`,
            t.left,
            t.perQ > 0 ? t.perQ.toFixed(2) : "—",
          ])}
        />
        <Text size="small" tone="tertiary">
          Marks out of 200. &quot;Marks per core question&quot; divides the level-3 gain by the core questions
          not yet ticked, as a rough return on each question.
        </Text>
      </Stack>

      <Stack gap={10}>
        <H2>Level-4 ceiling by topic</H2>
        <BarChart
          categories={caps.map((t) => t.short)}
          series={[{ name: "Share of topic marks secured at level 4", data: caps.map((t) => Number((100 * t.cap).toFixed(0))) }]}
          valueSuffix="%"
          height={280}
          yMin={60}
          yMax={100}
          showValues
        />
        <Text size="small" tone="tertiary">
          Topic vs. level-4 ceiling (%) under the {SEVERITY[sev].label.toLowerCase()} curve · Lower bars are topics
          where the A-level most often adds twists beyond the standard question types.
        </Text>
      </Stack>
    </Stack>
  );
}

export default function MathReadiness() {
  const [section, setSection] = useCanvasState<Section>("section", "Readiness");
  return (
    <Stack gap={24} style={{ padding: 24, maxWidth: 1180, margin: "0 auto" }}>
      <HeaderStats />
      <SectionNav section={section} setSection={setSection} />
      <Divider />
      {section === "Readiness" ? <ReadinessSection /> : null}
      {section === "Weightage" ? <WeightageSection /> : null}
      {section === "Topical" ? <TopicalSection /> : null}
      {section === "Acquire" ? <AcquireSection /> : null}
      {section === "Outlook" ? <OutlookSection /> : null}
    </Stack>
  );
}
