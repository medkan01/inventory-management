'use client'

import { useAuth } from '@/app/contexts'
import { useRouter } from 'next/navigation'
import Button from '@/app/components/ui/Button'

export default function Home() {
  const { user, loading, signOut } = useAuth()
  const router = useRouter()

  const handleSignOut = async () => {
    await signOut()
    router.push('/login')
  }

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-zinc-50 dark:bg-zinc-950">
        <p className="text-zinc-600 dark:text-zinc-400">Loading...</p>
      </div>
    )
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-zinc-50 dark:bg-zinc-950 p-4">
      <div className="w-full max-w-2xl">
        <div className="bg-white dark:bg-zinc-900 rounded-lg shadow-sm border border-zinc-200 dark:border-zinc-800 p-8">
          <h1 className="text-3xl font-semibold text-zinc-900 dark:text-zinc-50 mb-2">
            Inventory Management
          </h1>
          <p className="text-zinc-600 dark:text-zinc-400 mb-6">
            Welcome to your inventory management system
          </p>

          {user ? (
            <div className="space-y-4">
              <div className="p-4 bg-zinc-50 dark:bg-zinc-800 rounded-lg">
                <p className="text-sm text-zinc-600 dark:text-zinc-400">Logged in as:</p>
                <p className="text-lg font-medium text-zinc-900 dark:text-zinc-50">
                  {user.email}
                </p>
              </div>
              <Button onClick={handleSignOut} variant="outline" className="w-full">
                Sign Out
              </Button>
            </div>
          ) : (
            <div className="space-y-4">
              <p className="text-zinc-600 dark:text-zinc-400">
                Please sign in to access your inventory
              </p>
              <div className="flex gap-4">
                <Button onClick={() => router.push('/login')} className="flex-1">
                  Sign In
                </Button>
                <Button onClick={() => router.push('/signup')} variant="outline" className="flex-1">
                  Sign Up
                </Button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
