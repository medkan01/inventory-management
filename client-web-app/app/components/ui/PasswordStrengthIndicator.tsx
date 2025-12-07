import React from 'react'

interface PasswordRequirement {
  text: string
  met: boolean
}

interface PasswordStrengthIndicatorProps {
  requirements: PasswordRequirement[]
  show: boolean
}

export default function PasswordStrengthIndicator({ requirements, show }: PasswordStrengthIndicatorProps) {
  if (!show) return null

  return (
    <div className="mt-2 space-y-1.5">
      <p className="text-xs font-medium text-zinc-700 dark:text-zinc-300">
        Password requirements:
      </p>
      <ul className="space-y-1">
        {requirements.map((req, index) => (
          <li
            key={index}
            className={`text-xs flex items-center gap-1.5 ${
              req.met
                ? 'text-green-600 dark:text-green-400'
                : 'text-zinc-500 dark:text-zinc-500'
            }`}
          >
            <span className="flex-shrink-0">
              {req.met ? '✓' : '○'}
            </span>
            <span>{req.text}</span>
          </li>
        ))}
      </ul>
    </div>
  )
}
