// Vue.js 应用主逻辑
const { createApp } = Vue;

createApp({
    data() {
        return {
            // API基础地址
            apiBaseUrl: 'http://localhost:5000/api',
            
            // 数据列表
            dataList: [],
            
            // 平台列表
            platforms: [],
            
            // 筛选和搜索
            selectedPlatform: '',
            searchKeyword: '',
            
            // 统计信息
            statistics: {
                total_count: 0,
                platform_count: {},
                latest_update: null
            },
            
            // 加载状态
            isLoading: false,
            isCrawling: false
        };
    },
    
    mounted() {
        // 页面加载时获取数据
        this.loadData();
        this.loadPlatforms();
        this.loadStatistics();
    },
    
    methods: {
        /**
         * 使用Axios加载数据
         */
        async loadData() {
            this.isLoading = true;
            try {
                const response = await axios.get(`${this.apiBaseUrl}/data`);
                if (response.data.success) {
                    this.dataList = response.data.data;
                    console.log('成功加载数据:', this.dataList.length, '条');
                } else {
                    this.showError('加载数据失败');
                }
            } catch (error) {
                console.error('加载数据错误:', error);
                this.showError('无法连接到服务器，请确保后端API已启动');
            } finally {
                this.isLoading = false;
            }
        },
        
        /**
         * 加载平台列表
         */
        async loadPlatforms() {
            try {
                const response = await axios.get(`${this.apiBaseUrl}/platforms`);
                if (response.data.success) {
                    this.platforms = response.data.data;
                }
            } catch (error) {
                console.error('加载平台列表错误:', error);
            }
        },
        
        /**
         * 加载统计信息
         */
        async loadStatistics() {
            try {
                const response = await axios.get(`${this.apiBaseUrl}/statistics`);
                if (response.data.success) {
                    this.statistics = response.data.data;
                }
            } catch (error) {
                console.error('加载统计信息错误:', error);
            }
        },
        
        /**
         * 平台筛选
         */
        async filterData() {
            this.isLoading = true;
            try {
                const url = this.selectedPlatform 
                    ? `${this.apiBaseUrl}/data?platform=${this.selectedPlatform}`
                    : `${this.apiBaseUrl}/data`;
                
                const response = await axios.get(url);
                if (response.data.success) {
                    this.dataList = response.data.data;
                    console.log('筛选结果:', this.dataList.length, '条');
                }
            } catch (error) {
                console.error('筛选数据错误:', error);
                this.showError('筛选失败');
            } finally {
                this.isLoading = false;
            }
        },
        
        /**
         * 关键词搜索
         */
        async searchData() {
            if (!this.searchKeyword.trim()) {
                this.loadData();
                return;
            }
            
            this.isLoading = true;
            try {
                const response = await axios.get(`${this.apiBaseUrl}/data`, {
                    params: { keyword: this.searchKeyword }
                });
                
                if (response.data.success) {
                    this.dataList = response.data.data;
                    console.log('搜索结果:', this.dataList.length, '条');
                }
            } catch (error) {
                console.error('搜索错误:', error);
                this.showError('搜索失败');
            } finally {
                this.isLoading = false;
            }
        },
        
        /**
         * 刷新数据
         */
        refreshData() {
            this.selectedPlatform = '';
            this.searchKeyword = '';
            this.loadData();
            this.loadPlatforms();
            this.loadStatistics();
        },
        
        /**
         * 触发数据采集
         */
        async crawlData() {
            this.isCrawling = true;
            try {
                const response = await axios.post(`${this.apiBaseUrl}/crawl`, {
                    platform: this.selectedPlatform || null
                });
                
                if (response.data.success) {
                    alert('数据采集任务已启动，请稍后刷新查看结果');
                    
                    // 5秒后自动刷新数据
                    setTimeout(() => {
                        this.refreshData();
                    }, 5000);
                }
            } catch (error) {
                console.error('采集数据错误:', error);
                this.showError('数据采集失败');
            } finally {
                this.isCrawling = false;
            }
        },
        
        /**
         * 删除数据项
         */
        async deleteItem(itemId) {
            if (!confirm('确定要删除这条数据吗？')) {
                return;
            }
            
            try {
                const response = await axios.delete(`${this.apiBaseUrl}/data/${itemId}`);
                if (response.data.success) {
                    alert('删除成功');
                    this.refreshData();
                }
            } catch (error) {
                console.error('删除数据错误:', error);
                this.showError('删除失败');
            }
        },
        
        /**
         * 获取平台徽章样式
         */
        getPlatformBadge(platform) {
            const badges = {
                '微博': 'bg-danger',
                '知乎': 'bg-info',
                '抖音': 'bg-dark',
                '默认': 'bg-secondary'
            };
            return badges[platform] || badges['默认'];
        },
        
        /**
         * 显示错误信息
         */
        showError(message) {
            alert(message);
        }
    }
}).mount('#app');
