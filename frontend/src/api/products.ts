import client from './client'

export interface Product {
  id: string
  name: string
  category: string
  price: number
  unit: string
  min_order_quantity: number
  description?: string
  image_url?: string
  stock: number
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface ProductCreate {
  name: string
  category: string
  price: number
  unit: string
  min_order_quantity?: number
  description?: string
  stock?: number
  is_active?: boolean
}

export interface ProductUpdate {
  name?: string
  category?: string
  price?: number
  unit?: string
  min_order_quantity?: number
  description?: string
  stock?: number
  is_active?: boolean
}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  page_size: number
  pages: number
}

export interface ProductsParams {
  page?: number
  page_size?: number
  category?: string
  search?: string
}

export const productsApi = {
  list: async (params?: ProductsParams): Promise<PaginatedResponse<Product>> => {
    const response = await client.get<PaginatedResponse<Product>>('/products', { params })
    return response.data
  },

  get: async (id: string): Promise<Product> => {
    const response = await client.get<Product>(`/products/${id}`)
    return response.data
  },

  create: async (data: ProductCreate): Promise<Product> => {
    const response = await client.post<Product>('/products', data)
    return response.data
  },

  update: async (id: string, data: ProductUpdate): Promise<Product> => {
    const response = await client.put<Product>(`/products/${id}`, data)
    return response.data
  },

  delete: async (id: string): Promise<void> => {
    await client.delete(`/products/${id}`)
  },

  uploadImage: async (id: string, file: File): Promise<Product> => {
    const formData = new FormData()
    formData.append('file', file)
    const response = await client.post<Product>(`/products/${id}/image`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    return response.data
  },

  getCategories: async (): Promise<string[]> => {
    const response = await client.get<{ categories: string[] }>('/products/categories')
    return response.data.categories
  },
}

