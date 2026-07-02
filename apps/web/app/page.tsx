const sections = [
  ['Important emails', 'Prospect request and supplier renewal need attention.'],
  ['Calendar', 'Board preparation gap detected for tomorrow.'],
  ['KPIs', 'Revenue, pipeline and retention are visible in one executive view.'],
  ['Risks', 'Current priorities are retention, board readiness and sales execution.'],
  ['Competitors', 'Monitor overlapping AI executive workflow launches.'],
  ['Suggested actions', 'Assign owners, attach board pack and map executive sponsors.'],
];

export default function Home() {
  return (
    <main className="shell">
      <section className="hero">
        <p className="eyebrow">RaeburnAI Executive</p>
        <h1>A CEO&apos;s second brain.</h1>
        <p className="lede">Daily briefings across emails, calendar, KPIs, risks, sales, competitors, news and recommended actions.</p>
        <div className="actions"><a href="/api-docs">API ready</a><a href="https://github.com/Raebu/RaeburnAI-Executive">Open source</a></div>
      </section>
      <section className="dashboard">
        {sections.map(([title, body]) => <article className="card" key={title}><h2>{title}</h2><p>{body}</p></article>)}
      </section>
    </main>
  );
}
