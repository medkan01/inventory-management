'use client'

import { useState } from 'react'
import Link from 'next/link'
import { createClient } from '@/lib/supabase/client'
import { 
  Card, 
  CardContent, 
  CardDescription, 
  CardHeader, 
  CardTitle 
} from '@/app/components/ui/Card'
import { Form, FormField, FormError, FormSuccess } from '@/app/components/ui/Form'
import Input from '@/app/components/ui/Input'
import Button from '@/app/components/ui/Button'
import PasswordStrengthIndicator from '@/app/components/ui/PasswordStrengthIndicator'
import { validatePassword, isPasswordValid } from '@/lib/utils/password-validation'

export default function SignupPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(false)

  const passwordValidation = validatePassword(password)
  const passwordRequirements = [
    { text: 'At least 8 characters', met: passwordValidation.minLength },
    { text: 'Contains uppercase letter (A-Z)', met: passwordValidation.hasUppercase },
    { text: 'Contains lowercase letter (a-z)', met: passwordValidation.hasLowercase },
    { text: 'Contains number (0-9)', met: passwordValidation.hasNumber },
    { text: 'Contains special character (!@#$%...)', met: passwordValidation.hasSpecialChar },
  ]

  const handleSignup = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)
    setSuccess(null)
    setIsLoading(true)

    // Validation
    if (password !== confirmPassword) {
      setError('Passwords do not match')
      setIsLoading(false)
      return
    }

    if (!isPasswordValid(passwordValidation)) {
      setError('Password does not meet all requirements')
      setIsLoading(false)
      return
    }

    try {
      const supabase = createClient()
      const { data, error } = await supabase.auth.signUp({
        email,
        password,
        options: {
          emailRedirectTo: `${window.location.origin}/auth/callback`,
        },
      })

      if (error) {
        setError(error.message)
        return
      }

      if (data.user) {
        // Check if email confirmation is required
        if (data.user.identities && data.user.identities.length === 0) {
          setError('An account with this email already exists')
        } else {
          setSuccess('Account created! Please check your email to confirm your account.')
          setEmail('')
          setPassword('')
          setConfirmPassword('')
        }
      }
    } catch {
      setError('An unexpected error occurred')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Create an account</CardTitle>
        <CardDescription>Sign up to get started with your inventory management</CardDescription>
      </CardHeader>
      <CardContent>
        <Form onSubmit={handleSignup}>
          <FormField>
            <Input
              label="Email"
              type="email"
              placeholder="you@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              disabled={isLoading}
              autoComplete="email"
            />
          </FormField>

          <FormField>
            <Input
              label="Password"
              type="password"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              disabled={isLoading}
              autoComplete="new-password"
            />
            <PasswordStrengthIndicator 
              requirements={passwordRequirements}
              show={true}
            />
          </FormField>

          <FormField>
            <Input
              label="Confirm Password"
              type="password"
              placeholder="••••••••"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              required
              disabled={isLoading}
              autoComplete="new-password"
            />
          </FormField>

          <FormError>{error}</FormError>
          <FormSuccess>{success}</FormSuccess>

          <Button
            type="submit"
            variant="primary"
            size="lg"
            className="w-full mt-2"
            isLoading={isLoading}
          >
            Create account
          </Button>
        </Form>

        <div className="mt-6 text-center">
          <p className="text-sm text-zinc-600 dark:text-zinc-400">
            Already have an account?{' '}
            <Link
              href="/login"
              className="font-medium text-zinc-900 dark:text-zinc-50 hover:underline"
            >
              Sign in
            </Link>
          </p>
        </div>
      </CardContent>
    </Card>
  )
}
