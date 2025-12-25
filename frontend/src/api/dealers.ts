import client from './client'
import type { PaginatedResponse } from './products'

export interface DealerUser {
  id: string
  username: string
  email: string
  is_active: boolean
}

export interface Dealer {
  id: string
  company_name: string
  contact_name: string
  phone: string
  address?: string
  status: string
  created_at: string
  user: DealerUser
}

export interface DealerCreate {
  username: string
  email: string
  password: string
  company_name: string
  contact_name: string
  phone: string
  address?: string
  status?: string
}

export interface DealerUpdate {
  company_name?: string
  contact_name?: string
  phone?: string
  address?: string
}

export interface DealersParams {
  page?: number
  page_size?: number
  status?: string
  search?: string
}

export const dealersApi = {
  list: async (params?: DealersParams): Promise<PaginatedResponse<Dealer>> => {
    const response = await client.get<PaginatedResponse<Dealer>>('/dealers', { params })
    return response.data
  },

  get: async (id: string): Promise<Dealer> => {
    const response = await client.get<Dealer>(`/dealers/${id}`)
    return response.data
  },

  create: async (data: DealerCreate): Promise<Dealer> => {
    const response = await client.post<Dealer>('/dealers', data)
    return response.data
  },

  update: async (id: string, data: DealerUpdate): Promise<Dealer> => {
    const response = await client.put<Dealer>(`/dealers/${id}`, data)
    return response.data
  },

  updateStatus: async (id: string, status: string): Promise<Dealer> => {
    const response = await client.put<Dealer>(`/dealers/${id}/status`, { status })
    return response.data
  },

  delete: async (id: string): Promise<void> => {
    await client.delete(`/dealers/${id}`)
  },
}

