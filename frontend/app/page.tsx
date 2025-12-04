'use client'

import { useState } from 'react'
import ImageGenerationForm from '@/components/ImageGenerationForm'
import WorkflowVisualization from '@/components/WorkflowVisualization'
import ResultDisplay from '@/components/ResultDisplay'

interface WorkflowStep {
  agent: string
  status: string
  result: any
  timestamp: string
}

interface WorkflowResult {
  success: boolean
  workflow_id: string
  result: {
    original_prompt: string
    enhanced_prompt: string
    image_url: string
    validation: any
    passed_validation: boolean
  }
  message: string
}

export default function Home() {
  const [workflowResult, setWorkflowResult] = useState<WorkflowResult | null>(null)
  const [workflowSteps, setWorkflowSteps] = useState<WorkflowStep[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleGenerate = async (prompt: string) => {
    setLoading(true)
    setError(null)
    setWorkflowResult(null)
    setWorkflowSteps([])

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
      const response = await fetch(`${apiUrl}/api/generate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          prompt,
        }),
      })

      const data = await response.json()

      if (data.success) {
        setWorkflowResult(data)
        // Fetch detailed workflow steps
        const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
        const workflowResponse = await fetch(
          `${apiUrl}/api/workflow/${data.workflow_id}`
        )
        const workflowData = await workflowResponse.json()
        setWorkflowSteps(workflowData.steps || [])
      } else {
        setError(data.message || 'Failed to generate image')
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred')
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800">
      <div className="container mx-auto px-4 py-8">
        <header className="text-center mb-12">
          <h1 className="text-5xl font-bold text-gray-900 dark:text-white mb-4">
            SigmaChain
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-300">
            Agentic Image Generation with Intelligent Validation
          </p>
          <p className="text-sm text-gray-500 dark:text-gray-400 mt-2">
            Multi-agent workflow: Prompt Enhancement → Image Generation → Validation
          </p>
        </header>

        <div className="max-w-6xl mx-auto">
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-xl p-6 mb-8">
            <ImageGenerationForm
              onGenerate={handleGenerate}
              loading={loading}
            />
          </div>

          {error && (
            <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4 mb-8">
              <p className="text-red-800 dark:text-red-200">{error}</p>
            </div>
          )}

          {workflowSteps.length > 0 && (
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-xl p-6 mb-8">
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
                Workflow Steps
              </h2>
              <WorkflowVisualization steps={workflowSteps} />
            </div>
          )}

          {workflowResult && (
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-xl p-6">
              <ResultDisplay result={workflowResult} />
            </div>
          )}
        </div>

        <footer className="text-center mt-12 text-gray-500 dark:text-gray-400">
          <p>
            Learn how agentic tools work through this interactive demonstration
          </p>
        </footer>
      </div>
    </main>
  )
}

