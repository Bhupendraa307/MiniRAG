import React, { useState, useMemo } from 'react';
import { Search, Loader2, Clock, Zap, X } from 'lucide-react';
import { queryDocuments } from '../utils/api';

const AnswerWithCitations = ({ answer, citations, onSelectCitation }) => {
    const parsedAnswer = useMemo(() => {
        if (!answer) return [];
        const parts = [];
        let lastIndex = 0;
        const regex = /\[(\d+)\]/g;
        let match;

        while ((match = regex.exec(answer)) !== null) {
            if (match.index > lastIndex) {
                parts.push({ type: 'text', content: answer.slice(lastIndex, match.index) });
            }
            const index = Number(match[1]) - 1;
            parts.push({ type: 'citation', index });
            lastIndex = regex.lastIndex;
        }

        if (lastIndex < answer.length) {
            parts.push({ type: 'text', content: answer.slice(lastIndex) });
        }
        return parts;
    }, [answer]);

    return (
        <div className="text-gray-700 dark:text-gray-300 leading-relaxed">
            {parsedAnswer.map((part, idx) => {
                if (part.type === 'text') {
                    return <span key={idx}>{part.content}</span>;
                }
                if (part.type === 'citation') {
                    const citation = citations?.[part.index];
                    return (
                        <button
                            type="button"
                            key={idx}
                            className="inline-flex items-center px-2 py-1 text-xs font-medium bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200 rounded-full mx-1 cursor-pointer hover:bg-blue-200 dark:hover:bg-blue-800"
                            onClick={() => citation && onSelectCitation(citation)}
                        >
                            {part.index + 1}
                        </button>
                    );
                }
                return null;
            })}
        </div>
    );
};
const QueryInterface = ({ onError }) => {
    const [query, setQuery] = useState('');
    const [isQuerying, setIsQuerying] = useState(false);
    const [result, setResult] = useState(null);
    const [selectedCitation, setSelectedCitation] = useState(null);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!query.trim()) return;

        setIsQuerying(true);
        setResult(null);
        try {
            const response = await queryDocuments(query);
            setResult(response);
        } catch (error) {
            onError(error.response?.data?.detail || 'Query failed');
        } finally {
            setIsQuerying(false);
        }
    };

    return (
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold mb-4 text-gray-900 dark:text-white">Ask a Question</h2>

            <form onSubmit={handleSubmit} className="space-y-4">
                <div className="flex space-x-2">
                    <input
                        type="text"
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                        className="flex-1 px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
                        placeholder="Ask a question about your documents..."
                        disabled={isQuerying}
                    />
                    <button
                        type="submit"
                        disabled={isQuerying || !query.trim()}
                        className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
                    >
                        {isQuerying ? <Loader2 className="w-4 h-4 animate-spin" /> : <Search className="w-4 h-4" />}
                    </button>
                </div>
            </form>

            {result && (
                <div className="mt-6 space-y-6">
                    <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
                        <h3 className="font-semibold text-gray-900 dark:text-white mb-2">Answer:</h3>
                        <AnswerWithCitations
                            answer={result.answer}
                            citations={result.citations}
                            onSelectCitation={setSelectedCitation}
                        />
                    </div>

                    {result.citations && result.citations.length > 0 && (
                        <div className="space-y-2">
                            <h3 className="font-semibold text-gray-900 dark:text-white">Sources:</h3>
                            {result.citations.map((citation, index) => (
                                <details key={citation.id || index} className="bg-gray-50 dark:bg-gray-700 rounded-lg p-3">
                                    <summary className="cursor-pointer font-medium text-gray-900 dark:text-white">
                                        [{index + 1}] {citation.metadata.filename || 'Unknown source'}
                                    </summary>
                                    <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
                                        {citation.text.substring(0, 300)}{citation.text.length > 300 ? '...' : ''}
                                    </p>
                                </details>
                            ))}
                        </div>
                    )}

                    <div className="flex items-center space-x-4 text-sm text-gray-500 dark:text-gray-400">
                        <div className="flex items-center">
                            <Clock className="w-4 h-4 mr-1" /> {(result.latency ?? 0).toFixed(2)}s
                        </div>
                        <div className="flex items-center">
                            <Zap className="w-4 h-4 mr-1" /> {result.token_usage?.total_tokens ?? 0} tokens
                        </div>
                    </div>
                </div>
            )}

            {selectedCitation && (
                <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
                    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-2xl w-full">
                        <div className="flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-700">
                            <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                                {selectedCitation.metadata?.filename || 'Source'}
                            </h3>
                            <button
                                onClick={() => setSelectedCitation(null)}
                                className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
                            >
                                <X className="w-5 h-5" />
                            </button>
                        </div>
                        <div className="p-4">
                            <p className="text-gray-700 dark:text-gray-300 leading-relaxed whitespace-pre-line overflow-y-auto max-h-[70vh]">
                                {selectedCitation.text || ''}
                            </p>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default QueryInterface;