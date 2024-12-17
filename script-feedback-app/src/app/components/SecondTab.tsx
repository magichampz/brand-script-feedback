'use client'

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { PlusCircle, XCircle } from 'lucide-react'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export default function MultipleFeedbackPage() {
  const [feedbackEntries, setFeedbackEntries] = useState<string[]>([''])
  const [script, setScript] = useState("")
  const [combinedFeedback, setCombinedFeedback] = useState("")
  const [finalFeedback, setFinalFeedback] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [isScriptActive, setIsScriptActive] = useState(false)

  // Add a new feedback entry
  const addFeedbackEntry = () => {
    if (feedbackEntries.length < 10) {
      setFeedbackEntries([...feedbackEntries, ''])
    }
  }

  // Update feedback entry at index
  const updateFeedbackEntry = (index: number, value: string) => {
    const newEntries = [...feedbackEntries]
    newEntries[index] = value
    setFeedbackEntries(newEntries)
  }

  // Delete a feedback entry by index
  const deleteFeedbackEntry = (index: number) => {
    const newEntries = feedbackEntries.filter((_, i) => i !== index)
    setFeedbackEntries(newEntries)
  }

  // Handle processing of multiple feedbacks
  const handleProcessFeedbacks = async () => {
    setIsLoading(true)
    try {
      const response = await fetch(`${API_URL}/process-feedbacks`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ feedbacks: feedbackEntries }),
      })
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      const data = await response.json()
      setCombinedFeedback(data.combined_feedback)
      setIsScriptActive(true)
    } catch (error) {
      console.error('Error:', error)
      alert('An error occurred while processing feedbacks.')
    }
    setIsLoading(false)
  }

  // Handle script feedback generation
  const generateFeedback = async () => {
    setIsLoading(true)
    try {
      const response = await fetch(`${API_URL}/generate-feedback-2`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ script, combined_feedback: combinedFeedback }),
      })
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      const data = await response.json()
      setFinalFeedback(data.feedback)
    } catch (error) {
      console.error('Error:', error)
      alert('An error occurred while generating feedback.')
    }
    setIsLoading(false)
  }

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold">Process Multiple Feedbacks</h1>
      {feedbackEntries.map((entry, index) => (
        <div key={index} className="flex items-center space-x-2">
          <Textarea
            placeholder={`Feedback entry ${index + 1}`}
            value={entry}
            onChange={(e) => updateFeedbackEntry(index, e.target.value)}
            className="min-h-[100px] flex-1"
          />
          {index > 0 && (
            <button
              onClick={() => deleteFeedbackEntry(index)}
              className="text-red-500 hover:text-red-700"
              aria-label="Delete Entry"
            >
              <XCircle size={24} />
            </button>
          )}
        </div>
      ))}
      <div className="flex items-center space-x-2">
        <Button onClick={addFeedbackEntry} disabled={feedbackEntries.length >= 10}>
          <PlusCircle className="mr-2" /> Add Entry
        </Button>
        <Button onClick={handleProcessFeedbacks} disabled={isLoading || feedbackEntries.some(e => e.trim() === "")}>
          {isLoading ? 'Processing...' : 'Next'}
        </Button>
      </div>
      {combinedFeedback && (
        <div className="p-4 bg-gray-100 rounded mt-4">
          <h2 className="text-xl font-semibold mb-2">Combined Feedback:</h2>
          <p>{combinedFeedback}</p>
        </div>
      )}
      <Textarea
        placeholder="Enter your script here..."
        value={script}
        onChange={(e) => setScript(e.target.value)}
        className="min-h-[200px]"
        disabled={!isScriptActive}
      />
      <Button onClick={generateFeedback} disabled={isLoading || !isScriptActive || script.trim() === ""}>
        {isLoading ? 'Generating...' : 'Generate Feedback'}
      </Button>
      {finalFeedback && (
        <div className="mt-4 p-4 bg-gray-100 rounded">
          <h2 className="text-xl font-semibold mb-2">More Feedback:</h2>
          <p>{finalFeedback}</p>
        </div>
      )}
    </div>
  )
}