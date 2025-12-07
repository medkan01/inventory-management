export interface PasswordValidation {
  minLength: boolean
  hasUppercase: boolean
  hasLowercase: boolean
  hasNumber: boolean
  hasSpecialChar: boolean
}

export function validatePassword(password: string): PasswordValidation {
  return {
    minLength: password.length >= 8,
    hasUppercase: /[A-Z]/.test(password),
    hasLowercase: /[a-z]/.test(password),
    hasNumber: /[0-9]/.test(password),
    hasSpecialChar: /[!@#$%^&*(),.?":{}|<>]/.test(password),
  }
}

export function isPasswordValid(validation: PasswordValidation): boolean {
  return Object.values(validation).every(Boolean)
}

export function getPasswordStrength(validation: PasswordValidation): 'weak' | 'medium' | 'strong' {
  const validCount = Object.values(validation).filter(Boolean).length
  
  if (validCount <= 2) return 'weak'
  if (validCount <= 4) return 'medium'
  return 'strong'
}
