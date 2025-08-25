/**
 * 文本处理Web应用程序的JavaScript逻辑
 * 提供用户交互、API调用和UI更新功能
 */

class TextProcessorApp {
    constructor() {
        this.currentResult = null;
        this.isProcessing = false;
        this.regexRules = [];  // 存储正则规则
        this.inputWindows = [];  // 存储输入窗口信息
        this.outputWindows = [];  // 存储输出窗口信息
        this.nextWindowId = 2;  // 下一个窗口ID
        this.init();
    }

    /**
     * 初始化应用程序
     */
    init() {
        this.initializeWindows();
        this.bindEvents();
        this.updateCharCount();
        this.updateRegexRulesCharCount();
        this.setupViewToggle();
        this.setupToastHandlers();
        this.updateRegexRulesList();  // 初始化正则规则列表
        this.setupRegexRulesWindow();  // 设置正则规则窗口控制
        this.setupTabSwitching();  // 设置选项卡切换
        this.setupSmoothAnimations();  // 设置平滑动画
        this.setupKeyboardShortcuts();  // 设置键盘快捷键
    }

    /**
     * 初始化窗口系统
     */
    initializeWindows() {
        // 初始化第一个输入窗口
        this.inputWindows = [{
            id: 1,
            element: document.getElementById('inputText1'),
            charCount: 0
        }];

        // 初始化第一个输出窗口
        this.outputWindows = [{
            id: 1,
            element: document.getElementById('processedText1'),
            views: {
                processed: document.getElementById('processedView1'),
                statistics: document.getElementById('statisticsView1'),
                analysis: document.getElementById('analysisView1')
            },
            stats: {
                basicStats: document.getElementById('basicStats1'),
                charStats: document.getElementById('charStats1'),
                wordFreq: document.getElementById('wordFreq1'),
                readability: document.getElementById('readability1'),
                sentiment: document.getElementById('sentiment1'),
                languageFeatures: document.getElementById('languageFeatures1')
            }
        }];

        // 更新窗口控制按钮状态
        this.updateWindowControlButtons();
        
        // 从本地存储恢复数据
        this.restoreFromLocalStorage();
    }

    /**
     * 绑定事件监听器
     */
    bindEvents() {
        // 文本输入事件 - 为所有输入窗口绑定事件
        this.bindInputEvents();

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

        // 窗口管理事件
        document.getElementById('addInputWindow').addEventListener('click', () => this.addInputWindow());
        document.getElementById('removeInputWindow').addEventListener('click', () => this.removeInputWindow());
        document.getElementById('addOutputWindow').addEventListener('click', () => this.addOutputWindow());
        document.getElementById('removeOutputWindow').addEventListener('click', () => this.removeOutputWindow());

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
        
        // 提示词管理相关事件
        document.getElementById('selectPromptBtn').addEventListener('click', () => this.showPromptSelectModal());
        document.getElementById('savePromptBtn').addEventListener('click', () => this.showPromptEditModal());
        document.getElementById('addPromptBtn').addEventListener('click', () => this.showPromptEditModal());
        document.getElementById('exportPromptsBtn').addEventListener('click', () => this.exportPrompts());
        document.getElementById('importPromptsBtn').addEventListener('click', () => this.importPrompts());
        document.getElementById('clearPromptsBtn').addEventListener('click', () => this.clearPrompts());
        document.getElementById('promptSaveBtn').addEventListener('click', () => this.savePrompt());
        document.getElementById('promptCategoryFilter').addEventListener('change', () => this.filterPrompts());
        document.getElementById('promptSelectFilter').addEventListener('change', () => this.filterPromptSelect());
        document.getElementById('promptFileInput').addEventListener('change', (e) => this.handlePromptFileImport(e));
        
        // 初始化提示词管理
        this.loadPrompts();
    }

    /**
     * 为所有输入窗口绑定事件
     */
    bindInputEvents() {
        // 为现有的输入窗口绑定事件
        this.inputWindows.forEach(window => {
            this.bindSingleInputEvents(window);
        });
    }

    /**
     * 为单个输入窗口绑定事件
     */
    bindSingleInputEvents(window) {
        const textarea = window.element;
        textarea.addEventListener('input', () => this.updateCharCount());
        textarea.addEventListener('paste', () => this.updateCharCount());
    }

    /**
     * 添加输入窗口
     */
    addInputWindow() {
        const windowId = this.nextWindowId++;
        const container = document.querySelector('.input-windows-container');
        
        // 创建新的输入窗口HTML
        const windowHTML = `
            <div class="input-window-item" data-window-id="${windowId}">
                <div class="textarea-container">
                    <textarea
                        id="inputText${windowId}"
                        class="input-textarea"
                        placeholder="请在此处粘贴或输入要处理的文本..."
                        rows="12"
                        style="resize: vertical; max-height: 800px; min-height: 200px;"
                    ></textarea>
                    <button
                        class="copy-btn"
                        data-target="inputText${windowId}"
                        title="复制文本"
                    >
                        <i class="fas fa-copy"></i>
                    </button>
                </div>
            </div>
        `;
        
        // 插入到容器中
        container.insertAdjacentHTML('beforeend', windowHTML);
        
        // 创建窗口对象
        const newWindow = {
            id: windowId,
            element: document.getElementById(`inputText${windowId}`),
            charCount: 0
        };
        
        // 添加到窗口列表
        this.inputWindows.push(newWindow);
        
        // 绑定事件
        this.bindSingleInputEvents(newWindow);
        
        // 更新窗口控制按钮状态
        this.updateWindowControlButtons();
        
        // 重新绑定复制按钮事件
        this.rebindCopyButtons();
        
        this.showSuccess(`已添加输入窗口 ${windowId}`);
    }

    /**
     * 移除输入窗口
     */
    removeInputWindow() {
        if (this.inputWindows.length <= 1) {
            this.showError('至少需要保留一个输入窗口');
            return;
        }
        
        // 移除最后一个窗口
        const lastWindow = this.inputWindows.pop();
        const windowElement = document.querySelector(`[data-window-id="${lastWindow.id}"]`);
        
        if (windowElement) {
            windowElement.remove();
        }
        
        // 更新窗口控制按钮状态
        this.updateWindowControlButtons();
        
        // 重新绑定复制按钮事件
        this.rebindCopyButtons();
        
        this.showSuccess(`已移除输入窗口 ${lastWindow.id}`);
    }

