// 全局变量
const UNSPLASH_ACCESS_KEY = 'YOUR_UNSPLASH_ACCESS_KEY'; // 需要替换为实际的API密钥
let heroSwiper, attractionsSwiper;

// 景点数据
const attractionsData = [
    {
        name: '黄果树瀑布',
        description: '中国最大的瀑布群，气势磅礴，声震数里，被誉为"中华第一瀑"。',
        image: 'https://www.bijingdi.com/uploadfile/2022/0803/20220803000539164.jpg?w=500&h=300&fit=crop',
        keywords: 'Huangguoshu waterfall China'
    },
    {
        name: '西江千户苗寨',
        description: '世界最大的苗族聚居村寨，保存完整的苗族原生态文化。',
        image: 'https://youimg1.c-ctrip.com/target/100f12000000t34rv1058.jpg?w=500&h=300&fit=crop',
        keywords: 'Xijiang Miao village China'
    },
    {
        name: '梵净山',
        description: '世界自然遗产，中国佛教名山，生物多样性保护区。',
        image: 'https://tr-osdcp.qunarzz.com/tr-osd-tr-space/img/5dd89b2d96428a6ed0cd3ada938638d9.jpg?w=500&h=300&fit=crop',
        keywords: 'Fanjing mountain China'
    },
    {
        name: '遵义会址',
        description: '中国革命历史的重要转折点，红色旅游经典景区。',
        image: 'https://youimg1.c-ctrip.com/target/100t160000010mc8q2B3D.jpg?w=500&h=300&fit=crop',
        keywords: 'Zunyi conference site China'
    },
    {
        name: '荔波小七孔',
        description: '世界自然遗产，被誉为"地球上的绿宝石"。',
        image: 'https://youimg1.c-ctrip.com/target/10041f000001gp8t70511_D_10000_1200.jpg?w=500&h=300&fit=crop',
        keywords: 'Libo Xiaoqikong China'
    },
    {
        name: '镇远古镇',
        description: '有着2000多年历史的古镇，山水城浑然一体。',
        image: 'https://img1.qunarzz.com/travel/d7/1511/5a/802fff6cad7e2df7.jpg?w=500&h=300&fit=crop',
        keywords: 'Zhenyuan ancient town China'
    }
];

// 搜索建议关键词
const searchSuggestions = [
    '梵净山', '黄果树瀑布', '西江千户苗寨', '荔波小七孔', 
    '遵义会址', '镇远古镇', '贵州山水', '苗族文化', 
    '贵州风景', '瀑布', '古镇', '山峰'
];

// DOM加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

// 初始化应用
function initializeApp() {
    initializeNavigation();
    initializeHeroCarousel();
    initializeAttractionsCarousel();
    initializeImageSearch();
    initializeForm();
    loadHeroImages();
    loadRecentConsultations();
}

// 导航栏功能
function initializeNavigation() {
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');
    const navLinks = document.querySelectorAll('.nav-link');

    // 移动端菜单切换
    hamburger.addEventListener('click', () => {
        hamburger.classList.toggle('active');
        navMenu.classList.toggle('active');
    });

    // 导航链接点击处理
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('href');
            
            // 更新活跃状态
            navLinks.forEach(l => l.classList.remove('active'));
            link.classList.add('active');
            
            // 平滑滚动到目标区域
            if (targetId.startsWith('#')) {
                const targetElement = document.querySelector(targetId);
                if (targetElement) {
                    targetElement.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
            
            // 关闭移动端菜单
            hamburger.classList.remove('active');
            navMenu.classList.remove('active');
        });
    });

    // 滚动时更新导航高亮
    window.addEventListener('scroll', updateActiveNavigation);
}

// 更新导航栏活跃状态
function updateActiveNavigation() {
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-link');
    
    let current = '';
    sections.forEach(section => {
        const sectionTop = section.offsetTop - 100;
        if (window.pageYOffset >= sectionTop) {
            current = section.getAttribute('id');
        }
    });

    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === `#${current}`) {
            link.classList.add('active');
        }
    });
}

// 初始化首页轮播
function initializeHeroCarousel() {
    heroSwiper = new Swiper('.hero-carousel', {
        loop: true,
        autoplay: {
            delay: 5000,
            disableOnInteraction: false,
        },
        pagination: {
            el: '.swiper-pagination',
            clickable: true,
        },
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },
        effect: 'fade',
        fadeEffect: {
            crossFade: true
        }
    });
}

