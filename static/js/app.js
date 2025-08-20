/**
 * 文本处理Web应用程序的JavaScript逻辑
 * 提供用户交互、API调用和UI更新功能
 */

class TextProcessorApp {
    constructor() {
        this.currentResult = null;
        this.isProcessing = false;
        this.regexRules = [];  // 存储正则规则
        this.init();
    }

    /**
     * 初始化应用程序
     */
    init() {
        this.bindEvents();
        this.updateCharCount();
        this.updateRegexRulesCharCount();
        this.setupViewToggle();
        this.setupToastHandlers();
        this.updateRegexRulesList();  // 初始化正则规则列表
        this.setupResizeHandle();  // 设置拖动分隔线
        this.setupRegexRulesWindow();  // 设置正则规则窗口控制
        this.setupTabSwitching();  // 设置选项卡切换
    }

    /**
     * 绑定事件监听器
     */
    bindEvents() {
        // 文本输入事件
        const inputText = document.getElementById('inputText');
        inputText.addEventListener('input', () => this.updateCharCount());
        inputText.addEventListener('paste', () => this.updateCharCount());

        // 正则规则输入事件
        const regexReplaceRules = document.getElementById('regexReplaceRules');
        regexReplaceRules.addEventListener('input', () => this.updateRegexRulesCharCount());
        regexReplaceRules.addEventListener('paste', () => this.updateRegexRulesCharCount());

        // 按钮事件
        document.getElementById('processBtn').addEventListener('click', () => this.processText());
        document.getElementById('regexBtn').addEventListener('click', () => this.processRegex());
        document.getElementById('translateBtn').addEventListener('click', () => this.translateText());
        document.getElementById('clearBtn').addEventListener('click', () => this.clearAll());
        document.getElementById('parseRulesBtn').addEventListener('click', () => this.parseRegexRules());
        document.getElementById('exportRegexRules').addEventListener('click', () => this.exportRegexRules());
        document.getElementById('addRegexRule').addEventListener('click', () => this.addRegexRule());

        // 复制按钮事件
        document.querySelectorAll('.copy-btn').forEach(btn => {
            btn.addEventListener('click', (e) => this.copyText(e));
        });

        // 键盘快捷键
        document.addEventListener('keydown', (e) => this.handleKeyboardShortcuts(e));

        // 窗口事件
        window.addEventListener('beforeunload', () => this.handleBeforeUnload());
        
        // 初始化翻译服务
        this.loadTranslationServices();
        
        // 正则规则窗口控制事件
        document.getElementById('expandRegexRules').addEventListener('click', () => this.expandRegexRules());
        document.getElementById('collapseRegexRules').addEventListener('click', () => this.collapseRegexRules());
        
        // 导入正则规则事件
        document.getElementById('importRegexRules').addEventListener('click', () => this.importRegexRules());
        document.getElementById('regexFileInput').addEventListener('change', (e) => this.handleFileImport(e));
        
        // 选项卡切换事件
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', (e) => this.switchTab(e));
        });

        // API配置相关事件
        document.getElementById('translationService').addEventListener('change', (e) => this.onTranslationServiceChange(e));
        document.getElementById('saveApiConfigBtn').addEventListener('click', () => this.saveApiConfig());
        document.getElementById('clearApiConfigBtn').addEventListener('click', () => this.clearApiConfig());
        document.getElementById('testApiConfigBtn').addEventListener('click', () => this.testApiConfig());
        document.getElementById('toggleApiKeyBtn').addEventListener('click', () => this.toggleApiKeyVisibility());
        
        // API密钥输入框事件
        document.getElementById('apiKeyInput').addEventListener('focus', (e) => this.onApiKeyInputFocus(e));
    }

    /**
     * 处理键盘快捷键
     */
    handleKeyboardShortcuts(e) {
        // Ctrl+Enter 处理文本
        if (e.ctrlKey && e.key === 'Enter') {
            e.preventDefault();
            this.processText();
        }
        
        // Ctrl+Shift+C 清空
        if (e.ctrlKey && e.shiftKey && e.key === 'C') {
            e.preventDefault();
            this.clearAll();
        }
    }

    /**
     * 更新字符计数
     */
    updateCharCount() {
        const inputText = document.getElementById('inputText');
        const charCount = document.getElementById('charCount');
        const count = inputText.value.length;
        
        charCount.textContent = count.toLocaleString();
        
        // 根据字符数改变计数器颜色
        const counter = charCount.parentElement;
        if (count === 0) {
            counter.style.background = '#6b7280';
        } else if (count < 100) {
            counter.style.background = '#10b981';
        } else if (count < 1000) {
            counter.style.background = '#f59e0b';
        } else {
            counter.style.background = '#ef4444';
        }
    }

    /**
     * 更新正则规则字符计数
     */
    updateRegexRulesCharCount() {
        const regexReplaceRules = document.getElementById('regexReplaceRules');
        const regexCount = regexReplaceRules.value.length;
        const regexCharCount = document.getElementById('regexRulesCharCount');
        regexCharCount.textContent = regexCount.toLocaleString();

        const counter = regexCharCount.parentElement;
        if (regexCount === 0) {
            counter.style.background = '#6b7280';
        } else if (regexCount < 100) {
            counter.style.background = '#10b981';
        } else if (regexCount < 1000) {
            counter.style.background = '#f59e0b';
        } else {
            counter.style.background = '#ef4444';
        }
    }

    /**
     * 设置视图切换功能
     */
    setupViewToggle() {
        const toggleButtons = document.querySelectorAll('.toggle-btn');
        const outputViews = document.querySelectorAll('.output-view');

        toggleButtons.forEach(button => {
            button.addEventListener('click', () => {
                const targetView = button.getAttribute('data-view');
                
                // 更新按钮状态
                toggleButtons.forEach(btn => btn.classList.remove('active'));
                button.classList.add('active');
                
                // 更新视图显示
                outputViews.forEach(view => {
                    view.classList.remove('active');
                    if (view.id === `${targetView}View`) {
                        view.classList.add('active');
                    }
                });
            });
        });
    }

    /**
     * 设置提示框处理器
     */
    setupToastHandlers() {
        const toastCloseButtons = document.querySelectorAll('.toast-close');
        toastCloseButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                const toast = e.target.closest('.toast');
                this.hideToast(toast);
            });
        });
    }

    /**
     * 处理文本
     */
    async processText() {
        const inputText = document.getElementById('inputText');
        const text = inputText.value.trim();

        if (!text) {
            this.showError('请输入要处理的文本');
            return;
        }

        if (this.isProcessing) {
            return;
        }

        this.isProcessing = true;
        this.showLoading();

        try {
            // 获取处理选项
            const operations = this.getSelectedOperations();
            
            // 调用API
            const response = await fetch('/api/process', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    text: text,
                    operations: operations
                })
            });

            const result = await response.json();

            if (!response.ok) {
                throw new Error(result.error || '处理失败');
            }

            if (result.error) {
                throw new Error(result.error);
            }

            // 提取数据（API返回的数据在result.data中）
            const data = result.data || result;

            // 保存结果并更新UI
            this.currentResult = data;
            this.updateUI(data);
            this.showSuccess('文本处理完成');

        } catch (error) {
            console.error('处理文本时发生错误:', error);
            this.showError(error.message || '处理文本时发生错误');
        } finally {
            this.hideLoading();
            this.isProcessing = false;
        }
    }

    /**
     * 处理正则表达式替换
     */
    async processRegex() {
        const inputText = document.getElementById('inputText');
        const text = inputText.value.trim();

        if (!text) {
            this.showError('请输入要处理的文本');
            return;
        }

        if (this.regexRules.length === 0) {
            this.showError('请先添加正则替换规则');
            return;
        }

        if (this.isProcessing) {
            return;
        }

        this.isProcessing = true;
        this.showLoading();

        try {
            // 调用正则处理API
            const response = await fetch('/api/regex', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    text: text,
                    regex_rules: this.regexRules
                })
            });

            const result = await response.json();

            if (!response.ok) {
                throw new Error(result.error || '正则处理失败');
            }

            if (result.error) {
                throw new Error(result.error);
            }

            // 提取数据（API返回的数据在result.data中）
            const data = result.data || result;

            // 更新UI显示结果
            this.updateUIWithRegexResult(data);
            this.showSuccess('正则处理完成');

        } catch (error) {
            console.error('正则处理时发生错误:', error);
            this.showError(error.message || '正则处理时发生错误');
        } finally {
            this.hideLoading();
            this.isProcessing = false;
        }
    }

    /**
     * 添加正则规则
     */
    addRegexRule() {
        const patternInput = document.getElementById('regexPattern');
        const replacementInput = document.getElementById('regexReplacement');
        
        const pattern = patternInput.value.trim();
        const replacement = replacementInput.value.trim();
        
        if (!pattern) {
            this.showError('请输入正则表达式模式');
            return;
        }
        
        if (!replacement) {
            this.showError('请输入替换内容');
            return;
        }
        
        // 创建规则元组
        const rule = [pattern, replacement];
        
        // 添加到规则列表
        this.regexRules.push(rule);
        
        // 更新UI
        this.updateRegexRulesList();
        
        // 清空输入框
        patternInput.value = '';
        replacementInput.value = '';
        patternInput.focus();
        
        this.showSuccess('正则规则已添加');
    }

    /**
     * 移除正则规则
     */
    removeRegexRule(index) {
        this.regexRules.splice(index, 1);
        this.updateRegexRulesList();
        this.showSuccess('正则规则已移除');
    }

    /**
     * 更新正则规则列表显示
     */
    updateRegexRulesList() {
        const rulesList = document.getElementById('regexRulesList');
        
        if (this.regexRules.length === 0) {
            rulesList.innerHTML = '<div class="regex-empty-state">暂无正则规则，请添加规则</div>';
            return;
        }
        
        rulesList.innerHTML = this.regexRules.map((rule, index) => {
            const [pattern, replacement] = rule;
            return `
                <div class="regex-rule-item">
                    <div class="regex-rule-content">
                        <span class="regex-rule-pattern">${this.escapeHtml(pattern)}</span>
                        <span class="arrow">→</span>
                        <span class="regex-rule-replacement">${this.escapeHtml(replacement)}</span>
                    </div>
                    <button class="regex-rule-remove" onclick="app.removeRegexRule(${index})">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            `;
        }).join('');
    }

    /**
     * 使用正则结果更新UI
     */
    updateUIWithRegexResult(result) {
        // 更新处理后的文本
        const processedText = document.getElementById('processedText');
        processedText.textContent = result.processed_text || '';
        
        // 切换到处理文本视图
        this.switchToView('processed');
        
        // 保存当前结果
        this.currentResult = result;
    }

    /**
     * 切换到指定视图
     */
    switchToView(viewName) {
        const toggleButtons = document.querySelectorAll('.toggle-btn');
        const outputViews = document.querySelectorAll('.output-view');
        
        // 更新按钮状态
        toggleButtons.forEach(btn => btn.classList.remove('active'));
        document.querySelector(`[data-view="${viewName}"]`).classList.add('active');
        
        // 更新视图显示
        outputViews.forEach(view => {
            view.classList.remove('active');
            if (view.id === `${viewName}View`) {
                view.classList.add('active');
            }
        });
    }

    /**
     * HTML转义
     */
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    /**
     * 获取选中的处理选项
     */
    getSelectedOperations() {
        const operations = [];
        
        if (document.getElementById('formatOption').checked) {
            operations.push('format');
        }
        if (document.getElementById('statisticsOption').checked) {
            operations.push('statistics');
        }
        if (document.getElementById('analysisOption').checked) {
            operations.push('analysis');
        }

        return operations.length > 0 ? operations : null;
    }

    /**
     * 更新UI显示结果
     */
    updateUI(result) {
        // 更新处理后的文本
        const processedText = document.getElementById('processedText');
        processedText.textContent = result.processed_text || '';

        // 更新统计信息
        if (result.statistics) {
            this.updateStatistics(result.statistics);
        }

        // 更新分析结果
        if (result.analysis) {
            this.updateAnalysis(result.analysis);
        }
    }

    /**
     * 更新统计信息显示
     */
    updateStatistics(stats) {
        // 基本统计
        const basicStats = document.getElementById('basicStats');
        if (basicStats && stats.basic) {
            basicStats.innerHTML = this.createStatItems(stats.basic);
        }

        // 字符类型统计
        const charStats = document.getElementById('charStats');
        if (charStats && stats.character_types) {
            charStats.innerHTML = this.createStatItems(stats.character_types);
        }

        // 词频统计
        const wordFreq = document.getElementById('wordFreq');
        if (wordFreq && stats.word_frequency) {
            wordFreq.innerHTML = this.createWordFrequencyList(stats.word_frequency);
        }
    }

    /**
     * 更新分析结果显示
     */
    updateAnalysis(analysis) {
        // 可读性分析
        const readability = document.getElementById('readability');
        if (readability && analysis.readability) {
            readability.innerHTML = this.createReadabilityDisplay(analysis.readability);
        }

        // 情感分析
        const sentiment = document.getElementById('sentiment');
        if (sentiment && analysis.sentiment) {
            sentiment.innerHTML = this.createSentimentDisplay(analysis.sentiment);
        }

        // 语言特征
        const languageFeatures = document.getElementById('languageFeatures');
        if (languageFeatures && analysis.language_features) {
            languageFeatures.innerHTML = this.createLanguageFeaturesDisplay(analysis.language_features);
        }
    }

    /**
     * 创建统计项HTML
     */
    createStatItems(stats) {
        return Object.entries(stats)
            .map(([key, value]) => `
                <div class="stat-item">
                    <span class="stat-label">${this.formatStatLabel(key)}</span>
                    <span class="stat-value">${this.formatStatValue(value)}</span>
                </div>
            `)
            .join('');
    }

    /**
     * 创建词频列表HTML
     */
    createWordFrequencyList(wordFreq) {
        if (!wordFreq || wordFreq.length === 0) {
            return '<p style="color: #6b7280; font-style: italic;">暂无词频数据</p>';
        }

        return wordFreq
            .map(([word, count]) => `
                <div class="stat-item">
                    <span class="stat-label">"${word}"</span>
                    <span class="stat-value">${count} 次</span>
                </div>
            `)
            .join('');
    }

    /**
     * 创建可读性显示HTML
     */
    createReadabilityDisplay(readability) {
        const getReadabilityLevel = (score) => {
            if (score >= 90) return '非常容易';
            if (score >= 80) return '容易';
            if (score >= 70) return '较容易';
            if (score >= 60) return '标准';
            if (score >= 50) return '较难';
            if (score >= 30) return '难';
            return '非常难';
        };

        return `
            <div class="stat-item">
                <span class="stat-label">可读性评分</span>
                <span class="stat-value">${readability.flesch_reading_ease}</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">可读性级别</span>
                <span class="stat-value">${getReadabilityLevel(readability.flesch_reading_ease)}</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">平均句长</span>
                <span class="stat-value">${readability.average_sentence_length} 词</span>
            </div>
        `;
    }

    /**
     * 创建情感分析显示HTML
     */
    createSentimentDisplay(sentiment) {
        const getSentimentText = (sentiment) => {
            switch (sentiment) {
                case 'positive': return '积极';
                case 'negative': return '消极';
                case 'neutral': return '中性';
                default: return '未知';
            }
        };

        const getSentimentClass = (sentiment) => {
            switch (sentiment) {
                case 'positive': return 'sentiment-positive';
                case 'negative': return 'sentiment-negative';
                case 'neutral': return 'sentiment-neutral';
                default: return '';
            }
        };

        return `
            <div class="stat-item">
                <span class="stat-label">情感倾向</span>
                <span class="stat-value ${getSentimentClass(sentiment.sentiment)}">${getSentimentText(sentiment.sentiment)}</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">积极词汇比例</span>
                <span class="stat-value">${(sentiment.positive_ratio * 100).toFixed(1)}%</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">消极词汇比例</span>
                <span class="stat-value">${(sentiment.negative_ratio * 100).toFixed(1)}%</span>
            </div>
        `;
    }

    /**
     * 创建语言特征显示HTML
     */
    createLanguageFeaturesDisplay(features) {
        const getLanguageText = (type) => {
            switch (type) {
                case 'chinese': return '中文';
                case 'english': return '英文';
                case 'mixed': return '混合';
                default: return '未知';
            }
        };

        return `
            <div class="stat-item">
                <span class="stat-label">语言类型</span>
                <span class="stat-value">${getLanguageText(features.language_type)}</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">中文比例</span>
                <span class="stat-value">${(features.chinese_ratio * 100).toFixed(1)}%</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">英文比例</span>
                <span class="stat-value">${(features.english_ratio * 100).toFixed(1)}%</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">包含数字</span>
                <span class="stat-value">${features.features.has_numbers ? '是' : '否'}</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">包含链接</span>
                <span class="stat-value">${features.features.has_urls ? '是' : '否'}</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">包含邮箱</span>
                <span class="stat-value">${features.features.has_emails ? '是' : '否'}</span>
            </div>
        `;
    }

    /**
     * 格式化统计标签
     */
    formatStatLabel(key) {
        const labels = {
            'characters': '字符数',
            'words': '词数',
            'lines': '行数',
            'sentences': '句子数',
            'letters': '字母',
            'digits': '数字',
            'spaces': '空格',
            'punctuation': '标点符号',
            'average_word_length': '平均词长',
            'average_sentence_length': '平均句长'
        };
        return labels[key] || key;
    }

    /**
     * 格式化统计值
     */
    formatStatValue(value) {
        if (typeof value === 'number') {
            return value.toLocaleString();
        }
        return value;
    }

    /**
     * 清空所有内容
     */
    async clearAll() {
        try {
            // 调用清空API
            await fetch('/api/clear', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            // 清空输入文本
            document.getElementById('inputText').value = '';
            this.updateCharCount();

            // 清空正则规则输入
            document.getElementById('regexReplaceRules').value = '';
            this.updateRegexRulesCharCount();

            // 清空输出
            document.getElementById('processedText').textContent = '';
            document.getElementById('basicStats').innerHTML = '';
            document.getElementById('charStats').innerHTML = '';
            document.getElementById('wordFreq').innerHTML = '';
            document.getElementById('readability').innerHTML = '';
            document.getElementById('sentiment').innerHTML = '';
            document.getElementById('languageFeatures').innerHTML = '';

            // 清空正则规则
            this.regexRules = [];
            this.updateRegexRulesList();

            // 重置当前结果
            this.currentResult = null;

            this.showSuccess('内容已清空');

        } catch (error) {
            console.error('清空内容时发生错误:', error);
            this.showError('清空内容时发生错误');
        }
    }

    /**
     * 显示加载状态
     */
    showLoading() {
        const loadingOverlay = document.getElementById('loadingOverlay');
        const loadingText = document.querySelector('.loading-spinner p');
        
        // 检查是否是长文本翻译
        const inputText = document.getElementById('inputText').value.trim();
        if (inputText.length > 3000) {
            loadingText.textContent = '正在翻译长文本，请耐心等待...';
        } else {
            loadingText.textContent = '正在处理文本...';
        }
        
        loadingOverlay.classList.add('show');
    }

    /**
     * 隐藏加载状态
     */
    hideLoading() {
        const loadingOverlay = document.getElementById('loadingOverlay');
        loadingOverlay.classList.remove('show');
    }

    /**
     * 显示成功提示
     */
    showSuccess(message) {
        const toast = document.getElementById('successToast');
        const messageSpan = document.getElementById('successMessage');
        messageSpan.textContent = message;
        this.showToast(toast);
    }

    /**
     * 显示错误提示
     */
    showError(message) {
        const toast = document.getElementById('errorToast');
        const messageSpan = document.getElementById('errorMessage');
        messageSpan.textContent = message;
        this.showToast(toast);
    }

    /**
     * 显示提示框
     */
    showToast(toast) {
        toast.classList.add('show');
        
        // 3秒后自动隐藏
        setTimeout(() => {
            this.hideToast(toast);
        }, 3000);
    }

    /**
     * 隐藏提示框
     */
    hideToast(toast) {
        toast.classList.remove('show');
    }

    /**
     * 处理页面卸载前的事件
     */
    handleBeforeUnload() {
        if (this.isProcessing) {
            return '正在处理文本，确定要离开吗？';
        }
    }

    /**
     * 解析正则规则输入框中的规则
     */
    parseRegexRules() {
        const regexReplaceRules = document.getElementById('regexReplaceRules');
        const rules = regexReplaceRules.value.trim();
        
        if (!rules) {
            this.showError('请输入正则规则');
            return;
        }

        try {
            // 解析Python元组格式的规则
            const parsedRules = this.parsePythonTupleRules(rules);
            if (parsedRules.length === 0) {
                this.showError('未找到有效的正则规则');
                return;
            }
            
            this.regexRules = parsedRules;
            this.updateRegexRulesList();
            this.showSuccess(`成功解析 ${parsedRules.length} 条正则规则`);
            
        } catch (error) {
            console.error('正则规则解析失败:', error);
            this.showError('正则规则解析失败，请检查格式');
        }
    }

    /**
     * 解析Python元组格式的正则规则
     */
    parsePythonTupleRules(rulesText) {
        const rules = [];
        const lines = rulesText.split('\n').map(line => line.trim()).filter(line => line);
        
        for (const line of lines) {
            // 支持 pattern 和 replacement 分别用不同的引号
            // (r"pattern", r'replacement') 或 (r'pattern', r"replacement") 等
            const rawTupleMatch = line.match(/\(\s*r(["'])([\s\S]+?)\1\s*,\s*r(["'])([\s\S]+?)\3\s*\)/);
            if (rawTupleMatch) {
                const pattern = rawTupleMatch[2];
                const replacement = rawTupleMatch[4];
                rules.push([pattern, replacement]);
                continue;
            }
            // 兼容旧逻辑（同种引号）
            const oldRawTupleMatch = line.match(/\(\s*r["']([^"']+)["']\s*,\s*r["']([^"']+)["']\s*\)/);
            if (oldRawTupleMatch) {
                const pattern = oldRawTupleMatch[1];
                const replacement = oldRawTupleMatch[2];
                rules.push([pattern, replacement]);
                continue;
            }
            
            // 匹配 ("pattern", "replacement") 格式 - 需要转义处理
            const simpleMatch = line.match(/\(\s*["']([^"']+)["']\s*,\s*["']([^"']+)["']\s*\)/);
            if (simpleMatch) {
                const pattern = this.escapeRegexPattern(simpleMatch[1]);
                const replacement = this.escapeRegexReplacement(simpleMatch[2]);
                rules.push([pattern, replacement]);
                continue;
            }
            
            // 匹配 s/pattern/replacement/ 格式
            const sedMatch = line.match(/^s\/([^\/]+)\/([^\/]*)\/?$/);
            if (sedMatch) {
                const pattern = sedMatch[1];
                const replacement = sedMatch[2];
                rules.push([pattern, replacement]);
                continue;
            }
        }
        
        return rules;
    }

    /**
     * 转义正则表达式模式中的特殊字符
     */
    escapeRegexPattern(pattern) {
        // 正则表达式中的特殊字符
        const regexSpecialChars = [
            '\\', '.', '^', '$', '*', '+', '?', '(', ')', '[', ']', '{', '}', '|', '-'
        ];
        
        let escapedPattern = pattern;
        
        // 对每个特殊字符进行转义
        for (const char of regexSpecialChars) {
            // 使用字符串替换而不是正则表达式，避免循环转义
            escapedPattern = escapedPattern.split(char).join('\\' + char);
        }
        
        return escapedPattern;
    }

    /**
     * 转义替换字符串中的特殊字符
     */
    escapeRegexReplacement(replacement) {
        // 替换字符串中的特殊字符
        const replacementSpecialChars = ['\\', '$'];
        
        let escapedReplacement = replacement;
        
        // 对每个特殊字符进行转义
        for (const char of replacementSpecialChars) {
            // 使用字符串替换而不是正则表达式，避免循环转义
            escapedReplacement = escapedReplacement.split(char).join('\\' + char);
        }
        
        return escapedReplacement;
    }

    /**
     * 复制文本到剪贴板
     */
    async copyText(e) {
        e.preventDefault();
        const button = e.currentTarget;
        const targetId = button.getAttribute('data-target');
        const targetElement = document.getElementById(targetId);
        
        let textToCopy = '';
        
        if (targetId === 'processedText') {
            textToCopy = targetElement.textContent;
        } else {
            textToCopy = targetElement.value;
        }
        
        if (!textToCopy.trim()) {
            this.showError('没有内容可复制');
            return;
        }
        
        try {
            await navigator.clipboard.writeText(textToCopy);
            
            // 显示复制成功状态
            button.classList.add('copied');
            setTimeout(() => {
                button.classList.remove('copied');
            }, 2000);
            
            this.showSuccess('文本已复制到剪贴板');
        } catch (err) {
            console.error('复制文本失败:', err);
            this.showError('复制文本失败');
        }
    }

    /**
     * 导出正则规则
     */
    exportRegexRules() {
        if (this.regexRules.length === 0) {
            this.showError('没有规则可导出');
            return;
        }

        // 创建导出选项对话框
        const exportDialog = document.createElement('div');
        exportDialog.className = 'export-dialog';
        exportDialog.innerHTML = `
            <div class="export-dialog-content">
                <h3>选择导出格式</h3>
                <div class="export-options">
                    <label class="export-option">
                        <input type="radio" name="exportFormat" value="text" checked>
                        <span>文本格式 (.txt)</span>
                    </label>
                    <label class="export-option">
                        <input type="radio" name="exportFormat" value="json">
                        <span>JSON格式 (.json)</span>
                    </label>
                    <label class="export-option">
                        <input type="radio" name="exportFormat" value="rules">
                        <span>规则格式 (.rules)</span>
                    </label>
                </div>
                <div class="export-dialog-buttons">
                    <button class="btn btn-secondary" onclick="this.closest('.export-dialog').remove()">取消</button>
                    <button class="btn btn-primary" onclick="app.confirmExport(this)">导出</button>
                </div>
            </div>
        `;
        
        document.body.appendChild(exportDialog);
    }

    /**
     * 确认导出
     */
    confirmExport(button) {
        const dialog = button.closest('.export-dialog');
        const format = dialog.querySelector('input[name="exportFormat"]:checked').value;
        
        let fileContent = '';
        let fileName = '';
        let mimeType = '';
        
        switch (format) {
            case 'text':
                fileContent = this.generateTextFormat();
                fileName = 'regex_replace.txt';
                mimeType = 'text/plain;charset=utf-8';
                break;
            case 'json':
                fileContent = this.generateJsonFormat();
                fileName = 'regex_replace.json';
                mimeType = 'application/json;charset=utf-8';
                break;
            case 'rules':
                fileContent = this.generateRulesFormat();
                fileName = 'regex_replace.rules';
                mimeType = 'text/plain;charset=utf-8';
                break;
        }
        
        // 创建并下载文件
        const blob = new Blob([fileContent], { type: mimeType });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = fileName;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        
        dialog.remove();
        this.showSuccess(`成功导出 ${this.regexRules.length} 条正则规则`);
    }

    /**
     * 生成文本格式
     */
    generateTextFormat() {
        const rulesText = this.regexRules.map(rule => {
            const [pattern, replacement] = rule;
            return `(r"${pattern}", r"${replacement}")`;
        }).join(',\n');

        return `# 正则匹配替换规则
# 格式: (pattern, replacement)
# 使用说明: 将此文件内容复制到"正则规则编写"窗口中，然后点击"解析规则"按钮

${rulesText}`;
    }

    /**
     * 生成JSON格式
     */
    generateJsonFormat() {
        const rules = this.regexRules.map(rule => ({
            pattern: rule[0],
            replacement: rule[1]
        }));
        
        return JSON.stringify({
            version: "1.0",
            description: "正则匹配替换规则",
            rules: rules
        }, null, 2);
    }

    /**
     * 生成规则格式
     */
    generateRulesFormat() {
        return this.regexRules.map(rule => {
            const [pattern, replacement] = rule;
            return `${pattern}\t${replacement}`;
        }).join('\n');
    }

    /**
     * 加载翻译服务列表
     */
    async loadTranslationServices() {
        try {
            const response = await fetch('/api/translation-services');
            const result = await response.json();
            
            if (result.error) {
                console.error('加载翻译服务失败:', result.error);
                return;
            }
            
            // 提取数据（API返回的数据在result.data中）
            const data = result.data || result;
            
            const serviceSelect = document.getElementById('translationService');
            serviceSelect.innerHTML = '';
            
            if (data.count === 0) {
                serviceSelect.innerHTML = '<option value="">没有可用的翻译服务</option>';
                return;
            }
            
            // 添加默认选项
            serviceSelect.innerHTML = '<option value="">选择翻译服务</option>';
            
            // 添加所有可用服务
            Object.entries(data.services).forEach(([key, service]) => {
                const option = document.createElement('option');
                option.value = key;
                
                // 显示服务名称，如果已配置则添加标识
                let displayName = service.name;
                if (service.is_user_configured && service.enabled) {
                    displayName += ' ✓ (已配置)';
                } else if (service.enabled) {
                    displayName += ' ✓ (环境变量)';
                } else {
                    displayName += ' (未配置)';
                }
                
                option.textContent = displayName;
                serviceSelect.appendChild(option);
            });
            
        } catch (error) {
            console.error('加载翻译服务失败:', error);
        }
    }

    /**
     * 加载翻译服务的可用模型
     */
    async loadTranslationModels(serviceName) {
        try {
            const response = await fetch(`/api/translation-services/${serviceName}/models`);
            const result = await response.json();
            
            if (result.error) {
                console.error('加载模型列表失败:', result.error);
                return;
            }
            
            const data = result.data || result;
            const modelSelect = document.getElementById('modelSelect');
            modelSelect.innerHTML = '';
            
            if (data.count === 0) {
                modelSelect.innerHTML = '<option value="">该服务暂无可用模型</option>';
                return;
            }
            
            // 添加默认选项
            modelSelect.innerHTML = '<option value="">选择模型</option>';
            
            // 添加可用模型
            data.models.forEach(model => {
                const option = document.createElement('option');
                option.value = model;
                option.textContent = model;
                modelSelect.appendChild(option);
            });
            
        } catch (error) {
            console.error('加载模型列表失败:', error);
        }
    }

    /**
     * 加载翻译服务的当前配置
     */
    async loadTranslationServiceConfig(serviceName) {
        try {
            const response = await fetch(`/api/translation-services/${serviceName}/config`);
            const result = await response.json();
            
            if (result.error) {
                console.error('加载服务配置失败:', result.error);
                return;
            }
            
            const data = result.data || result;
            
            // 更新API密钥输入框
            const apiKeyInput = document.getElementById('apiKeyInput');
            if (data.user_config.has_api_key) {
                apiKeyInput.value = '••••••••••••••••'; // 显示占位符
                apiKeyInput.setAttribute('data-has-key', 'true');
            } else {
                apiKeyInput.value = '';
                apiKeyInput.removeAttribute('data-has-key');
            }
            
            // 更新模型选择
            const modelSelect = document.getElementById('modelSelect');
            if (data.user_config.model) {
                // 确保模型选项已加载
                await this.loadTranslationModels(serviceName);
                modelSelect.value = data.user_config.model;
            }
            
            // 更新状态显示
            this.updateApiConfigStatus('info', `当前服务: ${serviceName}`);
            
        } catch (error) {
            console.error('加载服务配置失败:', error);
        }
    }

    /**
     * 保存API配置
     */
    async saveApiConfig() {
        const serviceSelect = document.getElementById('translationService');
        const apiKeyInput = document.getElementById('apiKeyInput');
        const modelSelect = document.getElementById('modelSelect');
        
        const serviceName = serviceSelect.value;
        let apiKey = apiKeyInput.value.trim();
        const model = modelSelect.value;
        
        if (!serviceName) {
            this.showError('请先选择翻译服务');
            return;
        }
        
        // 检查API密钥是否有效（不是占位符）
        if (!apiKey || apiKey === '••••••••••••••••') {
            this.showError('请输入有效的API密钥');
            return;
        }
        
        // 验证API密钥格式（基本验证）
        if (apiKey.length < 10) {
            this.showError('API密钥长度不足，请检查输入');
            return;
        }
        
        try {
            const response = await fetch(`/api/translation-services/${serviceName}/config`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    api_key: apiKey,
                    model: model
                })
            });
            
            const result = await response.json();
            
            if (result.error) {
                this.showError(result.error);
                return;
            }
            
            const data = result.data || result;
            
            // 更新UI状态
            apiKeyInput.value = '••••••••••••••••';
            apiKeyInput.setAttribute('data-has-key', 'true');
            
            this.updateApiConfigStatus('success', data.message);
            
            // 重新加载翻译服务列表以反映新配置
            await this.loadTranslationServices();
            
        } catch (error) {
            console.error('保存API配置失败:', error);
            this.showError('保存配置失败，请检查网络连接');
        }
    }

    /**
     * 清除API配置
     */
    async clearApiConfig() {
        const serviceSelect = document.getElementById('translationService');
        const serviceName = serviceSelect.value;
        
        if (!serviceName) {
            this.showError('请先选择翻译服务');
            return;
        }
        
        const confirmClear = confirm(`确定要清除 ${serviceName} 的API配置吗？`);
        if (!confirmClear) {
            return;
        }
        
        try {
            const response = await fetch(`/api/translation-services/${serviceName}/config`, {
                method: 'DELETE'
            });
            
            const result = await response.json();
            
            if (result.error) {
                this.showError(result.error);
                return;
            }
            
            const data = result.data || result;
            
            // 清除UI状态
            const apiKeyInput = document.getElementById('apiKeyInput');
            const modelSelect = document.getElementById('modelSelect');
            
            apiKeyInput.value = '';
            apiKeyInput.removeAttribute('data-has-key');
            modelSelect.value = '';
            
            this.updateApiConfigStatus('info', data.message);
            
            // 重新加载翻译服务列表
            await this.loadTranslationServices();
            
        } catch (error) {
            console.error('清除API配置失败:', error);
            this.showError('清除配置失败，请检查网络连接');
        }
    }

    /**
     * 测试API连接
     */
    async testApiConfig() {
        const serviceSelect = document.getElementById('translationService');
        const serviceName = serviceSelect.value;
        
        if (!serviceName) {
            this.showError('请先选择翻译服务');
            return;
        }
        
        this.updateApiConfigStatus('info', '正在测试连接...');
        
        try {
            // 使用一个简单的测试文本进行翻译测试
            const response = await fetch('/api/translate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    text: 'Hello',
                    prompt: '请将以下文本翻译成中文：',
                    service_name: serviceName
                })
            });
            
            const result = await response.json();
            
            if (result.error) {
                this.updateApiConfigStatus('error', `连接测试失败: ${result.error}`);
                return;
            }
            
            this.updateApiConfigStatus('success', '连接测试成功！API配置正常。');
            
        } catch (error) {
            console.error('API连接测试失败:', error);
            this.updateApiConfigStatus('error', '连接测试失败，请检查API配置');
        }
    }

    /**
     * 更新API配置状态显示
     */
    updateApiConfigStatus(type, message) {
        const statusElement = document.getElementById('apiConfigStatus');
        statusElement.className = `api-config-status ${type}`;
        statusElement.textContent = message;
    }

    /**
     * 切换API密钥显示/隐藏
     */
    toggleApiKeyVisibility() {
        const apiKeyInput = document.getElementById('apiKeyInput');
        const toggleBtn = document.getElementById('toggleApiKeyBtn');
        const icon = toggleBtn.querySelector('i');
        
        if (apiKeyInput.type === 'password') {
            apiKeyInput.type = 'text';
            icon.className = 'fas fa-eye-slash';
            toggleBtn.title = '隐藏API密钥';
        } else {
            apiKeyInput.type = 'password';
            icon.className = 'fas fa-eye';
            toggleBtn.title = '显示API密钥';
        }
    }

    /**
     * 翻译服务选择变化时的处理
     */
    async onTranslationServiceChange(event) {
        const serviceName = event.target.value;
        
        if (!serviceName) {
            // 清除API配置区域
            const apiKeyInput = document.getElementById('apiKeyInput');
            const modelSelect = document.getElementById('modelSelect');
            const statusElement = document.getElementById('apiConfigStatus');
            
            apiKeyInput.value = '';
            apiKeyInput.removeAttribute('data-has-key');
            modelSelect.innerHTML = '<option value="">请先选择翻译服务</option>';
            statusElement.className = 'api-config-status';
            statusElement.textContent = '';
            return;
        }
        
        // 加载该服务的模型列表
        await this.loadTranslationModels(serviceName);
        
        // 加载该服务的当前配置
        await this.loadTranslationServiceConfig(serviceName);
    }

    /**
     * API密钥输入框获得焦点时的处理
     */
    onApiKeyInputFocus(event) {
        const apiKeyInput = event.target;
        
        // 如果当前显示的是占位符，清空输入框
        if (apiKeyInput.value === '••••••••••••••••') {
            apiKeyInput.value = '';
            apiKeyInput.removeAttribute('data-has-key');
        }
    }

    /**
     * 翻译文本
     */
    async translateText() {
        const inputText = document.getElementById('inputText').value.trim();
        const translationPrompt = document.getElementById('translationPrompt').value.trim();
        const translationService = document.getElementById('translationService').value;
        
        if (!inputText) {
            this.showError('请输入要翻译的文本');
            return;
        }
        
        if (!translationPrompt) {
            this.showError('请输入翻译提示词');
            return;
        }
        
        if (!translationService) {
            this.showError('请选择翻译服务');
            return;
        }
        
        // 检查文本长度，给出提示
        const textLength = inputText.length;
        if (textLength > 3000) {
            const confirmLongText = confirm(
                `检测到长文本（${textLength}个字符），翻译可能需要较长时间。\n\n` +
                `系统将自动分段翻译，请耐心等待。\n\n` +
                `是否继续翻译？`
            );
            if (!confirmLongText) {
                return;
            }
        }
        
        this.showLoading();
        
        try {
            const response = await fetch('/api/translate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    text: inputText,
                    prompt: translationPrompt,
                    service_name: translationService
                })
            });
            
            const result = await response.json();
            
            if (result.error) {
                this.showError(result.error);
                return;
            }
            
            // 提取数据（API返回的数据在result.data中）
            const data = result.data || result;
            
            this.updateUIWithTranslationResult(data);
            
            // 根据翻译结果显示不同的成功消息
            if (data.chunks_translated && data.chunks_translated > 1) {
                this.showSuccess(`翻译完成！共翻译了${data.chunks_translated}个文本段`);
            } else {
                this.showSuccess('翻译完成');
            }
            
        } catch (error) {
            console.error('翻译失败:', error);
            if (error.name === 'TypeError' && error.message.includes('timeout')) {
                this.showError('翻译超时，请稍后重试或减少文本长度');
            } else {
                this.showError('翻译失败，请检查网络连接');
            }
        } finally {
            this.hideLoading();
        }
    }

    /**
     * 更新UI显示翻译结果
     */
    updateUIWithTranslationResult(result) {
        const processedText = document.getElementById('processedText');
        
        if (result.error) {
            processedText.textContent = `翻译错误: ${result.error}`;
            return;
        }
        
        // 显示翻译结果
        processedText.textContent = result.translated_text;
        
        // 切换到处理文本视图
        this.switchToView('processed');
        
        // 更新当前结果
        this.currentResult = {
            ...result,
            processed_text: result.translated_text
        };
    }

    /**
     * 导入正则规则
     */
    importRegexRules() {
        const fileInput = document.getElementById('regexFileInput');
        fileInput.click();
    }

    /**
     * 处理文件导入
     */
    handleFileImport(event) {
        const file = event.target.files[0];
        if (!file) {
            return;
        }

        const reader = new FileReader();
        
        reader.onload = (e) => {
            try {
                const content = e.target.result;
                
                // 尝试解析不同格式的文件
                let rules = [];
                
                // 检查是否是JSON格式
                if (file.name.endsWith('.json')) {
                    try {
                        const jsonData = JSON.parse(content);
                        if (Array.isArray(jsonData)) {
                            rules = jsonData.map(rule => [rule.pattern || rule[0], rule.replacement || rule[1]]);
                        } else if (jsonData.rules) {
                            rules = jsonData.rules.map(rule => [rule.pattern, rule.replacement]);
                        }
                    } catch (jsonError) {
                        console.error('JSON解析失败:', jsonError);
                    }
                } else {
                    // 尝试解析文本格式
                    rules = this.parsePythonTupleRules(content);
                }
                
                if (rules.length === 0) {
                    this.showError('文件中未找到有效的正则规则');
                    return;
                }
                
                // 更新规则列表
                this.regexRules = rules;
                this.updateRegexRulesList();
                
                // 更新正则规则输入框
                const regexReplaceRules = document.getElementById('regexReplaceRules');
                const rulesText = rules.map(rule => {
                    const [pattern, replacement] = rule;
                    return `(r"${pattern}", r"${replacement}")`;
                }).join(',\n');
                regexReplaceRules.value = rulesText;
                this.updateRegexRulesCharCount();
                
                this.showSuccess(`成功导入 ${rules.length} 条正则规则`);
                
            } catch (error) {
                console.error('处理导入文件时发生错误:', error);
                this.showError('处理导入文件时发生错误');
            }
        };
        
        reader.onerror = () => {
            this.showError('读取文件失败');
        };
        
        reader.readAsText(file);
        
        // 清空文件输入，允许重复选择同一文件
        event.target.value = '';
    }

    /**
     * 设置拖动分隔线功能
     */
    setupResizeHandle() {
        const resizeHandle = document.getElementById('resizeHandle');
        const container = document.querySelector('.text-windows-container');
        let isResizing = false;
        let startX = 0;
        let startWidth = 0;

        resizeHandle.addEventListener('mousedown', (e) => {
            isResizing = true;
            startX = e.clientX;
            startWidth = container.offsetWidth;
            
            // 添加拖动样式
            document.body.style.cursor = 'col-resize';
            document.body.style.userSelect = 'none';
            
            e.preventDefault();
        });

        document.addEventListener('mousemove', (e) => {
            if (!isResizing) return;
            
            const deltaX = e.clientX - startX;
            const newWidth = startWidth + deltaX;
            
            // 限制最小宽度
            const minWidth = 300;
            const maxWidth = window.innerWidth - 100;
            
            if (newWidth >= minWidth && newWidth <= maxWidth) {
                const leftWidth = Math.max(minWidth, (newWidth - 8) / 2);
                const rightWidth = newWidth - 8 - leftWidth;
                
                container.style.gridTemplateColumns = `${leftWidth}px 8px ${rightWidth}px`;
            }
        });

        document.addEventListener('mouseup', () => {
            if (isResizing) {
                isResizing = false;
                document.body.style.cursor = '';
                document.body.style.userSelect = '';
            }
        });
    }

    /**
     * 设置正则规则窗口控制
     */
    setupRegexRulesWindow() {
        const content = document.querySelector('.regex-rules-content');
        const expandBtn = document.getElementById('expandRegexRules');
        const collapseBtn = document.getElementById('collapseRegexRules');
        
        // 初始化状态
        content.classList.add('collapsed');
        expandBtn.style.display = 'inline-flex';
        collapseBtn.style.display = 'none';
    }

    /**
     * 展开正则规则窗口
     */
    expandRegexRules() {
        const content = document.querySelector('.regex-rules-content');
        const expandBtn = document.getElementById('expandRegexRules');
        const collapseBtn = document.getElementById('collapseRegexRules');
        
        content.classList.remove('collapsed');
        content.classList.add('expanded');
        expandBtn.style.display = 'none';
        collapseBtn.style.display = 'inline-flex';
    }

    /**
     * 折叠正则规则窗口
     */
    collapseRegexRules() {
        const content = document.querySelector('.regex-rules-content');
        const expandBtn = document.getElementById('expandRegexRules');
        const collapseBtn = document.getElementById('collapseRegexRules');
        
        content.classList.remove('expanded');
        content.classList.add('collapsed');
        expandBtn.style.display = 'inline-flex';
        collapseBtn.style.display = 'none';
    }

    /**
     * 设置选项卡切换功能
     */
    setupTabSwitching() {
        // 恢复上次选择的选项卡，如果没有则显示第一个
        const savedTab = localStorage.getItem('activeTab');
        if (savedTab) {
            this.switchToTab(savedTab);
        } else {
            this.switchToTab('options');
        }
    }

    /**
     * 切换选项卡
     */
    switchTab(event) {
        event.preventDefault();
        const targetTab = event.currentTarget.getAttribute('data-tab');
        this.switchToTab(targetTab);
    }

    /**
     * 切换到指定选项卡
     */
    switchToTab(tabName) {
        // 更新选项卡按钮状态
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.remove('active');
            if (btn.getAttribute('data-tab') === tabName) {
                btn.classList.add('active');
            }
        });

        // 更新选项卡内容
        document.querySelectorAll('.tab-pane').forEach(pane => {
            pane.classList.remove('active');
        });

        const targetPane = document.getElementById(`${tabName}Tab`);
        if (targetPane) {
            targetPane.classList.add('active');
        }

        // 保存当前选项卡状态到localStorage
        localStorage.setItem('activeTab', tabName);
    }

    /**
     * 恢复上次选择的选项卡
     */
    restoreActiveTab() {
        const savedTab = localStorage.getItem('activeTab');
        if (savedTab) {
            this.switchToTab(savedTab);
        }
    }
}

// 当DOM加载完成后初始化应用程序
document.addEventListener('DOMContentLoaded', () => {
    window.app = new TextProcessorApp();
});

// 导出类以供测试使用
if (typeof module !== 'undefined' && module.exports) {
    module.exports = TextProcessorApp;
} 