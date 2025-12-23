// 欣与甜 E-Shop - Frontend JavaScript

// API Base URL - always use relative path (proxied through nginx)
const API_BASE = '';

// Storage key for search history
const STORAGE_KEY = window.location.host + '_search_log';

// DOM Elements
let searchForm;
let queryInput;
let searchHistorySection;
let historyList;
let clearHistoryBtn;
let resultsSection;
let resultsContainer;
let errorMessage;
let productCategories;

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    // Get DOM elements
    searchForm = document.getElementById('searchForm');
    queryInput = document.getElementById('queryInput');
    searchHistorySection = document.getElementById('searchHistory');
    historyList = document.getElementById('historyList');
    clearHistoryBtn = document.getElementById('clearHistory');
    resultsSection = document.getElementById('resultsSection');
    resultsContainer = document.getElementById('results');
    errorMessage = document.getElementById('errorMessage');
    productCategories = document.getElementById('productCategories');

    // Setup event listeners
    if (searchForm) {
        searchForm.addEventListener('submit', handleSearch);
    }
    if (clearHistoryBtn) {
        clearHistoryBtn.addEventListener('click', clearSearchHistory);
    }

    // Load initial data
    loadSearchHistory();
    loadProductCategories();

    console.log('欣与甜 E-Shop initialized');
});

// ==================== Search Functionality ====================

async function handleSearch(e) {
    e.preventDefault();
    
    const query = queryInput.value.trim();
    if (!query) {
        showError('请输入查询内容');
        return;
    }

    // Save to history
    saveToHistory(query);

    // Show loading
    showResults('<div class="loading">搜索中...</div>');

    try {
        const response = await fetch(`${API_BASE}/api/orders/search`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query_str: query }),
        });

        if (!response.ok) {
            throw new Error('Search failed');
        }

        const orders = await response.json();
        displayOrderResults(orders);
    } catch (error) {
        console.error('Search error:', error);
        showError('查询失败，请稍后重试');
    }
}

function displayOrderResults(orders) {
    if (!orders || orders.length === 0) {
        showResults('<div class="empty-state">未找到匹配的订单，请检查查询条件</div>');
        return;
    }

    let html = '';
    for (const order of orders) {
        html += renderOrderCard(order);
    }
    showResults(html);
}

function renderOrderCard(order) {
    const statusClass = getStatusClass(order.status);
    
    let trackingHtml = '';
    if (order.tracking_history && order.tracking_history.length > 0) {
        trackingHtml = '<div class="tracking-timeline">';
        // Show most recent first
        const history = [...order.tracking_history].reverse();
        for (const event of history) {
            trackingHtml += `
                <div class="tracking-item">
                    <div class="tracking-time">${event.time}</div>
                    <div class="tracking-location">${event.location}</div>
                    <div class="tracking-status">${event.status}</div>
                </div>
            `;
        }
        trackingHtml += '</div>';
    } else if (order.status === '待发货') {
        trackingHtml = '<div class="text-slate-400 text-sm mt-6 flex items-center gap-2 bg-slate-50 p-4 rounded-xl border border-slate-100"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg> 暂无物流信息，等待发货中...</div>';
    }

    return `
        <div class="order-card">
            <div class="order-card-header">
                <div class="flex-1">
                    <div class="text-xs font-bold text-amber-600 uppercase tracking-widest mb-1">Product Details</div>
                    <div class="font-bold text-slate-900 text-lg">${order.product_name}</div>
                    <div class="text-xs font-medium text-slate-400 mt-1 flex items-center gap-1">
                        <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path></svg>
                        ID: ${order.order_id}
                    </div>
                </div>
                <span class="order-status ${statusClass}">${order.status}</span>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 bg-slate-50/50 p-4 rounded-2xl border border-slate-100">
                <div class="space-y-1">
                    <div class="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Recipient</div>
                    <div class="text-sm font-semibold text-slate-700">${order.recipient_name}</div>
                </div>
                <div class="space-y-1">
                    <div class="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Phone Number</div>
                    <div class="text-sm font-semibold text-slate-700">${maskPhone(order.recipient_phone)}</div>
                </div>
                <div class="space-y-1">
                    <div class="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Carrier</div>
                    <div class="text-sm font-semibold text-slate-700">${order.courier}</div>
                </div>
                <div class="space-y-1">
                    <div class="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Tracking Number</div>
                    <div class="text-sm font-semibold text-slate-700">${order.tracking_number}</div>
                </div>
            </div>
            ${trackingHtml}
        </div>
    `;
}

function getStatusClass(status) {
    const statusMap = {
        '待发货': 'status-pending',
        '已发货': 'status-shipped',
        '运输中': 'status-transit',
        '派送中': 'status-delivering',
        '已签收': 'status-delivered',
    };
    return statusMap[status] || 'status-pending';
}

function maskPhone(phone) {
    if (!phone || phone.length < 7) return phone;
    return phone.substring(0, 3) + '****' + phone.substring(7);
}

function showResults(html) {
    hideError();
    resultsSection.classList.remove('hidden');
    resultsContainer.innerHTML = html;
}

function showError(message) {
    resultsSection.classList.remove('hidden');
    resultsContainer.innerHTML = '';
    errorMessage.textContent = message;
    errorMessage.classList.remove('hidden');
}

function hideError() {
    errorMessage.classList.add('hidden');
}

// ==================== Search History ====================

function loadSearchHistory() {
    const history = getHistory();
    if (history.length === 0) {
        searchHistorySection.classList.add('hidden');
        return;
    }

    renderHistory(history);
    searchHistorySection.classList.remove('hidden');
}

function getHistory() {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (!stored) return [];
    return stored.split(',').filter(item => item.trim());
}

function saveToHistory(query) {
    let history = getHistory();
    
    // Remove if already exists
    history = history.filter(item => item !== query);
    
    // Add to front
    history.unshift(query);
    
    // Limit to 10 items
    if (history.length > 10) {
        history = history.slice(0, 10);
    }
    
    localStorage.setItem(STORAGE_KEY, history.join(','));
    loadSearchHistory();
}

function renderHistory(history) {
    historyList.innerHTML = history.map(item => 
        `<span class="history-pill" data-query="${escapeHtml(item)}">${escapeHtml(item)}</span>`
    ).join('');

    // Add click handlers
    historyList.querySelectorAll('.history-pill').forEach(pill => {
        pill.addEventListener('click', function() {
            const query = this.dataset.query;
            queryInput.value = query;
            searchForm.dispatchEvent(new Event('submit'));
        });
    });
}

function clearSearchHistory() {
    localStorage.removeItem(STORAGE_KEY);
    searchHistorySection.classList.add('hidden');
    historyList.innerHTML = '';
}

// ==================== Product Categories ====================

async function loadProductCategories() {
    try {
        const response = await fetch(`${API_BASE}/api/products`);
        if (!response.ok) {
            throw new Error('Failed to load products');
        }
        const products = await response.json();
        displayProductCategories(products);
    } catch (error) {
        console.error('Error loading products:', error);
        productCategories.innerHTML = '<div class="col-span-2 text-center text-gray-500">加载产品分类失败</div>';
    }
}

function displayProductCategories(products) {
    if (!products || products.length === 0) {
        productCategories.innerHTML = '<div class="col-span-2 text-center text-gray-500">暂无产品分类</div>';
        return;
    }

    productCategories.innerHTML = products.map(product => 
        `<a href="product.html?id=${product.product_id}" class="product-btn">${escapeHtml(product.name)}</a>`
    ).join('');
}

// ==================== Utilities ====================

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
