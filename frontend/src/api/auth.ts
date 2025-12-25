import client, { setAccessToken, setRefreshToken, clearTokens } from './client'

export interface LoginRequest {
  username: string
  password: string
}

export interface DealerInfo {
  id: string
  company_name: string
  contact_name: string
  phone: string
  address?: string
  status: string
}

export interface UserInfo {
  id: string
  username: string
  email: string
  role: string
  is_active: boolean
  dealer?: DealerInfo
}

export interface LoginResponse {
  access_token: string
  refresh_token: string
  token_type: string
  user: UserInfo
}

export interface CurrentUserResponse extends UserInfo {
  created_at: string
  updated_at: string
}

export const authApi = {
  login: async (data: LoginRequest): Promise<LoginResponse> => {
    const response = await client.post<LoginResponse>('/auth/login', data)
    const { access_token, refresh_token } = response.data
    setAccessToken(access_token)
    setRefreshToken(refresh_token)
    return response.data
  },

  logout: async (): Promise<void> => {
    try {
      await client.post('/auth/logout')
    } finally {
      clearTokens()
    }
  },

  getCurrentUser: async (): Promise<CurrentUserResponse> => {
    const response = await client.get<CurrentUserResponse>('/auth/me')
    return response.data
  },

  refresh: async (refreshToken: string): Promise<{ access_token: string; refresh_token: string }> => {
    const response = await client.post('/auth/refresh', { refresh_token: refreshToken })
    return response.data
  },
}

