import React from 'react'

export interface FormProps extends React.FormHTMLAttributes<HTMLFormElement> {
  children: React.ReactNode
}

export function Form({ children, className = '', ...props }: FormProps) {
  return (
    <form className={`space-y-4 ${className}`} {...props}>
      {children}
    </form>
  )
}

export interface FormFieldProps {
  children: React.ReactNode
  className?: string
}

export function FormField({ children, className = '' }: FormFieldProps) {
  return (
    <div className={`${className}`}>
      {children}
    </div>
  )
}

export interface FormErrorProps {
  children: React.ReactNode
  className?: string
}

export function FormError({ children, className = '' }: FormErrorProps) {
  if (!children) return null
  
  return (
    <div className={`mt-4 p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg ${className}`}>
      <p className="text-sm text-red-800 dark:text-red-200">
        {children}
      </p>
    </div>
  )
}

export interface FormSuccessProps {
  children: React.ReactNode
  className?: string
}

export function FormSuccess({ children, className = '' }: FormSuccessProps) {
  if (!children) return null
  
  return (
    <div className={`mt-4 p-3 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg ${className}`}>
      <p className="text-sm text-green-800 dark:text-green-200">
        {children}
      </p>
    </div>
  )
}
