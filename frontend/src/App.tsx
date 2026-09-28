import { useEffect, useMemo, useState } from 'react';

type Session = {
  id: string;
  title: string;
  status: string;
  puzzle_count: number;
  current_stage: number;
  score: number;
};

type Hint = {
  text: string;
  level: number;
};

const API_BASE = window.location.hostname === 'localhost' ? 'http://localhost:8000' : '/api';

function App() {
  const [session, setSession] = useState<Session | null>(null);
  const [loading, setLoading] = useState(false);
  const [answer, setAnswer] = useState('');
  const [feedback, setFeedback] = useState<string>('');
  const [hint, setHint] = useState<Hint | null>(null);
  const [error, setError] = useState<string>('');

  const currentObjective = useMemo(() => {
    if (!session) return 'Create a session to begin the escape room.';
    return `Stage ${session.current_stage} / ${session.puzzle_count} • Current score ${session.score}`;
  }, [session]);

  useEffect(() => {
    void fetchSession();
  }, []);

  const fetchSession = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE}/sessions`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          player_name: 'Operator',
          puzzle_seed: 42,
        }),
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || 'Unable to create session.');
      setSession(data);
      setFeedback('Session ready. The room is live.');
      setError('');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Session creation failed.');
    } finally {
      setLoading(false);
    }
  };

  const submitAnswer = async () => {
    if (!session) return;
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE}/sessions/${session.id}/answer`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ answer }),
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || 'Answer rejected.');
      setFeedback(data.message || 'Puzzle solved.');
      setAnswer('');
      setHint(null);
      setSession((current) => current ? { ...current, score: data.score ?? current.score } : current);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Submission failed.');
    } finally {
      setLoading(false);
    }
  };

  const requestHint = async () => {
    if (!session) return;
    try {
      const response = await fetch(`${API_BASE}/sessions/${session.id}/hint`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({}),
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || 'Hint unavailable.');
      setHint({ text: data.hint || 'Keep searching for the hidden signal.', level: data.level || 1 });
      setFeedback('Hint unlocked.');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unable to fetch hint.');
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <div className="mx-auto max-w-6xl px-6 py-10">
        <header className="mb-8 flex items-center justify-between rounded-2xl border border-sky-500/20 bg-slate-900/70 p-5 shadow-glow backdrop-blur">
          <div>
            <p className="text-xs uppercase tracking-[0.3em] text-sky-300">Mission Control</p>
            <h1 className="mt-2 text-3xl font-bold">AI Escape Room</h1>
          </div>
          <button
            onClick={() => void fetchSession()}
            className="rounded-xl border border-sky-400/40 bg-sky-500/20 px-4 py-2 font-medium text-sky-100 transition hover:bg-sky-500/30"
          >
            New Session
          </button>
        </header>

        <div className="grid gap-6 lg:grid-cols-[1.4fr_0.6fr]">
          <main className="rounded-3xl border border-slate-800 bg-slate-900/80 p-6">
            <div className="mb-5 flex items-center justify-between gap-4 border-b border-slate-800 pb-4">
              <div>
                <p className="text-xs uppercase tracking-[0.25em] text-violet-300">Objective</p>
                <h2 className="mt-2 text-xl font-semibold">{currentObjective}</h2>
              </div>
              <div className="rounded-full border border-emerald-500/30 bg-emerald-500/10 px-3 py-1 text-sm text-emerald-200">
                {session ? session.status : 'Booting'}
              </div>
            </div>

            <div className="rounded-2xl border border-slate-800 bg-slate-950/80 p-5">
              <p className="text-sm text-slate-300">The chamber is humming. Evidence drifts across the walls, and the final door only opens when the hidden reasoning chain is complete.</p>
              <div className="mt-5 space-y-4">
                <label className="block text-sm font-medium text-slate-200">Your answer</label>
                <textarea
                  value={answer}
                  onChange={(event) => setAnswer(event.target.value)}
                  rows={4}
                  placeholder="Type the final solution or phrase..."
                  className="w-full resize-none rounded-xl border border-slate-700 bg-slate-900 px-4 py-3 text-slate-100 outline-none ring-0 transition placeholder:text-slate-500 focus:border-sky-500"
                />
                <div className="flex flex-wrap gap-3">
                  <button
                    onClick={() => void submitAnswer()}
                    disabled={!session || loading}
                    className="rounded-xl bg-sky-500 px-5 py-2.5 font-medium text-slate-950 transition hover:bg-sky-400 disabled:cursor-not-allowed disabled:opacity-50"
                  >
                    Submit
                  </button>
                  <button
                    onClick={() => void requestHint()}
                    disabled={!session}
                    className="rounded-xl border border-violet-400/40 bg-violet-500/10 px-5 py-2.5 font-medium text-violet-100 transition hover:bg-violet-500/20 disabled:cursor-not-allowed disabled:opacity-50"
                  >
                    Request Hint
                  </button>
                </div>
              </div>
            </div>

            <div className="mt-6 space-y-3">
              {feedback && <div className="rounded-xl border border-emerald-500/30 bg-emerald-500/10 px-4 py-3 text-sm text-emerald-200">{feedback}</div>}
              {hint && (
                <div className="rounded-xl border border-amber-500/30 bg-amber-500/10 px-4 py-3 text-sm text-amber-100">
                  <span className="font-semibold">Hint {hint.level}:</span> {hint.text}
                </div>
              )}
              {error && <div className="rounded-xl border border-rose-500/30 bg-rose-500/10 px-4 py-3 text-sm text-rose-200">{error}</div>}
            </div>
          </main>

          <aside className="space-y-6">
            <div className="rounded-3xl border border-slate-800 bg-slate-900/80 p-5">
              <p className="text-xs uppercase tracking-[0.25em] text-cyan-300">Session</p>
              <dl className="mt-4 space-y-3 text-sm text-slate-300">
                <div className="flex justify-between"><dt>ID</dt><dd>{session?.id ?? '---'}</dd></div>
                <div className="flex justify-between"><dt>Title</dt><dd>{session?.title ?? 'Awaiting'}</dd></div>
                <div className="flex justify-between"><dt>Puzzles</dt><dd>{session?.puzzle_count ?? 0}</dd></div>
                <div className="flex justify-between"><dt>Score</dt><dd>{session?.score ?? 0}</dd></div>
              </dl>
            </div>

            <div className="rounded-3xl border border-slate-800 bg-slate-900/80 p-5">
              <p className="text-xs uppercase tracking-[0.25em] text-fuchsia-300">Room Status</p>
              <ul className="mt-4 space-y-3 text-sm text-slate-300">
                <li>• Symbol recognition live</li>
                <li>• Retrieval memory active</li>
                <li>• Graph reasoning online</li>
                <li>• Semantic hint engine ready</li>
              </ul>
            </div>
          </aside>
        </div>
      </div>
    </div>
  );
}

export default App;
