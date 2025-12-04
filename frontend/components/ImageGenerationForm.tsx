'use client'

import { useState } from 'react'

interface ImageGenerationFormProps {
  onGenerate: (prompt: string) => void
  loading: boolean
}

export default function ImageGenerationForm({
  onGenerate,
  loading,
}: ImageGenerationFormProps) {
  const [prompt, setPrompt] = useState('')

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (prompt.trim()) {
      onGenerate(prompt)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label
          htmlFor="prompt"
          className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
        >
          Enter your image prompt
        </label>
        <textarea
          id="prompt"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="e.g., A professional portrait of a person in a business suit..."
          className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-gray-700 dark:text-white resize-none"
          rows={4}
          disabled={loading}
        />
        <p className="mt-2 text-sm text-gray-500 dark:text-gray-400">
          The system will enhance your prompt and generate images locally using Stable Diffusion
        </p>
      </div>

      <button
        type="submit"
        disabled={loading || !prompt.trim()}
        className="w-full bg-primary-600 hover:bg-primary-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {loading ? 'Generating...' : 'Generate Image'}
      </button>
    </form>
  )
}

