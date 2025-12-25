export { default as client } from './client'
export { getAccessToken, setAccessToken, getRefreshToken, setRefreshToken, clearTokens } from './client'
export { authApi } from './auth'
export { productsApi } from './products'
export { ordersApi } from './orders'
export { dealersApi } from './dealers'

export type { LoginRequest, LoginResponse, UserInfo, DealerInfo, CurrentUserResponse } from './auth'
export type { Product, ProductCreate, ProductUpdate, ProductsParams, PaginatedResponse } from './products'
export type { Order, OrderItem, OrderCreate, OrderItemCreate, OrdersParams, OrderStats } from './orders'
export type { Dealer, DealerCreate, DealerUpdate, DealersParams, DealerUser } from './dealers'