    /**
     * 添加输出窗口
     */
    addOutputWindow() {
        const windowId = this.nextWindowId++;
        const container = document.querySelector('.output-windows-container');
        
        // 创建新的输出窗口HTML
        const windowHTML = `
            <div class="output-window-item" data-window-id="${windowId}">
                <div class="output-container">
                    <!-- 处理文本视图 -->
                    <div
                        id="processedView${windowId}"
                        class="output-view active"
                    >
                        <div class="text-output">
                            <pre id="processedText${windowId}"></pre>
                            <button
                                class="copy-btn"
                                data-target="processedText${windowId}"
                                title="复制结果"
                            >
                                <i class="fas fa-copy"></i>
                            </button>
                        </div>
                    </div>

                    <!-- 统计信息视图 -->
                    <div id="statisticsView${windowId}" class="output-view">
                        <div class="statistics-grid">
                            <div class="stat-card">
                                <h4>基本统计</h4>
                                <div id="basicStats${windowId}"></div>
                            </div>
                            <div class="stat-card">
                                <h4>字符类型</h4>
                                <div id="charStats${windowId}"></div>
                            </div>
                            <div class="stat-card">
                                <h4>词频统计</h4>
                                <div id="wordFreq${windowId}"></div>
                            </div>
                        </div>
                    </div>

                    <!-- 文本分析视图 -->
                    <div id="analysisView${windowId}" class="output-view">
                        <div class="analysis-grid">
                            <div class="analysis-card">
                                <h4>可读性分析</h4>
                                <div id="readability${windowId}"></div>
                            </div>
                            <div class="analysis-card">
                                <h4>情感分析</h4>
                                <div id="sentiment${windowId}"></div>
                            </div>
                            <div class="analysis-card">
                                <h4>语言特征</h4>
                                <div id="languageFeatures${windowId}"></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        // 插入到容器中
        container.insertAdjacentHTML('beforeend', windowHTML);
        
        // 创建窗口对象
        const newWindow = {
            id: windowId,
            element: document.getElementById(`processedText${windowId}`),
            views: {
                processed: document.getElementById(`processedView${windowId}`),
                statistics: document.getElementById(`statisticsView${windowId}`),
                analysis: document.getElementById(`analysisView${windowId}`)
            },
            stats: {
                basicStats: document.getElementById(`basicStats${windowId}`),
                charStats: document.getElementById(`charStats${windowId}`),
                wordFreq: document.getElementById(`wordFreq${windowId}`),
                readability: document.getElementById(`readability${windowId}`),
                sentiment: document.getElementById(`sentiment${windowId}`),
                languageFeatures: document.getElementById(`languageFeatures${windowId}`)
            }
        };
        
        // 添加到窗口列表
        this.outputWindows.push(newWindow);
        
        // 更新窗口控制按钮状态
        this.updateWindowControlButtons();
        
        // 重新绑定复制按钮事件
        this.rebindCopyButtons();
        
        this.showSuccess(`已添加输出窗口 ${windowId}`);
    }

    /**
     * 移除输出窗口
     */
    removeOutputWindow() {
        if (this.outputWindows.length <= 1) {
            this.showError('至少需要保留一个输出窗口');
            return;
        }
        
        // 移除最后一个窗口
        const lastWindow = this.outputWindows.pop();
        const windowElement = document.querySelector(`[data-window-id="${lastWindow.id}"]`);
        
        if (windowElement) {
            windowElement.remove();
        }
        
        // 更新窗口控制按钮状态
        this.updateWindowControlButtons();
        
        // 重新绑定复制按钮事件
        this.rebindCopyButtons();
        
        this.showSuccess(`已移除输出窗口 ${lastWindow.id}`);
    }

    /**
     * 更新窗口控制按钮状态
     */
    updateWindowControlButtons() {
        const addInputBtn = document.getElementById('addInputWindow');
        const removeInputBtn = document.getElementById('removeInputWindow');
        const addOutputBtn = document.getElementById('addOutputWindow');
        const removeOutputBtn = document.getElementById('removeOutputWindow');
        
        // 输入窗口控制
        removeInputBtn.disabled = this.inputWindows.length <= 1;
        
        // 输出窗口控制
        removeOutputBtn.disabled = this.outputWindows.length <= 1;
    }

    /**
     * 重新绑定复制按钮事件
     */
    rebindCopyButtons() {
        // 移除所有现有的复制按钮事件
        document.querySelectorAll('.copy-btn').forEach(btn => {
            btn.replaceWith(btn.cloneNode(true));
        });
        
        // 重新绑定事件
        document.querySelectorAll('.copy-btn').forEach(btn => {
            btn.addEventListener('click', (e) => this.copyText(e));
        });
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
        
        // Ctrl+Shift+R 正则处理
        if (e.ctrlKey && e.shiftKey && e.key === 'R') {
            e.preventDefault();
            this.processRegex();
        }
        
        // Ctrl+Shift+T 翻译
        if (e.ctrlKey && e.shiftKey && e.key === 'T') {
            e.preventDefault();
            this.translateText();
        }
        
        // Ctrl+Shift+1-9 切换选项卡
        if (e.ctrlKey && e.shiftKey && /^[1-9]$/.test(e.key)) {
            e.preventDefault();
            const tabIndex = parseInt(e.key) - 1;
            const tabs = ['options', 'translation', 'regex'];
            if (tabs[tabIndex]) {
                this.switchToTab(tabs[tabIndex]);
            }
        }
    }

    /**
     * 更新字符计数
     */
    updateCharCount() {
        const charCount = document.getElementById('charCount');
        const textCounter = charCount.closest('.text-counter');
        let totalCount = 0;
        
        // 计算所有输入窗口的字符总数
        this.inputWindows.forEach(window => {
            totalCount += window.element.value.length;
        });
        
        charCount.textContent = totalCount.toLocaleString();
        
        // 根据字符数改变整个text-counter div的背景颜色和样式类
        // 先移除所有状态类
        textCounter.classList.remove('counter-empty', 'counter-low', 'counter-medium', 'counter-high');
        
        if (totalCount === 0) {
            textCounter.style.background = 'var(--counter-empty)';
            textCounter.classList.add('counter-empty');
        } else if (totalCount < 500) {
            textCounter.style.background = 'var(--counter-low)';
            textCounter.classList.add('counter-low');
        } else if (totalCount < 2500) {
            textCounter.style.background = 'var(--counter-medium)';
            textCounter.classList.add('counter-medium');
        } else {
            textCounter.style.background = 'var(--counter-high)';
            textCounter.classList.add('counter-high');
        }
    }

    /**
     * 更新正则规则字符计数
     */
    updateRegexRulesCharCount() {
        const regexReplaceRules = document.getElementById('regexReplaceRules');
        const regexCount = regexReplaceRules.value.length;
        const regexCharCount = document.getElementById('regexRulesCharCount');
        const textCounter = regexCharCount.closest('.text-counter');
        regexCharCount.textContent = regexCount.toLocaleString();

        // 根据字符数改变整个text-counter div的背景颜色和样式类
        // 先移除所有状态类
        textCounter.classList.remove('counter-empty', 'counter-low', 'counter-medium', 'counter-high');
        
        if (regexCount === 0) {
            textCounter.style.background = 'var(--counter-empty)';
            textCounter.classList.add('counter-empty');
        } else if (regexCount < 500) {
            textCounter.style.background = 'var(--counter-low)';
            textCounter.classList.add('counter-low');
        } else if (regexCount < 2500) {
            textCounter.style.background = 'var(--counter-medium)';
            textCounter.classList.add('counter-medium');
        } else {
            textCounter.style.background = 'var(--counter-high)';
            textCounter.classList.add('counter-high');
        }
    }

    /**
     * 设置视图切换功能
     */
    setupViewToggle() {
        const toggleButtons = document.querySelectorAll('.toggle-btn');

        toggleButtons.forEach(button => {
            button.addEventListener('click', () => {
                const targetView = button.getAttribute('data-view');
                
                // 更新按钮状态
                toggleButtons.forEach(btn => btn.classList.remove('active'));
                button.classList.add('active');
                
                // 更新所有输出窗口的视图显示
                this.outputWindows.forEach(window => {
                    Object.values(window.views).forEach(view => {
                        view.classList.remove('active');
                    });
                    if (window.views[targetView]) {
                        window.views[targetView].classList.add('active');
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
        // 收集所有输入窗口的文本
        const inputTexts = this.inputWindows.map(window => window.element.value.trim()).filter(text => text);
        
        if (inputTexts.length === 0) {
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
            
            // 为每个输入文本创建处理任务
            const processingTasks = inputTexts.map(async (text, index) => {
                try {
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
                    
                    return {
                        index: index,
                        data: data,
                        success: true
                    };
                } catch (error) {
                    console.error(`处理文本 ${index + 1} 时发生错误:`, error);
                    return {
                        index: index,
                        error: error.message || '处理失败',
                        success: false
                    };
                }
            });

            // 等待所有处理任务完成
            const results = await Promise.all(processingTasks);
            
            // 更新UI显示结果
            this.updateUIWithMultipleResults(results);
            
            // 保存当前结果
            this.currentResult = results;
            
            this.showEnhancedSuccess(`文本处理完成，共处理 ${results.filter(r => r.success).length} 个文本`);

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
        // 收集所有输入窗口的文本
        const inputTexts = this.inputWindows.map(window => window.element.value.trim()).filter(text => text);

        if (inputTexts.length === 0) {
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
            // 为每个输入文本创建处理任务
            const processingTasks = inputTexts.map(async (text, index) => {
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
                    
                    return {
                        index: index,
                        data: data,
                        success: true
                    };
                } catch (error) {
                    console.error(`正则处理文本 ${index + 1} 时发生错误:`, error);
                    return {
                        index: index,
                        error: error.message || '正则处理失败',
                        success: false
                    };
                }
            });

            // 等待所有处理任务完成
            const results = await Promise.all(processingTasks);
            
            // 更新UI显示结果
            this.updateUIWithRegexResults(results);
            
            // 保存当前结果
            this.currentResult = results;
            
            this.showEnhancedSuccess(`正则处理完成，共处理 ${results.filter(r => r.success).length} 个文本`);

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
    updateUIWithRegexResults(results) {
        // 确保有足够的输出窗口
        while (this.outputWindows.length < results.length) {
            this.addOutputWindow();
        }
        
        // 为每个结果分配一个输出窗口
        results.forEach((result, index) => {
            if (index < this.outputWindows.length) {
                const outputWindow = this.outputWindows[index];
                
                if (result.success) {
                    // 更新处理后的文本
                    outputWindow.element.textContent = result.data.processed_text || '';
                } else {
                    // 显示错误信息
                    outputWindow.element.textContent = `正则处理失败: ${result.error}`;
                }
            }
        });
        
        // 切换到处理文本视图
        this.switchToView('processed');
    }

    /**
     * 切换到指定视图
     */
    switchToView(viewName) {
        const toggleButtons = document.querySelectorAll('.toggle-btn');
        
        // 更新按钮状态
        toggleButtons.forEach(btn => btn.classList.remove('active'));
        const targetButton = document.querySelector(`[data-view="${viewName}"]`);
        if (targetButton) {
            targetButton.classList.add('active');
        }
        
        // 更新所有输出窗口的视图显示
        this.outputWindows.forEach(window => {
            Object.values(window.views).forEach(view => {
                view.classList.remove('active');
            });
            if (window.views[viewName]) {
                window.views[viewName].classList.add('active');
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

            // 清空所有输入窗口
            this.inputWindows.forEach(window => {
                window.element.value = '';
            });
            this.updateCharCount();

            // 清空正则规则输入
            document.getElementById('regexReplaceRules').value = '';
            this.updateRegexRulesCharCount();

            // 清空所有输出窗口
            this.outputWindows.forEach(window => {
                window.element.textContent = '';
                this.clearWindowStats(window);
            });

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
        const totalLength = this.inputWindows.reduce((sum, window) => sum + window.element.value.trim().length, 0);
        if (totalLength > 3000) {
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
        return undefined;
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
            const rawTupleMatch = line.match(/\(\s*r(["'])([\s\S]*?)\1\s*,\s*r(["'])([\s\S]*?)\3\s*\)/);
            if (rawTupleMatch) {
                const pattern = rawTupleMatch[2];
                const replacement = rawTupleMatch[4];
                rules.push([pattern, replacement]);
                continue;
            }
            // 兼容旧逻辑（同种引号）
            const oldRawTupleMatch = line.match(/\(\s*r["']([^"']*)["']\s*,\s*r["']([^"']*)["']\s*\)/);
            if (oldRawTupleMatch) {
                const pattern = oldRawTupleMatch[1];
                const replacement = oldRawTupleMatch[2];
                rules.push([pattern, replacement]);
                continue;
            }
            
            // 匹配 ("pattern", "replacement") 格式 - 需要转义处理
            const simpleMatch = line.match(/\(\s*["']([^"']*)["']\s*,\s*["']([^"']*)["']\s*\)/);
            if (simpleMatch) {
                const pattern = this.escapeRegexPattern(simpleMatch[1]);
                const replacement = this.escapeRegexReplacement(simpleMatch[2]);
                rules.push([pattern, replacement]);
                continue;
            }
            
            // 匹配 s/pattern/replacement/ 格式
            const sedMatch = line.match(/^s\/([^\/]*)\/([^\/]*)\/?$/);
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
        
        console.log('Copy button clicked:', { targetId, targetElement, button });
        
        if (!targetElement) {
            this.showError('找不到目标元素');
            return;
        }
        
        let textToCopy = '';
        
        // 检查是否是处理结果元素（processedText1, processedText2, etc.）
        if (targetId.startsWith('processedText')) {
            textToCopy = targetElement.textContent;
            console.log('Copying from processed text element:', { targetId, textLength: textToCopy.length, textContent: textToCopy });
        } else {
            textToCopy = targetElement.value;
            console.log('Copying from input element:', { targetId, textLength: textToCopy.length, textContent: textToCopy });
        }
        
        if (!textToCopy.trim()) {
            this.showError('没有内容可复制');
            return;
        }
        
        try {
            // 尝试使用现代 Clipboard API
            if (navigator.clipboard && navigator.clipboard.writeText) {
                console.log('Using modern Clipboard API');
                
                // 检查权限
                if (navigator.permissions) {
                    try {
                        const permission = await navigator.permissions.query({ name: 'clipboard-write' });
                        console.log('Clipboard permission state:', permission.state);
                        if (permission.state === 'denied') {
                            throw new Error('剪贴板权限被拒绝');
                        }
                    } catch (permErr) {
                        console.log('Permission check failed, continuing with clipboard API:', permErr);
                    }
                }
                
                await navigator.clipboard.writeText(textToCopy);
                console.log('Clipboard API copy successful');
            } else {
                console.log('Clipboard API not available, using fallback method');
                // 降级到传统方法
                this.fallbackCopyTextToClipboard(textToCopy);
            }
            
            // 显示复制成功状态
            button.classList.add('copied');
            setTimeout(() => {
                button.classList.remove('copied');
            }, 2000);
            
            this.showSuccess('文本已复制到剪贴板');
        } catch (err) {
            console.error('复制文本失败:', err);
            
            // 如果是权限问题，给出具体提示
            if (err.message.includes('权限') || err.message.includes('permission')) {
                this.showError('剪贴板权限被拒绝，请允许网站访问剪贴板或使用手动复制');
                return;
            }
            
            // 尝试降级方法
            try {
                this.fallbackCopyTextToClipboard(textToCopy);
                this.showSuccess('文本已复制到剪贴板（使用降级方法）');
            } catch (fallbackErr) {
                console.error('降级复制方法也失败:', fallbackErr);
                this.showError('复制文本失败，请手动选择文本复制');
            }
        }
    }

    /**
     * 降级复制文本到剪贴板的方法
     */
    fallbackCopyTextToClipboard(text) {
        console.log('Using fallback copy method');
        const textArea = document.createElement('textarea');
        textArea.value = text;
        
        // 避免滚动到页面底部
        textArea.style.top = '0';
        textArea.style.left = '0';
        textArea.style.position = 'fixed';
        textArea.style.opacity = '0';
        
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        
        try {
            const successful = document.execCommand('copy');
            console.log('execCommand copy result:', successful);
            if (!successful) {
                throw new Error('execCommand copy failed');
            }
        } finally {
            document.body.removeChild(textArea);
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
            if (!serviceSelect) return;
            
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
            if (!modelSelect) return;
            
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
            if (apiKeyInput && data.user_config && data.user_config.has_api_key) {
                apiKeyInput.value = '••••••••••••••••'; // 显示占位符
                apiKeyInput.setAttribute('data-has-key', 'true');
            } else if (apiKeyInput) {
                apiKeyInput.value = '';
                apiKeyInput.removeAttribute('data-has-key');
            }
            
            // 更新模型选择
            const modelSelect = document.getElementById('modelSelect');
            if (modelSelect && data.user_config && data.user_config.model) {
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
        
        if (!serviceSelect || !apiKeyInput || !modelSelect) {
            this.showError('找不到必要的表单元素');
            return;
        }
        
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
        if (!serviceSelect) {
            this.showError('找不到翻译服务选择器');
            return;
        }
        
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
            
            if (apiKeyInput) {
                apiKeyInput.value = '';
                apiKeyInput.removeAttribute('data-has-key');
            }
            if (modelSelect) {
                modelSelect.value = '';
            }
            
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
        if (!serviceSelect) {
            this.showError('找不到翻译服务选择器');
            return;
        }
        
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
        if (statusElement) {
            statusElement.className = `api-config-status ${type}`;
            statusElement.textContent = message;
        }
    }

    /**
     * 切换API密钥显示/隐藏
     */
    toggleApiKeyVisibility() {
        const apiKeyInput = document.getElementById('apiKeyInput');
        const toggleBtn = document.getElementById('toggleApiKeyBtn');
        
        if (!apiKeyInput || !toggleBtn) return;
        
        const icon = toggleBtn.querySelector('i');
        if (!icon) return;
        
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
            
            if (apiKeyInput) apiKeyInput.value = '';
            if (apiKeyInput) apiKeyInput.removeAttribute('data-has-key');
            if (modelSelect) modelSelect.innerHTML = '<option value="">请先选择翻译服务</option>';
            if (statusElement) {
                statusElement.className = 'api-config-status';
                statusElement.textContent = '';
            }
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
        
        if (!apiKeyInput) return;
        
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
        // 收集所有输入窗口的文本
        const inputTexts = this.inputWindows.map(window => window.element.value.trim()).filter(text => text);
        const translationPrompt = document.getElementById('translationPrompt').value.trim();
        const translationService = document.getElementById('translationService').value;
        
        if (inputTexts.length === 0) {
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
        const totalLength = inputTexts.reduce((sum, text) => sum + text.length, 0);
        if (totalLength > 3000) {
            const confirmLongText = confirm(
                `检测到长文本（${totalLength}个字符），翻译可能需要较长时间。\n\n` +
                `系统将自动分段翻译，请耐心等待。\n\n` +
                `是否继续翻译？`
            );
            if (!confirmLongText) {
                return;
            }
        }
        
        this.showLoading();
        
        try {
            // 为每个输入文本创建翻译任务
            const translationTasks = inputTexts.map(async (text, index) => {
                try {
                    const response = await fetch('/api/translate', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            text: text,
                            prompt: translationPrompt,
                            service_name: translationService
                        })
                    });
                    
                    const result = await response.json();
                    
                    if (result.error) {
                        throw new Error(result.error);
                    }
                    
                    // 提取数据（API返回的数据在result.data中）
                    const data = result.data || result;
                    
                    return {
                        index: index,
                        data: data,
                        success: true
                    };
                } catch (error) {
                    console.error(`翻译文本 ${index + 1} 时发生错误:`, error);
                    return {
                        index: index,
                        error: error.message || '翻译失败',
                        success: false
                    };
                }
            });

            // 等待所有翻译任务完成
            const results = await Promise.all(translationTasks);
            
            // 更新UI显示结果
            this.updateUIWithTranslationResults(results);
            
            // 更新当前结果
            this.currentResult = results;
            
                    // 根据翻译结果显示不同的成功消息
        const successCount = results.filter(r => r.success).length;
        if (successCount > 1) {
            this.showEnhancedSuccess(`翻译完成！共翻译了${successCount}个文本段`);
        } else {
            this.showEnhancedSuccess('翻译完成');
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
    updateUIWithTranslationResults(results) {
        // 确保有足够的输出窗口
        while (this.outputWindows.length < results.length) {
            this.addOutputWindow();
        }
        
        // 为每个结果分配一个输出窗口
        results.forEach((result, index) => {
            if (index < this.outputWindows.length) {
                const outputWindow = this.outputWindows[index];
                
                if (result.success) {
                    // 更新处理后的文本
                    outputWindow.element.textContent = result.data.translated_text || '';
                    
                    // 更新统计信息
                    if (result.data.statistics) {
                        this.updateStatisticsForWindow(result.data.statistics, outputWindow);
                    }

                    // 更新分析结果
                    if (result.data.analysis) {
                        this.updateAnalysisForWindow(result.data.analysis, outputWindow);
                    }
                } else {
                    // 显示错误信息
                    outputWindow.element.textContent = `翻译失败: ${result.error}`;
                    
                    // 清空统计和分析信息
                    this.clearWindowStats(outputWindow);
                }
            }
        });
        
        // 切换到处理文本视图
        this.switchToView('processed');
    }

    /**
     * 导入正则规则
     */
    importRegexRules() {
        const fileInput = document.getElementById('regexFileInput');
        if (fileInput) {
            fileInput.click();
        }
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
                if (regexReplaceRules) {
                    const rulesText = rules.map(rule => {
                        const [pattern, replacement] = rule;
                        return `(r"${pattern}", r"${replacement}")`;
                    }).join(',\n');
                    regexReplaceRules.value = rulesText;
                    this.updateRegexRulesCharCount();
                }
                
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

    /* 移除拖动分隔线功能 */

    /**
     * 设置正则规则窗口控制
     */
    setupRegexRulesWindow() {
        const content = document.querySelector('.regex-rules-content');
        const expandBtn = document.getElementById('expandRegexRules');
        const collapseBtn = document.getElementById('collapseRegexRules');
        
        if (!content || !expandBtn || !collapseBtn) return;
        
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
        
        if (!content || !expandBtn || !collapseBtn) return;
        
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
        
        if (!content || !expandBtn || !collapseBtn) return;
        
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
        if (targetTab) {
            this.switchToTab(targetTab);
        }
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

    /**
     * 设置平滑动画
     */
    setupSmoothAnimations() {
        // 为所有卡片添加进入动画
        const cards = document.querySelectorAll('.stat-card, .analysis-card, .card');
        cards.forEach((card, index) => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            
            setTimeout(() => {
                card.style.transition = 'all 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }, index * 100);
        });

        // 为按钮添加悬停动画
        const buttons = document.querySelectorAll('.btn');
        buttons.forEach(button => {
            button.addEventListener('mouseenter', () => {
                button.style.transform = 'translateY(-2px) scale(1.02)';
            });
            
            button.addEventListener('mouseleave', () => {
                button.style.transform = 'translateY(0) scale(1)';
            });
        });
    }

    // ==================== 提示词管理方法 ====================

    /**
     * 加载提示词列表
     */
    async loadPrompts() {
        try {
            const response = await fetch('/api/prompts');
            const result = await response.json();
            
            if (result.error) {
                console.error('加载提示词失败:', result.error);
                return;
            }
            
            const data = result.data || result;
            this.prompts = data.prompts || [];
            this.updatePromptList();
            
        } catch (error) {
            console.error('加载提示词失败:', error);
        }
    }

    /**
     * 更新提示词列表显示
     */
    updatePromptList() {
        const promptList = document.getElementById('promptList');
        const categoryFilter = document.getElementById('promptCategoryFilter');
        
        if (!promptList) return;
        
        // 过滤提示词
        let filteredPrompts = this.prompts || [];
        if (categoryFilter && categoryFilter.value) {
            filteredPrompts = filteredPrompts.filter(prompt => prompt.category === categoryFilter.value);
        }
        
        if (filteredPrompts.length === 0) {
            promptList.innerHTML = '<div class="prompt-item"><div class="prompt-item-info"><div class="prompt-item-content">暂无提示词</div></div></div>';
            return;
        }
        
        promptList.innerHTML = filteredPrompts.map(prompt => this.createPromptItemHTML(prompt)).join('');
        
        // 绑定提示词项的事件
        this.bindPromptItemEvents();
    }

    /**
     * 创建提示词项HTML
     */
    createPromptItemHTML(prompt) {
        const isUserCreated = prompt.is_user_created || false;
        const actionsHTML = isUserCreated ? 
            `<div class="prompt-item-actions">
                <button class="btn btn-sm btn-use" data-prompt-id="${prompt.id}" title="使用此提示词">
                    <i class="fas fa-play"></i>
                </button>
                <button class="btn btn-sm btn-edit" data-prompt-id="${prompt.id}" title="编辑">
                    <i class="fas fa-edit"></i>
                </button>
                <button class="btn btn-sm btn-delete" data-prompt-id="${prompt.id}" title="删除">
                    <i class="fas fa-trash"></i>
                </button>
            </div>` :
            `<div class="prompt-item-actions">
                <button class="btn btn-sm btn-use" data-prompt-id="${prompt.id}" title="使用此提示词">
                    <i class="fas fa-play"></i>
                </button>
            </div>`;
        
        return `
            <div class="prompt-item" data-prompt-id="${prompt.id}">
                <div class="prompt-item-info">
                    <div class="prompt-item-name">${prompt.name}</div>
                    <div class="prompt-item-content">${prompt.content}</div>
                    <span class="prompt-item-category">${this.getCategoryDisplayName(prompt.category)}</span>
                </div>
                ${actionsHTML}
            </div>
        `;
    }

    /**
     * 绑定提示词项事件
     */
    bindPromptItemEvents() {
        // 使用提示词
        document.querySelectorAll('.btn-use').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                const promptId = btn.getAttribute('data-prompt-id');
                this.usePrompt(promptId);
            });
        });
        
        // 编辑提示词
        document.querySelectorAll('.btn-edit').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                const promptId = btn.getAttribute('data-prompt-id');
                this.editPrompt(promptId);
            });
        });
        
        // 删除提示词
        document.querySelectorAll('.btn-delete').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                const promptId = btn.getAttribute('data-prompt-id');
                this.deletePrompt(promptId);
            });
        });
    }

    /**
     * 使用提示词
     */
    usePrompt(promptId) {
        const prompt = this.prompts.find(p => p.id === promptId);
        if (prompt) {
            document.getElementById('translationPrompt').value = prompt.content;
            this.showSuccess(`已选择提示词: ${prompt.name}`);
        }
    }

    /**
     * 编辑提示词
     */
    editPrompt(promptId) {
        const prompt = this.prompts.find(p => p.id === promptId);
        if (prompt) {
            this.currentEditingPromptId = promptId;
            document.getElementById('promptEditModalTitle').innerHTML = '<i class="fas fa-edit"></i> 编辑提示词';
            document.getElementById('promptNameInput').value = prompt.name;
            document.getElementById('promptContentInput').value = prompt.content;
            document.getElementById('promptCategoryInput').value = prompt.category;
            this.showPromptEditModal();
        }
    }

    /**
     * 删除提示词
     */
    async deletePrompt(promptId) {
        const prompt = this.prompts.find(p => p.id === promptId);
        if (!prompt) return;
        
        const confirmDelete = confirm(`确定要删除提示词 "${prompt.name}" 吗？`);
        if (!confirmDelete) return;
        
        try {
            const response = await fetch(`/api/prompts/${promptId}`, {
                method: 'DELETE'
            });
            
            const result = await response.json();
            
            if (result.error) {
                this.showError(result.error);
                return;
            }
            
            this.showSuccess('提示词删除成功');
            await this.loadPrompts();
            
        } catch (error) {
            console.error('删除提示词失败:', error);
            this.showError('删除提示词失败');
        }
    }

    /**
     * 显示提示词选择模态框
     */
    showPromptSelectModal() {
        this.updatePromptSelectList();
        document.getElementById('promptSelectModal').style.display = 'block';
    }

    /**
     * 显示提示词编辑模态框
     */
    showPromptEditModal() {
        if (!this.currentEditingPromptId) {
            // 新建模式
            document.getElementById('promptEditModalTitle').innerHTML = '<i class="fas fa-plus"></i> 添加提示词';
            document.getElementById('promptNameInput').value = '';
            document.getElementById('promptContentInput').value = '';
            document.getElementById('promptCategoryInput').value = 'custom';
        }
        document.getElementById('promptEditModal').style.display = 'block';
    }

    /**
     * 关闭模态框
     */
    closePromptModal() {
        document.getElementById('promptSelectModal').style.display = 'none';
        document.getElementById('promptEditModal').style.display = 'none';
        this.currentEditingPromptId = null;
    }

    /**
     * 更新提示词选择列表
     */
    updatePromptSelectList() {
        const promptSelectList = document.getElementById('promptSelectList');
        const categoryFilter = document.getElementById('promptSelectFilter').value;
        
        // 过滤提示词
        let filteredPrompts = this.prompts;
        if (categoryFilter) {
            filteredPrompts = this.prompts.filter(prompt => prompt.category === categoryFilter);
        }
        
        if (filteredPrompts.length === 0) {
            promptSelectList.innerHTML = '<div class="prompt-item"><div class="prompt-item-info"><div class="prompt-item-content">暂无提示词</div></div></div>';
            return;
        }
        
        promptSelectList.innerHTML = filteredPrompts.map(prompt => `
            <div class="prompt-item" onclick="app.selectPrompt('${prompt.id}')">
                <div class="prompt-item-info">
                    <div class="prompt-item-name">${prompt.name}</div>
                    <div class="prompt-item-content">${prompt.content}</div>
                    <span class="prompt-item-category">${this.getCategoryDisplayName(prompt.category)}</span>
                </div>
            </div>
        `).join('');
    }

    /**
     * 选择提示词
     */
    selectPrompt(promptId) {
        this.usePrompt(promptId);
        this.closePromptModal();
    }

    /**
     * 保存提示词
     */
    async savePrompt() {
        const name = document.getElementById('promptNameInput').value.trim();
        const content = document.getElementById('promptContentInput').value.trim();
        const category = document.getElementById('promptCategoryInput').value;
        
        if (!name || !content) {
            this.showError('请填写完整的提示词信息');
            return;
        }
        
        try {
            const url = this.currentEditingPromptId ? 
                `/api/prompts/${this.currentEditingPromptId}` : 
                '/api/prompts';
            
            const method = this.currentEditingPromptId ? 'PUT' : 'POST';
            
            const response = await fetch(url, {
                method: method,
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    name: name,
                    content: content,
                    category: category
                })
            });
            
            const result = await response.json();
            
            if (result.error) {
                this.showError(result.error);
                return;
            }
            
            this.showSuccess(this.currentEditingPromptId ? '提示词更新成功' : '提示词添加成功');
            this.closePromptModal();
            await this.loadPrompts();
            
        } catch (error) {
            console.error('保存提示词失败:', error);
            this.showError('保存提示词失败');
        }
    }

    /**
     * 导出提示词
     */
    async exportPrompts() {
        try {
            const response = await fetch('/api/prompts/export');
            const result = await response.json();
            
            if (result.error) {
                this.showError(result.error);
                return;
            }
            
            const data = result.data || result;
            const exportData = data.export_data;
            
            // 创建下载链接
            const blob = new Blob([exportData], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `prompts_${new Date().toISOString().slice(0, 10)}.json`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
            
            this.showSuccess('提示词导出成功');
            
        } catch (error) {
            console.error('导出提示词失败:', error);
            this.showError('导出提示词失败');
        }
    }

    /**
     * 导入提示词
     */
    importPrompts() {
        document.getElementById('promptFileInput').click();
    }

    /**
     * 处理提示词文件导入
     */
    async handlePromptFileImport(event) {
        const file = event.target.files[0];
        if (!file) return;

        const reader = new FileReader();
        reader.onload = async (e) => {
            try {
                const jsonData = e.target.result;
                
                const response = await fetch('/api/prompts/import', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        json_data: jsonData
                    })
                });
                
                const result = await response.json();
                
                if (result.error) {
                    this.showError(result.error);
                    return;
                }
                
                const data = result.data || result;
                this.showSuccess(`提示词导入成功！导入${data.imported_count}个，跳过${data.skipped_count}个`);
                
                if (data.errors && data.errors.length > 0) {
                    console.warn('导入错误:', data.errors);
                }
                
                await this.loadPrompts();
                
            } catch (error) {
                console.error('导入提示词失败:', error);
                this.showError('导入提示词失败');
            }
        };
        reader.readAsText(file);
    }

    /**
     * 清空提示词
     */
    async clearPrompts() {
        const confirmClear = confirm('确定要清空所有用户提示词吗？此操作不可恢复！');
        if (!confirmClear) return;
        
        try {
            const response = await fetch('/api/prompts/clear', {
                method: 'DELETE'
            });
            
            const result = await response.json();
            
            if (result.error) {
                this.showError(result.error);
                return;
            }
            
            this.showSuccess('所有用户提示词已清空');
            await this.loadPrompts();
            
        } catch (error) {
            console.error('清空提示词失败:', error);
            this.showError('清空提示词失败');
        }
    }

    /**
     * 过滤提示词
     */
    filterPrompts() {
        this.updatePromptList();
    }

    /**
     * 过滤提示词选择
     */
    filterPromptSelect() {
        this.updatePromptSelectList();
    }

    /**
     * 获取分类显示名称
     */
    getCategoryDisplayName(category) {
        const categoryNames = {
            'translation': '翻译',
            'polish': '润色',
            'summary': '总结',
            'custom': '自定义',
            'imported': '导入'
        };
        return categoryNames[category] || category;
    }

    /**
     * 使用多个结果更新UI
     */
    updateUIWithMultipleResults(results) {
        // 确保有足够的输出窗口
        while (this.outputWindows.length < results.length) {
            this.addOutputWindow();
        }
        
        // 为每个结果分配一个输出窗口
        results.forEach((result, index) => {
            if (index < this.outputWindows.length) {
                const outputWindow = this.outputWindows[index];
                
                if (result.success) {
                    // 更新处理后的文本
                    outputWindow.element.textContent = result.data.processed_text || '';
                    
                    // 更新统计信息
                    if (result.data.statistics) {
                        this.updateStatisticsForWindow(result.data.statistics, outputWindow);
                    }

                    // 更新分析结果
                    if (result.data.analysis) {
                        this.updateAnalysisForWindow(result.data.analysis, outputWindow);
                    }
                } else {
                    // 显示错误信息
                    outputWindow.element.textContent = `处理失败: ${result.error}`;
                    
                    // 清空统计和分析信息
                    this.clearWindowStats(outputWindow);
                }
            }
        });
        
        // 切换到处理文本视图
        this.switchToView('processed');
    }

    /**
     * 为指定窗口更新统计信息
     */
    updateStatisticsForWindow(stats, outputWindow) {
        if (!outputWindow.stats) return;
        
        // 基本统计
        if (stats.basic && outputWindow.stats.basicStats) {
            outputWindow.stats.basicStats.innerHTML = this.createStatItems(stats.basic);
        }

        // 字符类型统计
        if (stats.character_types && outputWindow.stats.charStats) {
            outputWindow.stats.charStats.innerHTML = this.createStatItems(stats.character_types);
        }

        // 词频统计
        if (stats.word_frequency && outputWindow.stats.wordFreq) {
            outputWindow.stats.wordFreq.innerHTML = this.createWordFrequencyList(stats.word_frequency);
        }
    }

    /**
     * 为指定窗口更新分析结果
     */
    updateAnalysisForWindow(analysis, outputWindow) {
        if (!outputWindow.stats) return;
        
        // 可读性分析
        if (analysis.readability && outputWindow.stats.readability) {
            outputWindow.stats.readability.innerHTML = this.createReadabilityDisplay(analysis.readability);
        }

        // 情感分析
        if (analysis.sentiment && outputWindow.stats.sentiment) {
            outputWindow.stats.sentiment.innerHTML = this.createSentimentDisplay(analysis.sentiment);
        }

        // 语言特征
        if (analysis.language_features && outputWindow.stats.languageFeatures) {
            outputWindow.stats.languageFeatures.innerHTML = this.createLanguageFeaturesDisplay(analysis.language_features);
        }
    }

    /**
     * 清空指定窗口的统计信息
     */
    clearWindowStats(outputWindow) {
        if (outputWindow.stats) {
            if (outputWindow.stats.basicStats) outputWindow.stats.basicStats.innerHTML = '';
            if (outputWindow.stats.charStats) outputWindow.stats.charStats.innerHTML = '';
            if (outputWindow.stats.wordFreq) outputWindow.stats.wordFreq.innerHTML = '';
            if (outputWindow.stats.readability) outputWindow.stats.readability.innerHTML = '';
            if (outputWindow.stats.sentiment) outputWindow.stats.sentiment.innerHTML = '';
            if (outputWindow.stats.languageFeatures) outputWindow.stats.languageFeatures.innerHTML = '';
        }
    }

    /**
     * 设置平滑动画
     */
    setupSmoothAnimations() {
        // 为所有卡片添加进入动画
        const cards = document.querySelectorAll('.stat-card, .analysis-card, .card');
        cards.forEach((card, index) => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            
            setTimeout(() => {
                card.style.transition = 'all 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }, index * 100);
        });

        // 为按钮添加悬停动画
        const buttons = document.querySelectorAll('.btn');
        buttons.forEach(button => {
            button.addEventListener('mouseenter', () => {
                button.style.transform = 'translateY(-2px) scale(1.02)';
            });
            
            button.addEventListener('mouseleave', () => {
                button.style.transform = 'translateY(0) scale(1)';
            });
        });
    }

    /**
     * 设置增强的键盘快捷键
     */
    setupKeyboardShortcuts() {
        // 显示快捷键提示
        this.showKeyboardShortcutsHelp();
        
        // 为输入框添加自动保存功能
        this.setupAutoSave();
    }

    /**
     * 显示键盘快捷键帮助
     */
    showKeyboardShortcutsHelp() {
        const helpText = `
            <div class="keyboard-shortcuts-help" style="
                position: fixed;
                bottom: 20px;
                left: 20px;
                background: var(--surface-color);
                padding: 16px;
                border-radius: var(--border-radius-sm);
                box-shadow: var(--shadow-lg);
                border: 1px solid var(--border-light);
                font-size: 0.85rem;
                color: var(--text-secondary);
                z-index: 999;
                max-width: 300px;
                opacity: 0.8;
                transition: opacity 0.3s ease;
            ">
                <strong>键盘快捷键:</strong><br>
                Ctrl+Enter: 处理文本<br>
                Ctrl+Shift+C: 清空所有<br>
                Ctrl+Shift+R: 正则处理<br>
                Ctrl+Shift+T: 翻译<br>
                Ctrl+Shift+1-4: 切换选项卡
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', helpText);
        
        // 点击隐藏帮助
        const helpElement = document.querySelector('.keyboard-shortcuts-help');
        helpElement.addEventListener('click', () => {
            helpElement.style.opacity = '0';
            setTimeout(() => helpElement.remove(), 300);
        });
        
        // 5秒后自动隐藏
        setTimeout(() => {
            if (helpElement) {
                helpElement.style.opacity = '0';
                setTimeout(() => helpElement.remove(), 300);
            }
        }, 5000);
    }

