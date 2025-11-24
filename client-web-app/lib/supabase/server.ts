import { createServerClient, type CookieOptions } from '@supabase/ssr'
import { cookies } from 'next/headers'

/**
 * Crée un client Supabase pour une utilisation côté serveur
 * Ce client est utilisé dans les Server Components, Server Actions, et Route Handlers
 */
export async function createClient() {
  const cookieStore = await cookies()

  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        get(name: string) {
          return cookieStore.get(name)?.value
        },
        set(name: string, value: string, options: CookieOptions) {
          try {
            cookieStore.set({ name, value, ...options })
          } catch {
            // La méthode `set` est appelée depuis un Server Component.
            // Cela peut être ignoré si vous avez un middleware qui rafraîchit les cookies.
          }
        },
        remove(name: string, options: CookieOptions) {
          try {
            cookieStore.set({ name, value: '', ...options })
          } catch {
            // La méthode `remove` est appelée depuis un Server Component.
            // Cela peut être ignoré si vous avez un middleware qui rafraîchit les cookies.
          }
        },
      },
    }
  )
}
