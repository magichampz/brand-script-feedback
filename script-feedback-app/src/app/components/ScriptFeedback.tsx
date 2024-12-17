'use client'

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { CheckCircle2 } from 'lucide-react'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export default function ScriptFeedback() {
  const [creativeBrief, setCreativeBrief] = useState("")
  const [script, setScript] = useState("")
  const [feedback, setFeedback] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [isScriptActive, setIsScriptActive] = useState(false)
  const [isValidated, setIsValidated] = useState(false)

  const handleNext = async () => {
    setIsLoading(true)
    try {
      const response = await fetch(`${API_URL}/validate-brief`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ brief: creativeBrief }),
        mode: 'cors',
      })
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      const data = await response.json()
      if (data.valid) {
        setIsScriptActive(true)
        setIsValidated(true)
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
      const response = await fetch(`${API_URL}/generate-feedback`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ brief: creativeBrief, script }),
        mode: 'cors',
      })
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
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
      <div className="space-y-2">
        <Textarea
          placeholder="Enter your creative brief here..."
          value={creativeBrief}
          onChange={(e) => setCreativeBrief(e.target.value)}
          className="min-h-[100px]"
        />
        <div className="flex items-center space-x-2">
          <Button onClick={handleNext} disabled={isLoading || creativeBrief.trim() === ""}>
            {isLoading ? 'Loading...' : 'Next'}
          </Button>
          {isValidated && <CheckCircle2 className="text-green-500" />}
        </div>
      </div>
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
      {feedback && (
        <div className="mt-4 p-4 bg-gray-100 rounded">
          <h2 className="text-xl font-semibold mb-2">Feedback:</h2>
          <p>{feedback}</p>
        </div>
      )}
    </div>
  )
}