    /**
     * 设置自动保存功能
     */
    setupAutoSave() {
        let autoSaveTimer;
        
        this.inputWindows.forEach(window => {
            window.element.addEventListener('input', () => {
                clearTimeout(autoSaveTimer);
                autoSaveTimer = setTimeout(() => {
                    this.saveToLocalStorage();
                }, 2000); // 2秒后自动保存
            });
        });
    }

    /**
     * 保存到本地存储
     */
    saveToLocalStorage() {
        const data = {
            inputTexts: this.inputWindows.map(w => w.element.value),
            regexRules: this.regexRules,
            timestamp: Date.now()
        };
        
        try {
            localStorage.setItem('textProcessorData', JSON.stringify(data));
        } catch (error) {
            console.warn('无法保存到本地存储:', error);
        }
    }

    /**
     * 从本地存储恢复
     */
    restoreFromLocalStorage() {
        try {
            const data = localStorage.getItem('textProcessorData');
            if (data) {
                const parsed = JSON.parse(data);
                const now = Date.now();
                const oneDay = 24 * 60 * 60 * 1000;
                
                // 只恢复24小时内的数据
                if (now - parsed.timestamp < oneDay) {
                    if (parsed.inputTexts) {
                        parsed.inputTexts.forEach((text, index) => {
                            if (this.inputWindows[index]) {
                                this.inputWindows[index].element.value = text;
                            }
                        });
                    }
                    
                    if (parsed.regexRules) {
                        this.regexRules = parsed.regexRules;
                        this.updateRegexRulesList();
                    }
                    
                    this.updateCharCount();
                    this.updateRegexRulesCharCount();
                }
            }
        } catch (error) {
            console.warn('无法从本地存储恢复:', error);
        }
    }

