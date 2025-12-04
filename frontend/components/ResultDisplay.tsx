'use client'

interface ValidationResult {
  overall_score?: number
  anatomical_score?: number
  quality_score?: number
  issues?: string[]
  recommendations?: string[]
  passed?: boolean
  detailed_analysis?: string
}

interface WorkflowResult {
  success: boolean
  workflow_id: string
  result: {
    original_prompt: string
    enhanced_prompt: string
    image_url: string
    validation: ValidationResult
    passed_validation: boolean
  }
  message: string
}

interface ResultDisplayProps {
  result: WorkflowResult
}

export default function ResultDisplay({ result }: ResultDisplayProps) {
  const validation = result.result.validation || {}

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
        Generated Image
      </h2>

      <div className="grid md:grid-cols-2 gap-6">
        <div className="space-y-4">
          <div>
            <h3 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Original Prompt
            </h3>
            <p className="text-sm text-gray-900 dark:text-white bg-gray-50 dark:bg-gray-700 p-3 rounded">
              {result.result.original_prompt}
            </p>
          </div>

          <div>
            <h3 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Enhanced Prompt
            </h3>
            <p className="text-sm text-gray-900 dark:text-white bg-gray-50 dark:bg-gray-700 p-3 rounded">
              {result.result.enhanced_prompt}
            </p>
          </div>
        </div>

        <div>
          <h3 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Generated Image
          </h3>
          {result.result.image_url && (
            <div className="relative rounded-lg overflow-hidden border border-gray-200 dark:border-gray-700">
              <img
                src={result.result.image_url.startsWith('http') 
                  ? result.result.image_url 
                  : `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}${result.result.image_url}`}
                alt="Generated image"
                className="w-full h-auto"
              />
            </div>
          )}
        </div>
      </div>

      <div className="border-t border-gray-200 dark:border-gray-700 pt-6">
        <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-4">
          Validation Results
        </h3>

        <div className="grid md:grid-cols-3 gap-4 mb-6">
          <div className="bg-blue-50 dark:bg-blue-900/20 p-4 rounded-lg">
            <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">
              Overall Score
            </p>
            <p className="text-2xl font-bold text-blue-600 dark:text-blue-400">
              {validation.overall_score ?? 'N/A'}
            </p>
          </div>
          <div className="bg-green-50 dark:bg-green-900/20 p-4 rounded-lg">
            <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">
              Anatomical Score
            </p>
            <p className="text-2xl font-bold text-green-600 dark:text-green-400">
              {validation.anatomical_score ?? 'N/A'}
            </p>
          </div>
          <div className="bg-purple-50 dark:bg-purple-900/20 p-4 rounded-lg">
            <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">
              Quality Score
            </p>
            <p className="text-2xl font-bold text-purple-600 dark:text-purple-400">
              {validation.quality_score ?? 'N/A'}
            </p>
          </div>
        </div>

        <div
          className={`p-4 rounded-lg mb-4 ${
            result.result.passed_validation
              ? 'bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800'
              : 'bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800'
          }`}
        >
          <p className="font-semibold text-gray-900 dark:text-white mb-2">
            Validation Status:{' '}
            <span
              className={
                result.result.passed_validation
                  ? 'text-green-600 dark:text-green-400'
                  : 'text-yellow-600 dark:text-yellow-400'
              }
            >
              {result.result.passed_validation ? 'PASSED' : 'REVIEW NEEDED'}
            </span>
          </p>
        </div>

        {validation.issues && validation.issues.length > 0 && (
          <div className="mb-4">
            <h4 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Issues Found
            </h4>
            <ul className="list-disc list-inside space-y-1 text-sm text-gray-600 dark:text-gray-400">
              {validation.issues.map((issue, index) => (
                <li key={index}>{issue}</li>
              ))}
            </ul>
          </div>
        )}

        {validation.recommendations && validation.recommendations.length > 0 && (
          <div className="mb-4">
            <h4 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Recommendations
            </h4>
            <ul className="list-disc list-inside space-y-1 text-sm text-gray-600 dark:text-gray-400">
              {validation.recommendations.map((rec, index) => (
                <li key={index}>{rec}</li>
              ))}
            </ul>
          </div>
        )}

        {validation.detailed_analysis && (
          <div>
            <h4 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Detailed Analysis
            </h4>
            <p className="text-sm text-gray-600 dark:text-gray-400 bg-gray-50 dark:bg-gray-700 p-3 rounded">
              {validation.detailed_analysis}
            </p>
          </div>
        )}
      </div>
    </div>
  )
}

