/**
 * Welcome card shown on the home page before the user submits a query.
 * Sets the scene ("you're a new engineer") and provides clickable
 * suggestion chips so users know what kinds of questions to ask.
 */

const SUGGESTIONS = [
  "What should I do during my first week?",
  "How is the codebase structured?",
  "How do I set up my local dev environment?",
  "What's the process for submitting a pull request?",
  "How does authentication work?",
];

interface WelcomeCardProps {
  onSuggestionClick: (query: string) => void;
}
export default function WelcomeCard({ onSuggestionClick }: WelcomeCardProps) {
  return (
    <div className="rounded-lg border border-gray-200 bg-white p-6 dark:border-vsc-surface dark:bg-vsc-surface">
      <p className="text-gray-700 dark:text-vsc-text">
        <strong>Scenario:</strong> You're a new engineer starting your first week at the company.
        You have access to all the internal docs — try asking about onboarding, architecture,
        dev setup, coding standards, or how things work around here.
      </p>
      <div className="mt-4 flex flex-wrap gap-2">
        {SUGGESTIONS.map((q) => (
          <button
            key={q}
            onClick={() => onSuggestionClick(q)}
            className="rounded-full border border-purple-300 px-3 py-1 text-sm text-purple-700 hover:bg-purple-50 dark:border-purple-500/40 dark:text-purple-300 dark:hover:bg-purple-500/10"
          >
            {q}
          </button>
        ))}
      </div>
    </div>
  );
}
