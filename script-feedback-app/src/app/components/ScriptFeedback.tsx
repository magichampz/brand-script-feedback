'use client'

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"

export default function ScriptFeedback() {
  const [step, setStep] = useState<1 | 2>(1)
  const [creativeBrief, setCreativeBrief] = useState("")
  const [script, setScript] = useState("")
  const [feedback, setFeedback] = useState("")
  const [isLoading, setIsLoading] = useState(false)

  const handleNext = async () => {
    setIsLoading(true)
    try {
      const response = await fetch('http://localhost:8000/validate-brief', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ brief: creativeBrief }),
      })
      const data = await response.json()
      if (data.valid) {
        setStep(2)
      } else {
        alert('Please provide a valid creative brief.')
      }
    } catch (error) {
      console.error('Error:', error)
      alert('An error occurred. Please try again.')
    }
    setIsLoading(false)
  }

  const generateFeedback = async () => {
    setIsLoading(true)
    try {
      const response = await fetch('http://localhost:8000/generate-feedback', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ brief: creativeBrief, script }),
      })
      const data = await response.json()
      setFeedback(data.feedback)
    } catch (error) {
      console.error('Error:', error)
      alert('An error occurred. Please try again.')
    }
    setIsLoading(false)
  }

  return (
    <div className="space-y-4">
      {step === 1 && (
        <>
          <Textarea
            placeholder="Enter your creative brief here..."
            value={creativeBrief}
            onChange={(e) => setCreativeBrief(e.target.value)}
            className="min-h-[100px]"
          />
          <Button onClick={handleNext} disabled={isLoading || creativeBrief.trim() === ""}>
            {isLoading ? 'Loading...' : 'Next'}
          </Button>
        </>
      )}
      {step === 2 && (
        <>
          <Textarea
            placeholder="Enter your script here..."
            value={script}
            onChange={(e) => setScript(e.target.value)}
            className="min-h-[200px]"
          />
          <Button onClick={generateFeedback} disabled={isLoading || script.trim() === ""}>
            {isLoading ? 'Generating...' : 'Generate Feedback'}
          </Button>
        </>
      )}
      {feedback && (
        <div className="mt-4 p-4 bg-gray-100 rounded">
          <h2 className="text-xl font-semibold mb-2">Feedback:</h2>
          <p>{feedback}</p>
        </div>
      )}
    </div>
  )
}

