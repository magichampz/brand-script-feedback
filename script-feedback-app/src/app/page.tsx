'use client'

import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import ScriptFeedback from "./components/ScriptFeedback"
import SecondTab from "./components/SecondTab"

export default function Home() {
  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Video Script Feedback Generator</h1>
      <Tabs defaultValue="tab1">
        <TabsList>
          <TabsTrigger value="tab1">Feedback Generator 1</TabsTrigger>
          <TabsTrigger value="tab2">Feedback Generator 2</TabsTrigger>
        </TabsList>
        <TabsContent value="tab1">
          <ScriptFeedback />
        </TabsContent>
        <TabsContent value="tab2">
          <SecondTab />
        </TabsContent>
      </Tabs>
    </div>
  )
}

