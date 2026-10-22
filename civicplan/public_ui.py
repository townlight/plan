"""Static public UI shell for Townlight Planning v0.2.2."""

from __future__ import annotations


def render_public_lookup_page() -> str:
    """Render the public-facing Townlight Planning sample page."""

    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Townlight Planning Public Policy Lookup</title>
<style>
  :root { --ink:#17202a; --muted:#56606a; --paper:#fffaf0; --blue:#184d70; --green:#2f6b50; --gold:#d8b45b; --line:#d6c6a1; }
  * { box-sizing: border-box; }
  body { margin:0; color:var(--ink); font-family:"Aptos","Segoe UI",sans-serif; background:radial-gradient(circle at 20% 10%,#fff4d0,transparent 34%),linear-gradient(135deg,#f8efe0,#edf6f4); }
  .skip-link { position:absolute; left:1rem; top:-4rem; background:var(--ink); color:white; padding:.7rem 1rem; border-radius:999px; }
  .skip-link:focus { top:1rem; }
  header, main, footer { width:min(1120px, calc(100% - 32px)); margin:0 auto; }
  header { padding:48px 0 24px; }
  .eyebrow { color:var(--blue); text-transform:uppercase; letter-spacing:.18em; font-weight:800; font-size:.78rem; }
  h1 { max-width:960px; margin:0; font-family:Georgia,"Times New Roman",serif; font-size:clamp(2.7rem,7vw,5.7rem); line-height:.95; letter-spacing:-.05em; }
  .lede { max-width:820px; font-size:clamp(1.1rem,2.4vw,1.45rem); line-height:1.55; color:#31404a; }
  .badge { display:inline-flex; width:fit-content; padding:.45rem .75rem; border-radius:999px; background:var(--green); color:white; font-weight:900; }
  .grid { display:grid; grid-template-columns:repeat(12,1fr); gap:18px; }
  .card { grid-column:span 6; min-width:0; padding:24px; border:1px solid var(--line); border-radius:28px; background:rgba(255,250,240,.92); box-shadow:0 18px 40px rgba(35,43,50,.10); }
  .card.large { grid-column:span 12; }
  h2,h3 { font-family:Georgia,"Times New Roman",serif; letter-spacing:-.03em; }
  h2 { margin:0 0 14px; font-size:clamp(1.8rem,4vw,3rem); }
  p, li { line-height:1.65; }
  .sample-box { padding:18px; border:1px solid #b9c6cc; border-radius:16px; background:#f3f7f8; color:var(--ink); }
  .result { margin-top:18px; padding:18px; border-left:6px solid var(--green); border-radius:18px; background:white; }
  .warning { border-left-color:#b2603f; background:#fff8f4; }
  .kicker { color:var(--muted); font-size:.86rem; font-weight:900; letter-spacing:.08em; text-transform:uppercase; }
  .notice { margin:24px 0 0; padding:18px; border:1px dashed #b2603f; border-radius:22px; background:rgba(178,96,63,.10); }
  footer { padding:38px 0 56px; color:var(--muted); }
  :focus-visible { outline:4px solid var(--gold); outline-offset:3px; }
  @media (max-width:760px) { header,main,footer{margin:0;max-width:390px;width:100%;padding-left:24px;padding-right:24px}header{padding-top:34px}h1{font-size:clamp(2.2rem,11vw,3rem)}.card{grid-column:span 12;padding:20px;border-radius:22px} }
</style>
</head>
<body>
<a class="skip-link" href="#main">Skip to main content</a>
<header>
  <p class="eyebrow">Townlight / Townlight Planning public sample</p>
  <h1>Find plan policies with citations before the meeting packet gets written.</h1>
  <p class="lede">Townlight Planning demonstrates cited comprehensive-plan lookup, policy-consistency support, and staff-analysis outlines. It helps staff and residents find adopted policy context without turning software into the decision-maker.</p>
  <p><span class="badge">0.3.0+dev.1 explicit static sample</span></p>
</header>
<main id="main" tabindex="-1">
  <section class="grid" aria-labelledby="lookup-title">
    <article class="card large">
      <p class="kicker">Plan-policy lookup</p>
      <h2 id="lookup-title">Housing proposal context</h2>
      <p class="kicker">Static sample proposal</p>
      <div class="sample-box">A small mixed-use housing project near transit, a school, and a neighborhood park.</div>
      <div class="result" role="status" aria-live="polite">
        <h3>Relevant adopted policy</h3>
        <p><strong>Comprehensive Plan, Housing Element, Policy H-2.1:</strong> Encourage missing-middle housing within walking distance of transit, schools, parks, and daily services.</p>
      </div>
    </article>
    <article class="card">
      <p class="kicker">Consistency support</p>
      <h2>Support, not determination</h2>
      <div class="result"><p>Sample status: potentially consistent. Planner of record must confirm facts, procedures, and official findings.</p></div>
    </article>
    <article class="card">
      <p class="kicker">Staff analysis</p>
      <h2>Cited outline</h2>
      <div class="result"><p>Draft bullets include relevant policy, sample status, and review-required warnings for the staff report.</p></div>
    </article>
    <article class="card">
      <p class="kicker">Records-ready export</p>
      <h2>Keep provenance</h2>
      <div class="result"><p>Exports preserve source policy, proposal text, reviewer, generated outline, and final staff edits.</p></div>
    </article>
    <article class="card">
      <p class="kicker">Plan navigator</p>
      <h2>Browse adopted structure</h2>
      <div class="result"><p>Residents and staff can browse policies by plan type, topic, goal, and citation while pending amendments stay labeled for review.</p></div>
    </article>
    <article class="card">
      <p class="kicker">Progress tracking</p>
      <h2>Evidence, not findings</h2>
      <div class="result"><p>Measurable targets include status, evidence, citation, and review-required boundaries for staff follow-up.</p></div>
    </article>
    <article class="card">
      <p class="kicker">Planning boundary</p>
      <h2>No official determination</h2>
      <div class="result warning"><p>Townlight Planning does not make zoning, land-use, environmental, legal, or elected-body decisions. Staff and officials remain responsible for every official action.</p></div>
    </article>
  </section>
  <section class="notice" aria-labelledby="boundary-title">
    <h2 id="boundary-title">Important boundaries</h2>
    <p>Townlight Planning 0.3.0+dev.1 is the P3/P4 development workflows. This page is an explicit static sample, not the municipal workflow. The published v0.2.2 remains a narrow truth-repair release with no functional upgrade. It exists solely to supersede the false v1.0.0 release from 2026-05-21 in GitHub's Latest impression; the Townlight Core pin is unchanged. Townlight Planning provides cited plan lookup, local policy ingestion when configured, Townlight Zoning and Townlight Meetings context contracts, amendment history, progress targets, and adversarial local integration validation. It does not call live external systems by default, provide legal advice, or make official planning determinations.</p>
  </section>
</main>
<footer><p>Townlight Planning is part of the AGPL-3.0 Townlight open-source municipal AI project.</p></footer>
</body>
</html>
"""