// 初始化景点轮播
function initializeAttractionsCarousel() {
    // 生成景点卡片
    const attractionsWrapper = document.getElementById('attractions-wrapper');
    attractionsWrapper.innerHTML = attractionsData.map(attraction => `
        <div class="swiper-slide">
            <div class="attraction-card">
                <div class="attraction-image" style="background-image: url('${attraction.image}')"></div>
                <div class="attraction-content">
                    <h3>${attraction.name}</h3>
                    <p>${attraction.description}</p>
                    <button class="attraction-btn" onclick="viewAttractionDetails('${attraction.name}')">
                        查看详情
                    </button>
                </div>
            </div>
        </div>
    `).join('');

    // 初始化轮播
    attractionsSwiper = new Swiper('.attractions-carousel', {
        slidesPerView: 1,
        spaceBetween: 20,
        loop: true,
        autoplay: {
            delay: 4000,
            disableOnInteraction: false,
        },
        pagination: {
            el: '.attractions-section .swiper-pagination',
            clickable: true,
        },
        breakpoints: {
            640: {
                slidesPerView: 2,
            },
            1024: {
                slidesPerView: 3,
            }
        }
    });
}

// 加载首页轮播图片
async function loadHeroImages() {
    const heroKeywords = [
        'Guizhou waterfall China',
        'Qianhu Miao Village China',
        'Fanjing mountain China'
    ];

    for (let i = 0; i < heroKeywords.length; i++) {
        try {
            const imageUrl = await fetchUnsplashImage(heroKeywords[i]);
            const heroImage = document.getElementById(`hero-image-${i + 1}`);
            if (heroImage && imageUrl) {
                heroImage.style.backgroundImage = `url('${imageUrl}')`;
            }
        } catch (error) {
            console.error(`加载首页图片 ${i + 1} 失败:`, error);
            // 使用默认图片
            const heroImage = document.getElementById(`hero-image-${i + 1}`);
            if (heroImage) {
                heroImage.style.backgroundImage = `url('https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=600&h=400&fit=crop')`;
            }
        }
    }
}

// 初始化图片搜索功能
function initializeImageSearch() {
    const searchInput = document.getElementById('image-search');
    const searchBtn = document.getElementById('search-btn');
    const suggestionsContainer = document.getElementById('search-suggestions');

    // 搜索按钮点击事件
    searchBtn.addEventListener('click', handleImageSearch);
    
    // 回车键搜索
    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            handleImageSearch();
        }
    });

    // 实时搜索建议
    searchInput.addEventListener('input', (e) => {
        const query = e.target.value.trim();
        if (query.length > 0) {
            showSearchSuggestions(query);
        } else {
            hideSuggestions();
        }
    });

    // 点击其他地方隐藏建议
    document.addEventListener('click', (e) => {
        if (!e.target.closest('.search-container')) {
            hideSuggestions();
        }
    });
}

// 显示搜索建议
function showSearchSuggestions(query) {
    const suggestionsContainer = document.getElementById('search-suggestions');
    const filteredSuggestions = searchSuggestions.filter(suggestion => 
        suggestion.toLowerCase().includes(query.toLowerCase())
    );

    if (filteredSuggestions.length > 0) {
        suggestionsContainer.innerHTML = filteredSuggestions.map(suggestion => 
            `<div class="suggestion-item" onclick="selectSuggestion('${suggestion}')">${suggestion}</div>`
        ).join('');
        suggestionsContainer.style.display = 'block';
    } else {
        hideSuggestions();
    }
}

// 选择搜索建议
function selectSuggestion(suggestion) {
    document.getElementById('image-search').value = suggestion;
    hideSuggestions();
    handleImageSearch();
}

// 隐藏搜索建议
function hideSuggestions() {
    document.getElementById('search-suggestions').style.display = 'none';
}

// 处理图片搜索
async function handleImageSearch() {
    const query = document.getElementById('image-search').value.trim();
    if (!query) {
        showNotification('请输入搜索关键词', 'warning');
        return;
    }

    const gallery = document.getElementById('image-gallery');
    const loading = document.getElementById('loading');
    
    // 显示加载状态
    gallery.innerHTML = '<div class="loading">正在搜索图片...</div>';
    
    try {
        const images = await searchUnsplashImages(query);
        displayImageGallery(images);
    } catch (error) {
        console.error('图片搜索失败:', error);
        gallery.innerHTML = `
            <div class="loading">
                搜索失败，请稍后重试。<br>
                <small>提示：由于API限制，当前显示示例图片</small>
            </div>
        `;
        // 显示示例图片
        displaySampleImages(query);
    }
}

// 从Unsplash获取单张图片
async function fetchUnsplashImage(query) {
    // 由于API密钥限制，这里返回示例图片URL
    const sampleImages = [
        'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=600&h=400&fit=crop',
        'https://images.unsplash.com/photo-1469474968028-56623f02e42e?w=600&h=400&fit=crop',
        'https://images.unsplash.com/photo-1551632811-561732d1e306?w=600&h=400&fit=crop',
        'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=600&h=400&fit=crop'
    ];
    
    return sampleImages[Math.floor(Math.random() * sampleImages.length)];
}

