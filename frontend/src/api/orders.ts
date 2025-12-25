import client from './client'
import type { PaginatedResponse } from './products'

export interface OrderItem {
  id: string
  order_id: string
  product_id: string
  product_name: string
  quantity: number
  unit_price: number
  subtotal: number
}

export interface Order {
  id: string
  order_no: string
  dealer_id: string
  dealer_company?: string
  status: string
  total_amount: number
  shipping_address: string
  notes?: string
  created_at: string
  updated_at: string
  items: OrderItem[]
}

export interface OrderItemCreate {
  product_id: string
  product_name: string
  quantity: number
  unit_price: number
}

export interface OrderCreate {
  items: OrderItemCreate[]
  shipping_address: string
  notes?: string
}

export interface OrdersParams {
  page?: number
  page_size?: number
  status?: string
  order_no?: string
}

export interface OrderStats {
  status_counts: Record<string, number>
  total_revenue: number
  today_orders: number
  recent_orders: Array<{
    id: string
    order_no: string
    status: string
    total_amount: number
    created_at: string
    dealer_company: string
  }>
}

export const ordersApi = {
  list: async (params?: OrdersParams): Promise<PaginatedResponse<Order>> => {
    const response = await client.get<PaginatedResponse<Order>>('/orders', { params })
    return response.data
  },

  get: async (id: string): Promise<Order> => {
    const response = await client.get<Order>(`/orders/${id}`)
    return response.data
  },

  create: async (data: OrderCreate): Promise<Order> => {
    const response = await client.post<Order>('/orders', data)
    return response.data
  },

  updateStatus: async (id: string, status: string): Promise<Order> => {
    const response = await client.put<Order>(`/orders/${id}/status`, { status })
    return response.data
  },

  cancel: async (id: string): Promise<Order> => {
    const response = await client.delete<Order>(`/orders/${id}`)
    return response.data
  },

  getStats: async (): Promise<OrderStats> => {
    const response = await client.get<OrderStats>('/orders/stats')
    return response.data
  },
}

