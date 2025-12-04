import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'SigmaChain - Agentic Image Generation',
  description: 'Multi-agent system for intelligent image generation and validation',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}