// 从Unsplash搜索图片
async function searchUnsplashImages(query) {
    // 模拟API响应，返回示例数据
    const sampleImages = [
        {
            id: '1',
            urls: { regular: 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400&h=300&fit=crop' },
            alt_description: `${query}风景`,
            user: { name: 'Unsplash用户1' }
        },
        {
            id: '2',
            urls: { regular: 'https://images.unsplash.com/photo-1469474968028-56623f02e42e?w=400&h=300&fit=crop' },
            alt_description: `${query}美景`,
            user: { name: 'Unsplash用户2' }
        },
        {
            id: '3',
            urls: { regular: 'https://images.unsplash.com/photo-1551632811-561732d1e306?w=400&h=300&fit=crop' },
            alt_description: `${query}景观`,
            user: { name: 'Unsplash用户3' }
        },
        {
            id: '4',
            urls: { regular: 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=400&h=300&fit=crop' },
            alt_description: `${query}自然风光`,
            user: { name: 'Unsplash用户4' }
        }
    ];
    
    return sampleImages;
}

// 显示示例图片
function displaySampleImages(query) {
    setTimeout(() => {
        const sampleImages = [
            {
                id: '1',
                urls: { regular: 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400&h=300&fit=crop' },
                alt_description: `${query}风景`,
                user: { name: '示例用户1' }
            },
            {
                id: '2',
                urls: { regular: 'https://images.unsplash.com/photo-1469474968028-56623f02e42e?w=400&h=300&fit=crop' },
                alt_description: `${query}美景`,
                user: { name: '示例用户2' }
            },
            {
                id: '3',
                urls: { regular: 'https://images.unsplash.com/photo-1551632811-561732d1e306?w=400&h=300&fit=crop' },
                alt_description: `${query}景观`,
                user: { name: '示例用户3' }
            }
        ];
        displayImageGallery(sampleImages);
    }, 1000);
}

// 显示图片画廊
function displayImageGallery(images) {
    const gallery = document.getElementById('image-gallery');
    
    if (images.length === 0) {
        gallery.innerHTML = '<div class="loading">未找到相关图片</div>';
        return;
    }

    gallery.innerHTML = images.map(image => `
        <div class="image-card">
            <img src="${image.urls.regular}" alt="${image.alt_description || '贵州风景'}" loading="lazy">
            <div class="image-info">
                <h4>${image.alt_description || '贵州美景'}</h4>
                <p>图片来源: ${image.user.name} / Unsplash</p>
            </div>
        </div>
    `).join('');
}

// 初始化表单功能
function initializeForm() {
    const form = document.getElementById('tourism-form');
    const inputs = form.querySelectorAll('input, select, textarea');

    // 表单提交处理
    form.addEventListener('submit', handleFormSubmit);

    // 实时验证
    inputs.forEach(input => {
        input.addEventListener('blur', () => validateField(input));
        input.addEventListener('input', () => clearFieldError(input));
    });

    // 设置最小日期为今天
    const dateInput = document.getElementById('travel-date');
    const today = new Date().toISOString().split('T')[0];
    dateInput.setAttribute('min', today);
}

// 处理表单提交
async function handleFormSubmit(e) {
    e.preventDefault();
    
    const form = e.target;
    const submitBtn = form.querySelector('.submit-btn');
    
    // 验证所有字段
    if (!validateForm(form)) {
        return;
    }

    // 显示加载状态
    submitBtn.classList.add('loading');
    
    try {
        // 模拟提交延迟
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        // 获取表单数据
        const formData = new FormData(form);
        const consultationData = {
            id: Date.now(),
            name: formData.get('name'),
            email: formData.get('email'),
            destination: formData.get('destination'),
            travelDate: formData.get('travel-date'),
            requirements: formData.get('requirements') || '无特殊要求',
            submitTime: new Date().toLocaleString('zh-CN')
        };

        // 保存到本地存储
        saveConsultation(consultationData);
        
        // 更新侧边栏
        updateRecentConsultations();
        
        // 显示成功弹窗
        showSuccessModal();
        
        // 重置表单
        form.reset();
        
    } catch (error) {
        console.error('表单提交失败:', error);
        showNotification('提交失败，请稍后重试', 'error');
    } finally {
        submitBtn.classList.remove('loading');
    }
}

// 验证表单
function validateForm(form) {
    const inputs = form.querySelectorAll('input[required], select[required]');
    let isValid = true;

    inputs.forEach(input => {
        if (!validateField(input)) {
            isValid = false;
        }
    });

    return isValid;
}

// 验证单个字段
function validateField(input) {
    const value = input.value.trim();
    const fieldName = input.name;
    let isValid = true;
    let errorMessage = '';

    // 必填项检查
    if (input.hasAttribute('required') && !value) {
        errorMessage = '此字段为必填项';
        isValid = false;
    }
    // 邮箱格式验证
    else if (fieldName === 'email' && value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) {
            errorMessage = '请输入有效的邮箱地址';
            isValid = false;
        }
    }
    // 日期验证
    else if (fieldName === 'travel-date' && value) {
        const selectedDate = new Date(value);
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        
        if (selectedDate < today) {
            errorMessage = '出行日期不能早于今天';
            isValid = false;
        }
    }

    // 显示错误信息
    showFieldError(input, errorMessage);
    
    return isValid;
}

// 显示字段错误
function showFieldError(input, message) {
    const errorElement = document.getElementById(`${input.name}-error`);
    if (errorElement) {
        errorElement.textContent = message;
        errorElement.classList.toggle('show', !!message);
    }
    
    input.classList.toggle('error', !!message);
}

// 清除字段错误
function clearFieldError(input) {
    const errorElement = document.getElementById(`${input.name}-error`);
    if (errorElement) {
        errorElement.textContent = '';
        errorElement.classList.remove('show');
    }
    
    input.classList.remove('error');
}

// 保存咨询记录
function saveConsultation(data) {
    let consultations = JSON.parse(localStorage.getItem('consultations') || '[]');
    consultations.unshift(data);
    
    // 只保留最新的10条记录
    consultations = consultations.slice(0, 10);
    
    localStorage.setItem('consultations', JSON.stringify(consultations));
}

// 加载最近咨询记录
function loadRecentConsultations() {
    updateRecentConsultations();
}

// 更新最近咨询显示
function updateRecentConsultations() {
    const consultations = JSON.parse(localStorage.getItem('consultations') || '[]');
    const container = document.getElementById('recent-consultations');
    
    if (consultations.length === 0) {
        container.innerHTML = '<p class="no-consultations">暂无咨询记录</p>';
        return;
    }

    // 只显示最新的3条
    const recentThree = consultations.slice(0, 3);
    
    container.innerHTML = recentThree.map(consultation => `
        <div class="consultation-item">
            <h4>${consultation.name}</h4>
            <p><strong>目的地:</strong> ${consultation.destination}</p>
            <p><strong>出行日期:</strong> ${consultation.travelDate}</p>
            <p class="consultation-date">${consultation.submitTime}</p>
        </div>
    `).join('');
}

// 显示成功弹窗
function showSuccessModal() {
    const modal = document.getElementById('success-modal');
    const closeBtn = document.getElementById('modal-close');
    
    modal.classList.add('show');
    
    // 关闭按钮事件
    closeBtn.onclick = () => {
        modal.classList.remove('show');
    };
    
    // 点击背景关闭
    modal.onclick = (e) => {
        if (e.target === modal) {
            modal.classList.remove('show');
        }
    };
    
    // 3秒后自动关闭
    setTimeout(() => {
        modal.classList.remove('show');
    }, 3000);
}

// 显示通知消息
function showNotification(message, type = 'info') {
    // 创建通知元素
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
        <span>${message}</span>
    `;
    
    // 添加样式
    notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        background: ${type === 'success' ? '#27ae60' : type === 'error' ? '#e74c3c' : '#3498db'};
        color: white;
        padding: 15px 20px;
        border-radius: 10px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        z-index: 2000;
        display: flex;
        align-items: center;
        gap: 10px;
        animation: slideInRight 0.3s ease;
        max-width: 300px;
    `;
    
    document.body.appendChild(notification);
    
    // 3秒后移除
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

// 查看景点详情
function viewAttractionDetails(attractionName) {
    showNotification(`正在查看${attractionName}详情...`, 'info');
    // 这里可以添加跳转到详情页的逻辑
}

// 添加CSS动画样式
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(100%);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideOutRight {
        from {
            opacity: 1;
            transform: translateX(0);
        }
        to {
            opacity: 0;
            transform: translateX(100%);
        }
    }
    
    .form-group input.error,
    .form-group select.error,
    .form-group textarea.error {
        border-color: #e74c3c;
        box-shadow: 0 0 10px rgba(231, 76, 60, 0.2);
    }
`;
document.head.appendChild(style);

// 页面滚动优化
let ticking = false;

function updateOnScroll() {
    updateActiveNavigation();
    ticking = false;
}

window.addEventListener('scroll', () => {
    if (!ticking) {
        requestAnimationFrame(updateOnScroll);
        ticking = true;
    }
});

// 图片懒加载优化
if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });

    // 观察所有懒加载图片
    document.querySelectorAll('img[data-src]').forEach(img => {
        imageObserver.observe(img);
    });
}

// 错误处理
window.addEventListener('error', (e) => {
    console.error('页面错误:', e.error);
});

window.addEventListener('unhandledrejection', (e) => {
    console.error('未处理的Promise错误:', e.reason);
});