    /**
     * 显示键盘快捷键帮助
     */
    showKeyboardShortcutsHelp() {
        const helpText = `
            <div class="keyboard-shortcuts-help" style="
                position: fixed;
                bottom: 20px;
                left: 20px;
                background: var(--surface-color);
                padding: 16px;
                border-radius: var(--border-radius-sm);
                box-shadow: var(--shadow-lg);
                border: 1px solid var(--border-light);
                font-size: 0.85rem;
                color: var(--text-secondary);
                z-index: 999;
                max-width: 300px;
                opacity: 0.8;
                transition: opacity 0.3s ease;
            ">
                <strong>键盘快捷键:</strong><br>
                Ctrl+Enter: 处理文本<br>
                Ctrl+Shift+C: 清空所有<br>
                Ctrl+Shift+R: 正则处理<br>
                Ctrl+Shift+T: 翻译<br>
                Ctrl+Shift+1-4: 切换选项卡
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', helpText);
        
        // 点击隐藏帮助
        const helpElement = document.querySelector('.keyboard-shortcuts-help');
        helpElement.addEventListener('click', () => {
            helpElement.style.opacity = '0';
            setTimeout(() => helpElement.remove(), 300);
        });
        
        // 5秒后自动隐藏
        setTimeout(() => {
            if (helpElement) {
                helpElement.style.opacity = '0';
                setTimeout(() => helpElement.remove(), 300);
            }
        }, 5000);
    }

    /**
     * 设置自动保存功能
     */
    setupAutoSave() {
        let autoSaveTimer;
        
        this.inputWindows.forEach(window => {
            window.element.addEventListener('input', () => {
                clearTimeout(autoSaveTimer);
                autoSaveTimer = setTimeout(() => {
                    this.saveToLocalStorage();
                }, 2000); // 2秒后自动保存
            });
        });
    }

    /**
     * 保存到本地存储
     */
    saveToLocalStorage() {
        const data = {
            inputTexts: this.inputWindows.map(w => w.element.value),
            regexRules: this.regexRules,
            timestamp: Date.now()
        };
        
        try {
            localStorage.setItem('textProcessorData', JSON.stringify(data));
        } catch (error) {
            console.warn('无法保存到本地存储:', error);
        }
    }

    /**
     * 从本地存储恢复
     */
    restoreFromLocalStorage() {
        try {
            const data = localStorage.getItem('textProcessorData');
            if (data) {
                const parsed = JSON.parse(data);
                const now = Date.now();
                const oneDay = 24 * 60 * 60 * 1000;
                
                // 只恢复24小时内的数据
                if (now - parsed.timestamp < oneDay) {
                    if (parsed.inputTexts) {
                        parsed.inputTexts.forEach((text, index) => {
                            if (this.inputWindows[index]) {
                                this.inputWindows[index].element.value = text;
                            }
                        });
                    }
                    
                    if (parsed.regexRules) {
                        this.regexRules = parsed.regexRules;
                        this.updateRegexRulesList();
                    }
                    
                    this.updateCharCount();
                    this.updateRegexRulesCharCount();
                }
            }
        } catch (error) {
            console.warn('无法从本地存储恢复:', error);
        }
    }

    /**
     * 增强的成功提示
     */
    showEnhancedSuccess(message, duration = 3000) {
        const toast = document.getElementById('successToast');
        const messageSpan = document.getElementById('successMessage');
        
        // 添加图标和动画
        messageSpan.innerHTML = `
            <i class="fas fa-check-circle" style="margin-right: 8px; animation: scaleIn 0.3s ease;"></i>
            ${message}
        `;
        
        this.showToast(toast);
        
        // 自动隐藏
        setTimeout(() => {
            this.hideToast(toast);
        }, duration);
    }

    /**
     * 增强的错误提示
     */
    showEnhancedError(message, duration = 4000) {
        const toast = document.getElementById('errorToast');
        const messageSpan = document.getElementById('errorMessage');
        
        // 添加图标和动画
        messageSpan.innerHTML = `
            <i class="fas fa-exclamation-triangle" style="margin-right: 8px; animation: scaleIn 0.3s ease;"></i>
            ${message}
        `;
        
        this.showToast(toast);
        
        // 自动隐藏
        setTimeout(() => {
            this.hideToast(toast);
        }, duration);
    }

    /**
     * 增强的错误提示
     */
    showEnhancedError(message, duration = 4000) {
        const toast = document.getElementById('errorToast');
        const messageSpan = document.getElementById('errorMessage');
        
        // 添加图标和动画
        messageSpan.innerHTML = `
            <i class="fas fa-exclamation-triangle" style="margin-right: 8px; animation: scaleIn 0.3s ease;"></i>
            ${message}
        `;
        
        this.showToast(toast);
        
        // 自动隐藏
        setTimeout(() => {
            this.hideToast(toast);
        }, duration);
    }
}

// 当DOM加载完成后初始化应用程序
document.addEventListener('DOMContentLoaded', () => {
    window.app = new TextProcessorApp();
    
    // 添加测试函数到控制台
    window.testCopyFunction = () => {
        console.log('Testing copy function...');
        const copyBtn = document.querySelector('.copy-btn');
        if (copyBtn) {
            console.log('Found copy button:', copyBtn);
            copyBtn.click();
        } else {
            console.log('No copy button found');
        }
    };
    
    console.log('TextProcessorApp initialized. Use testCopyFunction() to test copy functionality.');
});

// 导出类以供测试使用
if (typeof module !== 'undefined' && module.exports) {
    module.exports = TextProcessorApp;
} 