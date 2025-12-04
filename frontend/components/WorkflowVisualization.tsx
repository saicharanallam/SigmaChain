'use client'

interface WorkflowStep {
  agent: string
  status: string
  result: any
  timestamp: string
}

interface WorkflowVisualizationProps {
  steps: WorkflowStep[]
}

export default function WorkflowVisualization({
  steps,
}: WorkflowVisualizationProps) {
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'success':
        return 'bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400'
      case 'failed':
        return 'bg-red-100 text-red-800 dark:bg-red-900/20 dark:text-red-400'
      default:
        return 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300'
    }
  }

  const getAgentDescription = (agent: string) => {
    switch (agent) {
      case 'PromptEnhancer':
        return 'Enhances your prompt with technical details and best practices'
      case 'ImageGenerator':
        return 'Generates the image using AI image generation models'
      case 'Validator':
        return 'Validates anatomical correctness and image quality'
      default:
        return 'Processes the workflow step'
    }
  }

  return (
    <div className="space-y-4">
      {steps.map((step, index) => (
        <div
          key={index}
          className="border-l-4 border-primary-500 pl-4 py-2"
        >
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center space-x-3">
              <span className="text-sm font-semibold text-primary-600 dark:text-primary-400">
                Step {index + 1}
              </span>
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                {step.agent}
              </h3>
              <span
                className={`px-2 py-1 text-xs font-medium rounded ${getStatusColor(
                  step.status
                )}`}
              >
                {step.status}
              </span>
            </div>
            <span className="text-xs text-gray-500 dark:text-gray-400">
              {new Date(step.timestamp).toLocaleTimeString()}
            </span>
          </div>
          <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">
            {getAgentDescription(step.agent)}
          </p>
          {step.result?.message && (
            <p className="text-sm text-gray-700 dark:text-gray-300">
              {step.result.message}
            </p>
          )}
        </div>
      ))}
    </div>
  )
}

