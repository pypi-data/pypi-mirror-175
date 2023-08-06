"use strict";
(self["webpackChunk_jupyterlab_benchmarks_ui_profiler"] = self["webpackChunk_jupyterlab_benchmarks_ui_profiler"] || []).push([["lib_index_js"],{

/***/ "./lib/benchmark.js":
/*!**************************!*\
  !*** ./lib/benchmark.js ***!
  \**************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "benchmark": () => (/* binding */ benchmark),
/* harmony export */   "profile": () => (/* binding */ profile)
/* harmony export */ });
/* harmony import */ var _statistics__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./statistics */ "./lib/statistics.js");

async function profile(scenario, options, mode, afterMicroStep, n = 3, inSuite = false) {
    if (!inSuite && scenario.setupSuite) {
        await scenario.setupSuite();
    }
    if (typeof window.Profiler === 'undefined') {
        throw new Error('Self-profiling is not available');
    }
    const traces = [];
    const errors = [];
    let profiler;
    if (mode === 'micro') {
        for (let i = 0; i < n; i++) {
            if (scenario.setup) {
                await scenario.setup();
            }
            profiler = new window.Profiler(options);
            try {
                await scenario.run();
            }
            catch (e) {
                console.error('Benchmark failed in scenario', scenario, e);
                errors.push(e);
            }
            traces.push(await profiler.stop());
            if (scenario.cleanup) {
                await scenario.cleanup();
            }
            afterMicroStep(i);
        }
    }
    else {
        profiler = new window.Profiler(options);
        for (let i = 0; i < n; i++) {
            if (scenario.setup) {
                await scenario.setup();
            }
            try {
                await scenario.run();
            }
            catch (e) {
                console.error('Benchmark failed in scenario', scenario, e);
                errors.push(e);
            }
            if (scenario.cleanup) {
                await scenario.cleanup();
            }
        }
        traces.push(await profiler.stop());
    }
    if (!inSuite && scenario.cleanupSuite) {
        await scenario.cleanupSuite();
    }
    return {
        traces,
        errors,
        samplingInterval: profiler.sampleInterval,
        averageSampleInterval: _statistics__WEBPACK_IMPORTED_MODULE_0__.Statistic.mean(traces
            .map(trace => {
            let previous = trace.samples[0].timestamp;
            const intervals = [];
            for (const sample of trace.samples.slice(1)) {
                intervals.push(sample.timestamp - previous);
                previous = sample.timestamp;
            }
            return intervals;
        })
            .flat())
    };
}
async function benchmark(scenario, n = 3, inSuite = false) {
    if (!inSuite && scenario.setupSuite) {
        await scenario.setupSuite();
    }
    const times = [];
    const errors = [];
    for (let i = 0; i < n; i++) {
        if (scenario.setup) {
            await scenario.setup();
        }
        const start = performance.now();
        try {
            await scenario.run();
            times.push(performance.now() - start);
        }
        catch (e) {
            console.error('Benchmark failed in scenario', scenario, e);
            errors.push(e);
        }
        if (scenario.cleanup) {
            await scenario.cleanup();
        }
    }
    if (!inSuite && scenario.cleanupSuite) {
        await scenario.cleanupSuite();
    }
    return {
        times,
        errors
    };
}


/***/ }),

/***/ "./lib/css.js":
/*!********************!*\
  !*** ./lib/css.js ***!
  \********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "collectRules": () => (/* binding */ collectRules),
/* harmony export */   "extractSourceMap": () => (/* binding */ extractSourceMap)
/* harmony export */ });
/**
 * Extract CSS source map from CSS text content.
 *
 * Note: if URL is embedded, fetch method will be used to retrive the JSON contents.
 */
async function extractSourceMap(cssContent) {
    if (!cssContent) {
        return null;
    }
    const matches = cssContent.matchAll(new RegExp('# sourceMappingURL=(.*)\\s*\\*/', 'g'));
    if (!matches) {
        return null;
    }
    let url = '';
    for (const match of matches) {
        const parts = match[1].split('data:application/json;base64,');
        if (parts.length > 1) {
            return JSON.parse(atob(parts[1]));
        }
        else {
            url = match[1];
        }
    }
    if (url === '') {
        return null;
    }
    const response = await fetch(url);
    return response.json();
}
async function collectRules(styles, options) {
    let j = 0;
    const allRules = [];
    for (const style of styles) {
        const sheet = style.sheet;
        if (!sheet) {
            continue;
        }
        const cssMap = await extractSourceMap(style.textContent);
        const sourceName = cssMap ? cssMap.sources[0] : null;
        j++;
        const rules = sheet.rules;
        for (let i = 0; i < rules.length; i++) {
            const rule = rules[i];
            if (!(rule instanceof CSSStyleRule)) {
                continue;
            }
            if (options.skipPattern &&
                rule.selectorText.match(options.skipPattern) != null) {
                continue;
            }
            allRules.push({
                rule: rule,
                selector: rule.selectorText,
                sheet: sheet,
                source: sourceName,
                ruleIndex: i,
                stylesheetIndex: j
            });
        }
    }
    return allRules;
}


/***/ }),

/***/ "./lib/dramaturg.js":
/*!**************************!*\
  !*** ./lib/dramaturg.js ***!
  \**************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ElementHandle": () => (/* binding */ ElementHandle),
/* harmony export */   "layoutReady": () => (/* binding */ layoutReady),
/* harmony export */   "page": () => (/* binding */ page),
/* harmony export */   "waitForScrollEnd": () => (/* binding */ waitForScrollEnd)
/* harmony export */ });
/* harmony import */ var _lumino_keyboard__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/keyboard */ "../../node_modules/@lumino/keyboard/dist/index.es6.js");
/**
 * Dramaturg implements a subset of Playwright-like API for native web testing.
 */

function waitElementVisible(selector, within, visible = true) {
    return new Promise((resolve, reject) => {
        const node = (within || document).querySelector(selector);
        if (!node) {
            return reject(`No element matching ${selector} is attached`);
        }
        const conditionSatisfied = (data) => {
            return visible
                ? data.width !== 0 && data.height !== 0
                : data.width === 0 || data.height === 0;
        };
        const observer = new ResizeObserver(entries => {
            for (const entry of entries) {
                const node = entry.target;
                const matches = conditionSatisfied(entry.contentRect);
                if (matches && node instanceof HTMLElement && node.matches(selector)) {
                    observer.disconnect();
                    resolve(node);
                }
            }
        });
        observer.observe(node);
        if (conditionSatisfied(node.getBoundingClientRect())) {
            observer.disconnect();
            return resolve(node);
        }
    });
}
async function waitElementHidden(selector, within) {
    await waitElementVisible(selector, within, false);
    return null;
}
function waitForElement(selector, within) {
    return new Promise(resolve => {
        const observer = new MutationObserver(mutations => {
            for (const mutation of mutations) {
                for (const node of mutation.addedNodes) {
                    if (!(node instanceof HTMLElement)) {
                        continue;
                    }
                    if (node.matches(selector)) {
                        resolve(node);
                        observer.disconnect();
                    }
                    const childNode = node.querySelector(selector);
                    if (childNode) {
                        resolve(childNode);
                        observer.disconnect();
                    }
                }
            }
        });
        observer.observe(within || document.documentElement, {
            childList: true,
            subtree: true,
            attributes: selector.includes('[') || selector.includes(':')
        });
        const node = document.querySelector(selector);
        if (node) {
            observer.disconnect();
            return resolve(node);
        }
    });
}
function waitNoElement(selector, within) {
    return new Promise(resolve => {
        if (!document.querySelector(selector)) {
            return resolve(null);
        }
        const observer = new MutationObserver(mutations => {
            for (const mutation of mutations) {
                for (const node of mutation.removedNodes) {
                    if (node instanceof HTMLElement && node.matches(selector)) {
                        resolve(null);
                        observer.disconnect();
                    }
                }
            }
        });
        observer.observe(within || document.documentElement, {
            childList: true,
            subtree: true,
            attributes: selector.includes('[') || selector.includes(':')
        });
    });
}
async function waitForScrollEnd(element, requiredRestTime) {
    return new Promise(resolve => {
        let lastScrollTop = element.scrollTop;
        let lastScrollLeft = element.scrollLeft;
        const intervalHandle = setInterval(() => {
            if (element.scrollTop === lastScrollTop &&
                element.scrollLeft === lastScrollLeft) {
                clearInterval(intervalHandle);
                return resolve();
            }
            lastScrollTop = element.scrollTop;
            lastScrollLeft = element.scrollLeft;
        }, requiredRestTime);
    });
}
function layoutReady() {
    return new Promise(resolve => {
        return requestAnimationFrame(() => {
            resolve();
        });
    });
}
class ElementHandle {
    constructor(element) {
        this.element = element;
        // no-op
    }
    $(selector) {
        return $(selector, this.element);
    }
    click() {
        return click(this.element);
    }
    async focus() {
        return this.element.focus();
    }
    press(key, options = { delay: 0 }) {
        return press(key, options, this.element);
    }
    type(text, options = { delay: 0 }) {
        return type(text, options, this.element);
    }
    waitForSelector(selector, options) {
        return waitForSelector(selector, {
            ...options,
            within: this.element
        });
    }
}
function waitForSelector(selector, options = { state: 'visible' }) {
    let promise;
    switch (options.state) {
        case 'attached':
            promise = waitForElement(selector, options.within).then(element => new ElementHandle(element));
            break;
        case 'detached':
            promise = waitNoElement(selector, options.within);
            break;
        case 'visible':
            promise = waitElementVisible(selector, options.within).then(element => new ElementHandle(element));
            break;
        case 'hidden':
            promise = waitElementHidden(selector, options.within);
            break;
    }
    const timeout = options.timeout || 5 * 1000;
    return Promise.race([
        promise,
        new Promise((_, reject) => {
            setTimeout(() => reject(`Selector ${selector} not found in ${options.state} state in ${timeout / 1000}s`), timeout);
        })
    ]);
}
const keyboardLayout = (0,_lumino_keyboard__WEBPACK_IMPORTED_MODULE_0__.getKeyboardLayout)();
// TODO: should lumino expose the codes?
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-ignore
const codeToKey = keyboardLayout._codes;
const keyToCode = Object.fromEntries(Object.entries(codeToKey).map(a => a.reverse()));
async function press(key, options = { delay: 0 }, element = null) {
    if (!element) {
        element = document.activeElement || document.body;
    }
    const keys = key.split('+');
    const modifiers = keys.filter(k => keyboardLayout.isModifierKey(k));
    const target = keys.filter(k => !keyboardLayout.isModifierKey(k))[0];
    const eventData = {
        keyCode: keyToCode[target],
        shiftKey: modifiers.includes('Shift'),
        ctrlKey: modifiers.includes('Ctrl'),
        metaKey: modifiers.includes('Meta'),
        key: target
    };
    element.dispatchEvent(new KeyboardEvent('keydown', eventData));
    element.dispatchEvent(new KeyboardEvent('keypress', eventData));
    if (options.delay) {
        await new Promise(resolve => setTimeout(resolve, options.delay));
    }
    element.dispatchEvent(new KeyboardEvent('keyup', eventData));
}
async function type(text, options = { delay: 0 }, element = null) {
    for (const char of text) {
        await press(char, options, element);
    }
}
async function click(element) {
    const rect = element.getBoundingClientRect();
    const initDict = {
        clientX: rect.x + rect.width / 2,
        clientY: rect.x + rect.height / 2
    };
    element.dispatchEvent(new MouseEvent('mousedown', initDict));
    element.dispatchEvent(new MouseEvent('mouseup', initDict));
    element.click();
}
async function $(selector, element) {
    const matched = element
        ? element.querySelector(selector)
        : document.querySelector(selector);
    if (!matched) {
        return null;
    }
    return new ElementHandle(matched);
}
const page = {
    waitForSelector,
    press,
    $: $,
    type: async (selector, text, options = { delay: 0 }) => {
        const element = await waitForSelector(selector, { state: 'visible' });
        return element.type(text, options);
    },
    click: async (selector) => {
        await waitForSelector(selector, { state: 'attached' });
        const element = await waitForSelector(selector, { state: 'visible' });
        click(element.element);
    },
    focus: async (selector) => {
        const element = await waitForSelector(selector, { state: 'visible' });
        element.element.focus();
    },
    mouse: {
        wheel: async (deltaX, deltaY) => {
            document.dispatchEvent(new WheelEvent('wheel', {
                deltaX,
                deltaY
            }));
        }
    }
};


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/filebrowser */ "webpack/sharing/consume/default/@jupyterlab/filebrowser");
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/launcher */ "webpack/sharing/consume/default/@jupyterlab/launcher");
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _ui__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./ui */ "./lib/ui.js");
/* harmony import */ var _styleBenchmarks__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./styleBenchmarks */ "./lib/styleBenchmarks.js");
/* harmony import */ var _jsBenchmarks__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./jsBenchmarks */ "./lib/jsBenchmarks.js");
/* harmony import */ var _scenarios__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./scenarios */ "./lib/scenarios.js");











var CommandIDs;
(function (CommandIDs) {
    // export const findUnusedStyles = 'ui-profiler:find-unused-styles';
    CommandIDs.openProfiler = 'ui-profiler:open';
})(CommandIDs || (CommandIDs = {}));
/**
 * Initialization data for the @jupyterlab-benchmarks/ui-profiler extension.
 */
const plugin = {
    id: '@jupyterlab-benchmarks/ui-profiler:plugin',
    autoStart: true,
    requires: [_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_3__.IFileBrowserFactory],
    optional: [_jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_4__.ILauncher, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer],
    activate: (app, factory, launcher, restorer) => {
        const options = {
            benchmarks: [
                _styleBenchmarks__WEBPACK_IMPORTED_MODULE_7__.styleSheetsBenchmark,
                _styleBenchmarks__WEBPACK_IMPORTED_MODULE_7__.styleRuleBenchmark,
                _styleBenchmarks__WEBPACK_IMPORTED_MODULE_7__.styleRuleGroupBenchmark,
                _styleBenchmarks__WEBPACK_IMPORTED_MODULE_7__.styleRuleUsageBenchmark,
                _jsBenchmarks__WEBPACK_IMPORTED_MODULE_8__.selfProfileBenchmark
            ],
            scenarios: [
                new _scenarios__WEBPACK_IMPORTED_MODULE_9__.MenuOpenScenario(app),
                new _scenarios__WEBPACK_IMPORTED_MODULE_9__.MenuSwitchScenario(app),
                new _scenarios__WEBPACK_IMPORTED_MODULE_9__.SwitchTabScenario(app),
                new _scenarios__WEBPACK_IMPORTED_MODULE_9__.SwitchTabFocusScenario(app),
                new _scenarios__WEBPACK_IMPORTED_MODULE_9__.SidebarOpenScenario(app),
                new _scenarios__WEBPACK_IMPORTED_MODULE_9__.CompleterScenario(app),
                new _scenarios__WEBPACK_IMPORTED_MODULE_9__.ScrollScenario(app)
            ],
            translator: _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_5__.nullTranslator,
            upload: (file) => {
                // this.manager = new ServiceManager();
                // this.manager.contents.uploadFile - only exists in galata...
                // TODO: this is actually an upstream issue, services should offer upload method
                // rather than each place re-implmenting it
                return factory.defaultBrowser.model.upload(file);
            },
            getJupyterState: () => {
                const state = {
                    client: app.name,
                    version: app.version,
                    devMode: (_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.PageConfig.getOption('devMode') || '').toLowerCase() === 'true',
                    mode: _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.PageConfig.getOption('mode')
                };
                return state;
            },
            resultLocation: '/ui-profiler-results/'
        };
        const content = new _ui__WEBPACK_IMPORTED_MODULE_10__.UIProfiler(options);
        const widget = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.MainAreaWidget({ content });
        widget.id = 'ui-profiler-centre';
        widget.title.label = 'UI Profiler';
        widget.title.closable = true;
        widget.title.icon = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_6__.offlineBoltIcon;
        const tracker = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.WidgetTracker({
            namespace: 'ui-profiler'
        });
        app.commands.addCommand(CommandIDs.openProfiler, {
            execute: async () => {
                if (!widget.isAttached) {
                    // Attach the widget to the main work area if it's not there
                    app.shell.add(widget, 'main');
                }
                // Activate the widget
                app.shell.activateById(widget.id);
                tracker.add(widget);
            },
            label: 'UI Profiler',
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_6__.offlineBoltIcon,
            caption: 'Open JupyterLab UI Profiler'
        });
        // TODO this does work and allows to avoid defining a custom tracker
        // but there is a bug in restoration - the icon class on tab bar does
        // not get properly restored.
        // if (restorer) {
        // restorer.add(widget, 'test')
        // }
        if (restorer) {
            // Handle state restoration.
            void restorer.restore(tracker, {
                command: CommandIDs.openProfiler,
                name: widget => widget.title.label
            });
        }
        if (launcher) {
            launcher.add({
                command: CommandIDs.openProfiler,
                category: 'Other',
                rank: 1
            });
        }
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ }),

/***/ "./lib/jsBenchmarks.js":
/*!*****************************!*\
  !*** ./lib/jsBenchmarks.js ***!
  \*****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "extractTimes": () => (/* binding */ extractTimes),
/* harmony export */   "iterateFrames": () => (/* binding */ iterateFrames),
/* harmony export */   "selfProfileBenchmark": () => (/* binding */ selfProfileBenchmark)
/* harmony export */ });
/* harmony import */ var _benchmark__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./benchmark */ "./lib/benchmark.js");
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./utils */ "./lib/utils.js");
/* harmony import */ var _dramaturg__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./dramaturg */ "./lib/dramaturg.js");
/* harmony import */ var _ui__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./ui */ "./lib/ui.js");
/* harmony import */ var _schema_benchmark_profile_json__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./schema/benchmark-profile.json */ "./lib/schema/benchmark-profile.json");





function* iterateFrames(trace) {
    let runningFrames = new Map();
    for (const sample of trace.samples) {
        const now = sample.timestamp;
        // when undefined, the stack was empty -> mark all currently running functions as done
        let completedFrames;
        const previouslyRunningFrames = [...runningFrames.keys()];
        const activeFrames = new Map();
        if (typeof sample.stackId === 'undefined') {
            completedFrames = [...previouslyRunningFrames];
        }
        else {
            let stack = trace.stacks[sample.stackId];
            let staskSize = 0;
            while (stack) {
                stack =
                    typeof stack.parentId !== 'undefined'
                        ? trace.stacks[stack.parentId]
                        : null;
                staskSize++;
            }
            let depth = 0;
            stack = trace.stacks[sample.stackId];
            while (stack) {
                const inverseDepth = staskSize - depth;
                const blockId = stack.frameId + '-' + inverseDepth;
                activeFrames.set(blockId, runningFrames.get(blockId) ?? {
                    start: now,
                    stackDepth: inverseDepth,
                    frameId: stack.frameId
                });
                stack =
                    typeof stack.parentId !== 'undefined'
                        ? trace.stacks[stack.parentId]
                        : null;
                depth++;
            }
            completedFrames = [...previouslyRunningFrames].filter(a => !activeFrames.has(a));
        }
        for (const frameId of completedFrames) {
            const state = runningFrames.get(frameId);
            const time = now - state.start;
            yield {
                duration: time,
                ...state
            };
            runningFrames.delete(frameId);
        }
        runningFrames = activeFrames;
    }
}
function extractTimes(trace) {
    const totalFrameTime = new Map();
    for (const frameData of iterateFrames(trace)) {
        totalFrameTime.set(frameData.frameId, totalFrameTime.get(frameData.frameId) || 0 + frameData.duration);
    }
    return [...totalFrameTime.entries()].map(([frameId, time]) => {
        const frame = trace.frames[frameId];
        return {
            resource: typeof frame.resourceId !== 'undefined'
                ? trace.resources[frame.resourceId]
                : undefined,
            name: frame.name,
            column: frame.column,
            line: frame.line,
            time
        };
    });
}
const selfProfileBenchmark = {
    id: 'self-profile',
    name: 'Profile JavaScript',
    configSchema: _schema_benchmark_profile_json__WEBPACK_IMPORTED_MODULE_0__,
    run: async (scenario, options, progress) => {
        const n = options.repeats || 3;
        const start = Date.now();
        if (scenario.setupSuite) {
            await scenario.setupSuite();
        }
        await (0,_dramaturg__WEBPACK_IMPORTED_MODULE_1__.layoutReady)();
        const result = await (0,_benchmark__WEBPACK_IMPORTED_MODULE_2__.profile)(scenario, {
            maxBufferSize: options.maxBufferSize,
            sampleInterval: options.sampleInterval
        }, options.scale, i => progress?.emit({ percentage: (100 * (i + 1)) / n }), n, true);
        await (0,_dramaturg__WEBPACK_IMPORTED_MODULE_1__.layoutReady)();
        if (scenario.cleanupSuite) {
            await scenario.cleanupSuite();
        }
        progress?.emit({ percentage: 100 });
        return {
            results: [result],
            tags: (0,_utils__WEBPACK_IMPORTED_MODULE_3__.reportTagCounts)(),
            totalTime: Date.now() - start,
            type: 'profile'
        };
    },
    isAvailable: () => typeof window.Profiler !== 'undefined',
    render: _ui__WEBPACK_IMPORTED_MODULE_4__.renderProfile
};


/***/ }),

/***/ "./lib/lumino.js":
/*!***********************!*\
  !*** ./lib/lumino.js ***!
  \***********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "LuminoWidget": () => (/* binding */ LuminoWidget)
/* harmony export */ });
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);


const LuminoWidget = (props) => {
    const ref = react__WEBPACK_IMPORTED_MODULE_1___default().useRef(null);
    react__WEBPACK_IMPORTED_MODULE_1___default().useEffect(() => {
        const widget = props.widget;
        _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget.attach(widget, ref.current);
        function updateSize() {
            props.widget.fit();
        }
        const observer = new ResizeObserver(entries => {
            updateSize();
        });
        observer.observe(ref.current);
        return () => {
            _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget.detach(widget);
            observer.disconnect();
        };
    }, [props.widget]);
    return react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { className: "up-LuminoWidgetWrapper", ref: ref });
};


/***/ }),

/***/ "./lib/scenarios.js":
/*!**************************!*\
  !*** ./lib/scenarios.js ***!
  \**************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "CompleterScenario": () => (/* binding */ CompleterScenario),
/* harmony export */   "MenuOpenScenario": () => (/* binding */ MenuOpenScenario),
/* harmony export */   "MenuSwitchScenario": () => (/* binding */ MenuSwitchScenario),
/* harmony export */   "ScrollScenario": () => (/* binding */ ScrollScenario),
/* harmony export */   "SidebarOpenScenario": () => (/* binding */ SidebarOpenScenario),
/* harmony export */   "SwitchTabFocusScenario": () => (/* binding */ SwitchTabFocusScenario),
/* harmony export */   "SwitchTabScenario": () => (/* binding */ SwitchTabScenario),
/* harmony export */   "insertText": () => (/* binding */ insertText)
/* harmony export */ });
/* harmony import */ var _dramaturg__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./dramaturg */ "./lib/dramaturg.js");
/* harmony import */ var _schema_scenario_base_json__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./schema/scenario-base.json */ "./lib/schema/scenario-base.json");
/* harmony import */ var _schema_scenario_menu_open_json__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./schema/scenario-menu-open.json */ "./lib/schema/scenario-menu-open.json");
/* harmony import */ var _schema_scenario_tabs_json__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./schema/scenario-tabs.json */ "./lib/schema/scenario-tabs.json");
/* harmony import */ var _schema_scenario_completer_json__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./schema/scenario-completer.json */ "./lib/schema/scenario-completer.json");
/* harmony import */ var _schema_scenario_sidebars_json__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./schema/scenario-sidebars.json */ "./lib/schema/scenario-sidebars.json");
/* harmony import */ var _schema_scenario_scroll_json__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./schema/scenario-scroll.json */ "./lib/schema/scenario-scroll.json");







async function switchMainMenu(jupyterApp) {
    for (const menu of ['edit', 'view', 'run', 'kernel', 'settings', 'help']) {
        await openMainMenu(jupyterApp, menu);
    }
}
async function openMainMenu(jupyterApp, menu = 'file') {
    await jupyterApp.commands.execute(`${menu}menu:open`);
    await _dramaturg__WEBPACK_IMPORTED_MODULE_0__.page.waitForSelector(`#jp-mainmenu-${menu}`, { state: 'attached' });
    await (0,_dramaturg__WEBPACK_IMPORTED_MODULE_0__.layoutReady)();
}
async function cleanupMenu() {
    // ensure menu is open
    await _dramaturg__WEBPACK_IMPORTED_MODULE_0__.page.waitForSelector('.lm-Menu', { state: 'attached' });
    await _dramaturg__WEBPACK_IMPORTED_MODULE_0__.page.press('Escape');
    await _dramaturg__WEBPACK_IMPORTED_MODULE_0__.page.waitForSelector('.lm-Menu', { state: 'detached' });
    await (0,_dramaturg__WEBPACK_IMPORTED_MODULE_0__.layoutReady)();
}
class MenuSwitchScenario {
    constructor(jupyterApp) {
        this.jupyterApp = jupyterApp;
        this.cleanup = cleanupMenu;
        this.id = 'menuSwitch';
        this.name = 'Switch Menu';
        this.configSchema = _schema_scenario_base_json__WEBPACK_IMPORTED_MODULE_1__;
        // no-op
    }
    setOptions(options) {
        // no-op
    }
    async setup() {
        return openMainMenu(this.jupyterApp);
    }
    async run() {
        return switchMainMenu(this.jupyterApp);
    }
}
class MenuOpenScenario {
    constructor(jupyterApp) {
        this.jupyterApp = jupyterApp;
        this.cleanup = cleanupMenu;
        this.id = 'menuOpen';
        this.name = 'Open Menu';
        this.configSchema = _schema_scenario_menu_open_json__WEBPACK_IMPORTED_MODULE_2__;
        this._menu = 'file';
    }
    setOptions(options) {
        this._menu = options.menu;
    }
    async run() {
        return openMainMenu(this.jupyterApp, this._menu);
    }
}
async function closeSidebars(jupyterApp) {
    for (const side of ['left', 'right']) {
        const panel = document.querySelector(`#jp-${side}-stack`);
        if (panel && !panel.classList.contains('lm-mod-hidden')) {
            await jupyterApp.commands.execute(`application:toggle-${side}-area`);
            await _dramaturg__WEBPACK_IMPORTED_MODULE_0__.page.waitForSelector(`#jp-${side}-stack`, { state: 'hidden' });
            await (0,_dramaturg__WEBPACK_IMPORTED_MODULE_0__.layoutReady)();
        }
    }
}
class SidebarOpenScenario {
    constructor(jupyterApp) {
        this.jupyterApp = jupyterApp;
        // TOOD restore initially open panel in cleanup?
        this.id = 'sidebarOpen';
        this.name = 'Open Sidebar';
        this.configSchema = _schema_scenario_sidebars_json__WEBPACK_IMPORTED_MODULE_3__;
        this._sidebars = ['filebrowser'];
        // no-op
    }
    setOptions(options) {
        this._sidebars = options.sidebars;
    }
    async setup() {
        return closeSidebars(this.jupyterApp);
    }
    async run() {
        // TODO make this configurable (with this list as default)
        for (const sidebar of this._sidebars) {
            // will be possible with commands in 4.0+ https://stackoverflow.com/a/74005349/6646912
            this.jupyterApp.shell.activateById(sidebar);
            await _dramaturg__WEBPACK_IMPORTED_MODULE_0__.page.waitForSelector(`#${CSS.escape(sidebar)}`, {
                state: 'visible'
            });
            await (0,_dramaturg__WEBPACK_IMPORTED_MODULE_0__.layoutReady)();
        }
    }
}
function insertText(jupyterApp, text) {
    return jupyterApp.commands.execute('apputils:run-first-enabled', {
        commands: [
            'notebook:replace-selection',
            'console:replace-selection',
            'fileeditor:replace-selection'
        ],
        args: {
            text: text
        }
    });
}
class SingleEditorScenario {
    constructor(jupyterApp) {
        this.jupyterApp = jupyterApp;
        this.editor = null;
        this.path = null;
        this.options = null;
        this.useNotebook = true;
        this.widget = null;
        // no-op
    }
    setOptions(options) {
        this.options = options;
        this.useNotebook = this.options.editor === 'Notebook';
    }
    async setupSuite() {
        if (!this.options) {
            throw new Error('Options not set for scenario.');
        }
        if (!this.options.path || this.options.path.length === 0) {
            const model = await this.jupyterApp.commands.execute('docmanager:new-untitled', this.useNotebook
                ? { path: '', type: 'notebook' }
                : {
                    path: '',
                    type: 'file',
                    ext: 'py'
                });
            this.path = model.path;
        }
        else {
            this.path = this.options.path;
        }
        const widget = await this.jupyterApp.commands.execute('docmanager:open', {
            path: this.path,
            factory: this.useNotebook ? 'Notebook' : 'Editor'
        });
        this.widget = widget;
        this.jupyterApp.shell.add(this.widget, 'main', { mode: 'split-right' });
        await activateTabWidget(this.jupyterApp, widget);
        await (0,_dramaturg__WEBPACK_IMPORTED_MODULE_0__.layoutReady)();
        if (this.useNotebook) {
            // Accept default kernel in kernel selection dialog
            await _dramaturg__WEBPACK_IMPORTED_MODULE_0__.page.click('.jp-Dialog-button.jp-mod-accept');
        }
        const handle = new _dramaturg__WEBPACK_IMPORTED_MODULE_0__.ElementHandle(this.widget.node);
        await handle.waitForSelector('.jp-Editor', { state: 'attached' });
        await (0,_dramaturg__WEBPACK_IMPORTED_MODULE_0__.layoutReady)();
        await handle.waitForSelector('.jp-Editor', { state: 'visible' });
        await (0,_dramaturg__WEBPACK_IMPORTED_MODULE_0__.layoutReady)();
        this.editor = this.useNotebook
            ? this.widget.node.querySelector('.jp-Notebook')
            : this.widget.node.querySelector('.jp-FileEditorCodeWrapper');
    }
    async cleanupSuite() {
        if (this.widget) {
            // TODO: reset cell/editor contents if anything was added?
            await this.jupyterApp.commands.execute('docmanager:save');
            this.widget.close();
        }
        // TODO: remove file; also the file should be in a temp dir
    }
}
class CompleterScenario extends SingleEditorScenario {
    constructor() {
        super(...arguments);
        this.id = 'completer';
        this.name = 'Completer';
        this.configSchema = _schema_scenario_completer_json__WEBPACK_IMPORTED_MODULE_4__;
    }
    async setupSuite() {
        await super.setupSuite();
        if (!this.widget || !this.options) {
            throw new Error('Parent setup failure');
        }
        let text;
        if (typeof this.options.setup?.setupText !== 'undefined') {
            text = this.options.setup.setupText;
        }
        else {
            const tokens = [];
            for (let i = 0; i < this.options.setup.tokenCount; i++) {
                tokens.push(('t' + i).padEnd(this.options.setup.tokenSize, 'x') + ' = ' + i);
            }
            tokens.push('t');
            text = tokens.join('\n');
        }
        await insertText(this.jupyterApp, text);
        if (!this.useNotebook) {
            // Scroll down a little bit to avoid out of view bug
            this.editor.querySelector('.CodeMirror-scroll').scrollBy({
                top: 500,
                left: 0,
                behavior: 'smooth'
            });
        }
        // first run is flaky
        try {
            await this.run();
        }
        catch (e) {
            // no-op
        }
        await this.cleanup();
    }
    async run() {
        if (this.useNotebook) {
            // TODO enter a specific cell, not the first cell?
            const handle = new _dramaturg__WEBPACK_IMPORTED_MODULE_0__.ElementHandle(this.widget.node);
            const editor = await handle.$('.jp-Editor textarea');
            await editor.focus();
        }
        await (0,_dramaturg__WEBPACK_IMPORTED_MODULE_0__.layoutReady)();
        await _dramaturg__WEBPACK_IMPORTED_MODULE_0__.page.press('Tab');
        await (0,_dramaturg__WEBPACK_IMPORTED_MODULE_0__.layoutReady)();
        // Note: in JupyterLab 3.x all completers were retained in the attached state
        // (which may have had a performance benefit to some point, but later was just
        // cluttering the DOM) which makes finding the correct completer harder; we
        // need to query for a completer with programatically set styles (which are
        // things like position (top/left/width/height) which are only present in the
        // active completer
        await _dramaturg__WEBPACK_IMPORTED_MODULE_0__.page.waitForSelector('.jp-Completer[style]', { state: 'attached' });
        await _dramaturg__WEBPACK_IMPORTED_MODULE_0__.page.waitForSelector('.jp-Completer[style]', { state: 'visible' });
        await (0,_dramaturg__WEBPACK_IMPORTED_MODULE_0__.layoutReady)();
    }
    async cleanup() {
        await _dramaturg__WEBPACK_IMPORTED_MODULE_0__.page.press('Escape');
        await (0,_dramaturg__WEBPACK_IMPORTED_MODULE_0__.layoutReady)();
        await _dramaturg__WEBPACK_IMPORTED_MODULE_0__.page.waitForSelector('.jp-Completer[style]', { state: 'hidden' });
        await (0,_dramaturg__WEBPACK_IMPORTED_MODULE_0__.layoutReady)();
    }
}
async function activateTabWidget(jupyterApp, widget) {
    await jupyterApp.commands.execute('tabsmenu:activate-by-id', {
        id: widget.id
    });
    await (0,_dramaturg__WEBPACK_IMPORTED_MODULE_0__.layoutReady)();
    await _dramaturg__WEBPACK_IMPORTED_MODULE_0__.page.waitForSelector(`li.lm-mod-current[data-id="${widget.id}"]`, {
        state: 'attached'
    });
    await (0,_dramaturg__WEBPACK_IMPORTED_MODULE_0__.layoutReady)();
}
class ScrollScenario extends SingleEditorScenario {
    constructor() {
        super(...arguments);
        this.id = 'scroll';
        this.name = 'Scroll';
        this.configSchema = _schema_scenario_scroll_json__WEBPACK_IMPORTED_MODULE_5__;
    }
    async setupSuite() {
        await super.setupSuite();
        if (!this.widget || !this.options) {
            throw new Error('Parent setup failure');
        }
        const showEveryN = this.options.cells < 100 ? 20 : 50;
        for (let i = 0; i < this.options.cells; i++) {
            if (this.useNotebook) {
                await this.jupyterApp.commands.execute('notebook:insert-cell-below');
            }
            if (this.options.editorContent) {
                await insertText(this.jupyterApp, this.useNotebook
                    ? this.options.editorContent
                    : this.options.editorContent + '\n');
            }
            // just to show that the setup is progressing
            if (i < 5 || i % showEveryN === 0) {
                await (0,_dramaturg__WEBPACK_IMPORTED_MODULE_0__.layoutReady)();
            }
        }
        this.editor.scrollTop = 0;
        await (0,_dramaturg__WEBPACK_IMPORTED_MODULE_0__.layoutReady)();
    }
    async run() {
        if (!this.widget || !this.options) {
            throw new Error('Scrol scenario setup failure');
        }
        if (this.options.cellByCell && this.useNotebook) {
            for (let i = 0; i < this.options.cells; i++) {
                await this.jupyterApp.commands.execute('notebook:move-cursor-down');
                await (0,_dramaturg__WEBPACK_IMPORTED_MODULE_0__.layoutReady)();
            }
            await (0,_dramaturg__WEBPACK_IMPORTED_MODULE_0__.layoutReady)();
        }
        else {
            this.editor.scrollBy({
                top: this.options.scrollTop,
                left: 0,
                behavior: this.options.scrollBehavior
            });
            await (0,_dramaturg__WEBPACK_IMPORTED_MODULE_0__.waitForScrollEnd)(this.editor, 50);
            await (0,_dramaturg__WEBPACK_IMPORTED_MODULE_0__.layoutReady)();
        }
    }
    async cleanup() {
        if (!this.widget || !this.options) {
            throw new Error('Scrol scenario setup failure');
        }
        if (this.options.cellByCell && this.useNotebook) {
            for (let i = 0; i < this.options.cells; i++) {
                await this.jupyterApp.commands.execute('notebook:move-cursor-up');
            }
            await (0,_dramaturg__WEBPACK_IMPORTED_MODULE_0__.layoutReady)();
        }
        else {
            this.editor.scrollTop = 0;
            await (0,_dramaturg__WEBPACK_IMPORTED_MODULE_0__.layoutReady)();
        }
    }
}
class SwitchTabScenario {
    constructor(jupyterApp) {
        this.jupyterApp = jupyterApp;
        this.id = 'tabSwitch';
        this.name = 'Switch Tabs';
        this.split = 'first';
        this.configSchema = _schema_scenario_tabs_json__WEBPACK_IMPORTED_MODULE_6__;
        this._tabs = [];
        this._widgets = [];
        // no-op
    }
    setOptions(options) {
        const { tabs } = options;
        if (!tabs || !tabs.length) {
            throw new Error('At least one tab specification must be provided');
        }
        this._tabs = tabs;
        this._widgets = [];
    }
    async setupSuite() {
        this._widgets = [];
        for (const tab of this._tabs) {
            let widget;
            switch (tab.type) {
                case 'launcher':
                    widget = await this.jupyterApp.commands.execute('launcher:create');
                    break;
                case 'file':
                    widget = await this.jupyterApp.commands.execute('docmanager:open', {
                        path: tab.path
                    });
                    break;
                default:
                    throw Error('Unknown tab type');
            }
            await _dramaturg__WEBPACK_IMPORTED_MODULE_0__.page.waitForSelector('#' + widget.id, { state: 'attached' });
            if ((this.split === 'first' && this._widgets.length === 0) ||
                this.split === 'all') {
                this.jupyterApp.shell.add(widget, 'main', { mode: 'split-right' });
            }
            await activateTabWidget(this.jupyterApp, widget);
            this._widgets.push(widget);
        }
    }
    async cleanupSuite() {
        for (const widget of this._widgets) {
            widget.close();
            await _dramaturg__WEBPACK_IMPORTED_MODULE_0__.page.waitForSelector(`.lm-Widget[data-id="${widget.id}"]`, {
                state: 'detached'
            });
        }
    }
    async run() {
        if (!this._widgets.length) {
            throw new Error('Suite not set up');
        }
        for (const widget of this._widgets) {
            await activateTabWidget(this.jupyterApp, widget);
        }
    }
}
class SwitchTabFocusScenario extends SwitchTabScenario {
    constructor() {
        super(...arguments);
        this.id = 'tabSwitchFocus';
        this.name = 'Switch Tab Focus';
        this.split = 'all';
    }
}


/***/ }),

/***/ "./lib/statistics.js":
/*!***************************!*\
  !*** ./lib/statistics.js ***!
  \***************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "Statistic": () => (/* binding */ Statistic)
/* harmony export */ });
var Statistic;
(function (Statistic) {
    function min(numbers) {
        return Math.min(...numbers);
    }
    Statistic.min = min;
    function mean(numbers) {
        if (numbers.length === 0) {
            return NaN;
        }
        return sum(numbers) / numbers.length;
    }
    Statistic.mean = mean;
    function interQuartileMean(numbers) {
        numbers = numbers.sort((a, b) => a - b);
        if (numbers.length % 4 === 0) {
            const q = Math.floor(numbers.length / 4);
            return mean(numbers.slice(q, numbers.length - q));
        }
        else {
            const iqrSpan = (numbers.length / 4) * 2;
            const q = Math.floor(numbers.length / 4);
            const toConsider = numbers.slice(q, numbers.length - q);
            const full = toConsider.length - 2;
            const fraction = (iqrSpan - full) / 2;
            const fullContrib = toConsider.slice(1, toConsider.length - 1);
            const fractionalPart = [
                toConsider[0] * fraction,
                toConsider[toConsider.length - 1] * fraction
            ];
            return sum([...fullContrib, ...fractionalPart]) / iqrSpan;
        }
    }
    Statistic.interQuartileMean = interQuartileMean;
    function round(n, precision = 0) {
        const factor = Math.pow(10, precision);
        return Math.round(n * factor) / factor;
    }
    Statistic.round = round;
    function sum(numbers) {
        if (numbers.length === 0) {
            return 0;
        }
        return numbers.reduce((a, b) => a + b);
    }
    Statistic.sum = sum;
})(Statistic || (Statistic = {}));


/***/ }),

/***/ "./lib/styleBenchmarks.js":
/*!********************************!*\
  !*** ./lib/styleBenchmarks.js ***!
  \********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "styleRuleBenchmark": () => (/* binding */ styleRuleBenchmark),
/* harmony export */   "styleRuleGroupBenchmark": () => (/* binding */ styleRuleGroupBenchmark),
/* harmony export */   "styleRuleUsageBenchmark": () => (/* binding */ styleRuleUsageBenchmark),
/* harmony export */   "styleSheetsBenchmark": () => (/* binding */ styleSheetsBenchmark)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _benchmark__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./benchmark */ "./lib/benchmark.js");
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./utils */ "./lib/utils.js");
/* harmony import */ var _dramaturg__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./dramaturg */ "./lib/dramaturg.js");
/* harmony import */ var _css__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./css */ "./lib/css.js");
/* harmony import */ var _ui__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./ui */ "./lib/ui.js");
/* harmony import */ var _schema_benchmark_base_json__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./schema/benchmark-base.json */ "./lib/schema/benchmark-base.json");
/* harmony import */ var _schema_benchmark_rule_json__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./schema/benchmark-rule.json */ "./lib/schema/benchmark-rule.json");
/* harmony import */ var _schema_benchmark_rule_group_json__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./schema/benchmark-rule-group.json */ "./lib/schema/benchmark-rule-group.json");
/* harmony import */ var _schema_benchmark_rule_usage_json__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./schema/benchmark-rule-usage.json */ "./lib/schema/benchmark-rule-usage.json");










class RuleSetMap extends Map {
    add(element, rule) {
        let ruleSet = this.get(element);
        if (!ruleSet) {
            ruleSet = new Set();
            this.set(element, ruleSet);
        }
        ruleSet.add(rule);
    }
    countRulesUsage() {
        const usage = new Map();
        for (const ruleSet of this.values()) {
            for (const selector of ruleSet.values()) {
                usage.set(selector, (usage.get(selector) || 0) + 1);
            }
        }
        return usage;
    }
}
const styleRuleUsageBenchmark = {
    id: 'rule-usage',
    name: 'Style Rule Usage',
    configSchema: _schema_benchmark_rule_usage_json__WEBPACK_IMPORTED_MODULE_1__,
    run: async (scenario, options = {}, progress) => {
        const n = options.repeats || 3;
        const start = Date.now();
        const skipPattern = options.skipPattern
            ? new RegExp(options.skipPattern, 'g')
            : undefined;
        const excludePattern = options.excludeMatchPattern
            ? new RegExp(options.excludeMatchPattern, 'g')
            : undefined;
        if (scenario.setupSuite) {
            await scenario.setupSuite();
        }
        const reference = await (0,_benchmark__WEBPACK_IMPORTED_MODULE_2__.benchmark)(scenario, n * 2, true);
        console.log('Reference for', scenario.name, 'is:', reference);
        const observeEverythingConfig = {
            subtree: true,
            childList: true,
            attributes: true
        };
        const relevantNodes = new Set();
        const collect = mutations => {
            for (const node of (0,_utils__WEBPACK_IMPORTED_MODULE_3__.iterateAffectedNodes)(mutations)) {
                relevantNodes.add(node);
            }
        };
        const collectingObserver = new MutationObserver(collect);
        await (0,_dramaturg__WEBPACK_IMPORTED_MODULE_4__.layoutReady)();
        // Execute action to determine relevant nodes.
        collectingObserver.observe(document.body, observeEverythingConfig);
        await (0,_benchmark__WEBPACK_IMPORTED_MODULE_2__.benchmark)(scenario, n, true);
        await (0,_dramaturg__WEBPACK_IMPORTED_MODULE_4__.layoutReady)();
        collect(collectingObserver.takeRecords(), collectingObserver);
        collectingObserver.disconnect();
        const relevantElements = [...relevantNodes].filter(node => node instanceof Element);
        const filteredElements = relevantElements.filter(element => element.tagName.toLocaleLowerCase() !== 'body');
        console.log('Relevant nodes:', relevantNodes);
        // Find relevant class names and ids for rule style discovery.
        const relevantClassNames = new Set([
            ...filteredElements
                .map(element => [...element.classList.values()])
                .flat()
                .filter(rule => !excludePattern || !rule.match(excludePattern))
        ]);
        const relevantIds = filteredElements
            .filter(element => element.id)
            .map(element => element.id);
        console.log('Relevant class names:', relevantClassNames);
        console.log('Relevant IDs:', relevantIds);
        // Find relevant style rules.
        const results = [];
        const styles = [...document.querySelectorAll('style')];
        const allRules = await (0,_css__WEBPACK_IMPORTED_MODULE_5__.collectRules)(styles, { skipPattern });
        const relevantRules = new Set();
        for (const rule of allRules) {
            for (const className of relevantClassNames) {
                if (rule.selector.includes('.' + className)) {
                    relevantRules.add(rule);
                    break;
                }
            }
            for (const id of relevantIds) {
                if (rule.selector.includes('#' + id)) {
                    relevantRules.add(rule);
                    break;
                }
            }
        }
        const rules = [...relevantRules];
        progress?.emit({ percentage: (100 * 0.5) / rules.length });
        // Prepare observer recording elements matching relevant rules.
        const touches = new Map();
        const seenMatchingRule = new RuleSetMap();
        const touchedMatchingRule = new RuleSetMap();
        const recordMatches = mutations => {
            const touchedNodes = new Set();
            for (const node of (0,_utils__WEBPACK_IMPORTED_MODULE_3__.iterateAffectedNodes)(mutations)) {
                touchedNodes.add(node);
            }
            for (const node of touchedNodes) {
                if (!(node instanceof Element)) {
                    continue;
                }
                for (const rule of relevantRules) {
                    if (node.matches(rule.selector)) {
                        touches.set(rule.selector, (touches.get(rule.selector) || 0) + 1);
                        touchedMatchingRule.add(node, rule.selector);
                    }
                }
            }
            for (const rule of relevantRules) {
                for (const element of document.querySelectorAll(rule.selector)) {
                    seenMatchingRule.add(element, rule.selector);
                }
            }
        };
        // Start counting the nodes matching the relevant rules.
        const recordingObserver = new MutationObserver(recordMatches);
        recordingObserver.observe(document.body, observeEverythingConfig);
        await (0,_benchmark__WEBPACK_IMPORTED_MODULE_2__.benchmark)(scenario, n, true);
        await (0,_dramaturg__WEBPACK_IMPORTED_MODULE_4__.layoutReady)();
        recordMatches(recordingObserver.takeRecords(), recordingObserver);
        recordingObserver.disconnect();
        const uniqueTouches = touchedMatchingRule.countRulesUsage();
        const uniqueApparences = seenMatchingRule.countRulesUsage();
        // Estimate impact of relevant rules on the scenario performance.
        for (let i = 0; i < rules.length; i++) {
            progress?.emit({ percentage: (100 * (i + 0.5)) / rules.length });
            const rule = rules[i];
            // Benchmark without the rule.
            rule.sheet.deleteRule(rule.ruleIndex);
            await (0,_dramaturg__WEBPACK_IMPORTED_MODULE_4__.layoutReady)();
            const measurements = await (0,_benchmark__WEBPACK_IMPORTED_MODULE_2__.benchmark)(scenario, n, true);
            results.push({
                ...measurements,
                selector: rule.selector,
                source: rule.source,
                ruleIndex: rule.ruleIndex,
                stylesheetIndex: rule.stylesheetIndex,
                touchCount: touches.get(rule.selector) || 0,
                elementsTouched: uniqueTouches.get(rule.selector) || 0,
                elementsSeen: uniqueApparences.get(rule.selector) || 0
            });
            // Restore the rule.
            rule.sheet.insertRule(rule.rule.cssText, rule.ruleIndex);
            await (0,_dramaturg__WEBPACK_IMPORTED_MODULE_4__.layoutReady)();
        }
        // Clean up.
        if (scenario.cleanupSuite) {
            await scenario.cleanupSuite();
        }
        progress?.emit({ percentage: 100 });
        return {
            results: results,
            reference: reference.times,
            tags: (0,_utils__WEBPACK_IMPORTED_MODULE_3__.reportTagCounts)(),
            totalTime: Date.now() - start,
            type: 'time'
        };
    },
    sortColumn: 'elementsSeen',
    interpretation: (react__WEBPACK_IMPORTED_MODULE_0___default().createElement((react__WEBPACK_IMPORTED_MODULE_0___default().Fragment), null,
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("ul", null,
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("li", null,
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("code", null, "elementsSeen"),
                ": how many elements were seen on the entire page when executing the scenario."),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("li", null,
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("code", null, "elementsTouched"),
                ": how many elements were modified or in the subtree of a modified element when executing the scenario."),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("li", null,
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("code", null, "touchCount"),
                ": upper bound on how many times the rule matched an element (will be high for rules matching many elements, and for rules matching a single element that is repeatedly modified in the chosen scenario).")),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", null,
            "Low number of ",
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("code", null, "elementsSeen"),
            " suggest potentially unused rule. Negative ",
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("code", null, "\u0394"),
            " highlights rules which may be deteriorating performance.")))
};
const styleSheetsBenchmark = {
    id: 'style-sheet',
    name: 'Style Sheets',
    configSchema: _schema_benchmark_base_json__WEBPACK_IMPORTED_MODULE_6__,
    run: async (scenario, options = {}, progress) => {
        const n = options.repeats || 3;
        const start = Date.now();
        if (scenario.setupSuite) {
            await scenario.setupSuite();
        }
        const styles = [...document.querySelectorAll('style')];
        const reference = await (0,_benchmark__WEBPACK_IMPORTED_MODULE_2__.benchmark)(scenario, n * 2, true);
        console.log('Reference for', scenario.name, 'is:', reference);
        const results = [];
        let j = 0;
        let sheetIndex = 0;
        const stylesWithSheets = styles.filter(style => style.sheet);
        if (stylesWithSheets.length !== styles.length) {
            console.log('Skipped', styles.length - stylesWithSheets.length, 'style tags without stylesheets (out of', styles.length, 'total)');
        }
        for (const style of styles) {
            const sheet = style.sheet;
            // Always increment the sheet index.
            sheetIndex++;
            if (!sheet) {
                continue;
            }
            // Only increment the loop control variable if style included in denominator.
            progress?.emit({ percentage: (100 * j) / stylesWithSheets.length });
            j++;
            // Benchmark the style.
            sheet.disabled = true;
            await (0,_dramaturg__WEBPACK_IMPORTED_MODULE_4__.layoutReady)();
            const measurements = await (0,_benchmark__WEBPACK_IMPORTED_MODULE_2__.benchmark)(scenario, n, true);
            await (0,_dramaturg__WEBPACK_IMPORTED_MODULE_4__.layoutReady)();
            sheet.disabled = false;
            // Extract CSS map
            const cssMap = await (0,_css__WEBPACK_IMPORTED_MODULE_5__.extractSourceMap)(style.textContent);
            // Store result.
            results.push({
                ...measurements,
                content: style.textContent,
                source: cssMap != null ? cssMap.sources[0] : null,
                stylesheetIndex: sheetIndex
            });
        }
        if (scenario.cleanupSuite) {
            await scenario.cleanupSuite();
        }
        progress?.emit({ percentage: 100 });
        return {
            results: results,
            reference: reference.times,
            tags: (0,_utils__WEBPACK_IMPORTED_MODULE_3__.reportTagCounts)(),
            totalTime: Date.now() - start,
            type: 'time'
        };
    }
};
const styleRuleBenchmark = {
    id: 'style-rule',
    name: 'Style Rules',
    configSchema: _schema_benchmark_rule_json__WEBPACK_IMPORTED_MODULE_7__,
    run: async (scenario, options = {}, progress) => {
        const n = options.repeats || 3;
        const skipPattern = options.skipPattern
            ? new RegExp(options.skipPattern, 'g')
            : undefined;
        const start = Date.now();
        if (scenario.setupSuite) {
            await scenario.setupSuite();
        }
        const styles = [...document.querySelectorAll('style')];
        const reference = await (0,_benchmark__WEBPACK_IMPORTED_MODULE_2__.benchmark)(scenario, n * 2, true);
        console.log('Reference for', scenario.name, 'is:', reference);
        const results = [];
        const rules = await (0,_css__WEBPACK_IMPORTED_MODULE_5__.collectRules)(styles, { skipPattern });
        for (let i = 0; i < rules.length; i++) {
            progress?.emit({ percentage: (100 * i) / rules.length });
            const rule = rules[i];
            // benchmark without the rule
            rule.sheet.deleteRule(rule.ruleIndex);
            await (0,_dramaturg__WEBPACK_IMPORTED_MODULE_4__.layoutReady)();
            const measurements = await (0,_benchmark__WEBPACK_IMPORTED_MODULE_2__.benchmark)(scenario, n, true);
            results.push({
                ...measurements,
                selector: rule.selector,
                source: rule.source,
                ruleIndex: rule.ruleIndex,
                stylesheetIndex: rule.stylesheetIndex,
                bgMatches: document.querySelectorAll(rule.selector).length
            });
            // restore the rule
            rule.sheet.insertRule(rule.rule.cssText, rule.ruleIndex);
            await (0,_dramaturg__WEBPACK_IMPORTED_MODULE_4__.layoutReady)();
        }
        if (scenario.cleanupSuite) {
            await scenario.cleanupSuite();
        }
        progress?.emit({ percentage: 100 });
        return {
            results: results,
            reference: reference.times,
            tags: (0,_utils__WEBPACK_IMPORTED_MODULE_3__.reportTagCounts)(),
            totalTime: Date.now() - start,
            type: 'time'
        };
    },
    interpretation: (react__WEBPACK_IMPORTED_MODULE_0___default().createElement((react__WEBPACK_IMPORTED_MODULE_0___default().Fragment), null,
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("ul", null,
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("li", null,
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("code", null, "bgMatches"),
                ": how many elements matched the rule at standby (as compared to during scenario execution); mostly useful to find too broad rules, or potentially unused rules with expensive selectors.")),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", null,
            "Negative ",
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("code", null, "\u0394"),
            " highlights rules which may be deteriorating performance.")))
};
const styleRuleGroupBenchmark = {
    id: 'style-rule-group',
    name: 'Style Rule Groups',
    configSchema: _schema_benchmark_rule_group_json__WEBPACK_IMPORTED_MODULE_8__,
    run: async (scenario, options = {}, progress) => {
        const n = options.repeats || 3;
        const skipPattern = options.skipPattern
            ? new RegExp(options.skipPattern, 'g')
            : undefined;
        const maxBlocks = options.maxBlocks || 5;
        const minBlocks = options.minBlocks || 2;
        const start = Date.now();
        if (scenario.setupSuite) {
            await scenario.setupSuite();
        }
        let styles = [...document.querySelectorAll('style')];
        const reference = await (0,_benchmark__WEBPACK_IMPORTED_MODULE_2__.benchmark)(scenario, n * 2, true);
        console.log('Reference for', scenario.name, 'is:', reference);
        const results = [];
        const randomizations = options.sheetRandomizations || 0;
        let step = 0;
        const total = (maxBlocks - minBlocks + 1) * (randomizations + 1);
        for (let randomization = 0; randomization < randomizations + 1; randomization++) {
            if (randomization !== 0) {
                styles = (0,_utils__WEBPACK_IMPORTED_MODULE_3__.shuffled)(styles);
            }
            const allRules = await (0,_css__WEBPACK_IMPORTED_MODULE_5__.collectRules)(styles, { skipPattern });
            console.log(`Collected ${allRules.length} rules, randomization: ${randomization}`);
            for (let blocks = minBlocks; blocks <= maxBlocks; blocks++) {
                step += 1;
                progress?.emit({ percentage: (100 * step) / total });
                const rulesPerBlock = Math.round(allRules.length / blocks);
                console.log(`Benchmarking ${blocks} blocks, each having ${rulesPerBlock} rules`);
                for (let i = 0; i < blocks; i++) {
                    const rulesInBlock = [];
                    // remove rules from this block
                    for (let j = rulesPerBlock; j >= 0; j--) {
                        const ruleData = allRules[i * rulesPerBlock + j];
                        if (typeof ruleData === 'undefined') {
                            continue;
                        }
                        rulesInBlock.push(ruleData);
                        ruleData.sheet.deleteRule(ruleData.ruleIndex);
                    }
                    await (0,_dramaturg__WEBPACK_IMPORTED_MODULE_4__.layoutReady)();
                    const measurements = await (0,_benchmark__WEBPACK_IMPORTED_MODULE_2__.benchmark)(scenario, n, true);
                    results.push({
                        ...measurements,
                        rulesInBlock: rulesInBlock,
                        block: i,
                        divisions: blocks,
                        randomization: randomization
                    });
                    // restore the rule
                    for (let j = rulesInBlock.length - 1; j >= 0; j--) {
                        const ruleData = rulesInBlock[j];
                        ruleData.sheet.insertRule(ruleData.rule.cssText, ruleData.ruleIndex);
                    }
                    await (0,_dramaturg__WEBPACK_IMPORTED_MODULE_4__.layoutReady)();
                }
            }
        }
        if (scenario.cleanupSuite) {
            await scenario.cleanupSuite();
        }
        progress?.emit({ percentage: 100 });
        return {
            results: results,
            reference: reference.times,
            tags: (0,_utils__WEBPACK_IMPORTED_MODULE_3__.reportTagCounts)(),
            totalTime: Date.now() - start,
            type: 'time'
        };
    },
    render: _ui__WEBPACK_IMPORTED_MODULE_9__.renderBlockResult
};


/***/ }),

/***/ "./lib/table.js":
/*!**********************!*\
  !*** ./lib/table.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ResultTable": () => (/* binding */ ResultTable),
/* harmony export */   "TimingTable": () => (/* binding */ TimingTable)
/* harmony export */ });
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_datagrid__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/datagrid */ "webpack/sharing/consume/default/@lumino/datagrid");
/* harmony import */ var _lumino_datagrid__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_datagrid__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _statistics__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./statistics */ "./lib/statistics.js");



class MouseHandler extends _lumino_datagrid__WEBPACK_IMPORTED_MODULE_1__.BasicMouseHandler {
    constructor() {
        super(...arguments);
        this._clicked = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__.Signal(this);
        this._lastMouseDownHit = null;
    }
    get clicked() {
        return this._clicked;
    }
    onMouseDown(grid, event) {
        const { clientX, clientY } = event;
        const hit = grid.hitTest(clientX, clientY);
        this._lastMouseDownHit = hit;
        super.onMouseDown(grid, event);
    }
    onMouseUp(grid, event) {
        const lastHit = this._lastMouseDownHit;
        if (lastHit) {
            const { clientX, clientY } = event;
            const hit = grid.hitTest(clientX, clientY);
            if (lastHit.column === hit.column && lastHit.row === hit.row) {
                this._clicked.emit(hit);
            }
        }
        super.onMouseUp(grid, event);
    }
    onMouseMove(grid, event) {
        // cancel click to allow smooth resize
        this._lastMouseDownHit = null;
        super.onMouseMove(grid, event);
    }
}
class ResultTable extends _lumino_datagrid__WEBPACK_IMPORTED_MODULE_1__.DataGrid {
    constructor() {
        super();
        this.keyHandler = new _lumino_datagrid__WEBPACK_IMPORTED_MODULE_1__.BasicKeyHandler();
        const mouseHandler = new MouseHandler();
        this.mouseHandler = mouseHandler;
        this.columnNames = [];
        mouseHandler.clicked.connect((_, hit) => {
            this.handleClick(hit);
        });
    }
    setupColumnWidths() {
        this.fitColumnNames('all');
        for (const [name, size] of Object.entries(this.columnWidths)) {
            const index = this.columnNames.indexOf(name);
            if (index !== -1) {
                this.resizeColumn('body', index, size);
            }
        }
    }
}
class TimingTable extends ResultTable {
    constructor(options) {
        super();
        this.columnWidths = {
            source: 325,
            content: 100,
            selector: 175,
            rulesInBlock: 450,
            IQM: 55,
            min: 55,
            Δ: 55,
            'Δ%': 55,
            name: 150,
            resource: 500
        };
        this.sortOrder = 'ascending';
        this.stateSource = options.stateSource;
        const referenceIQM = options.reference
            ? _statistics__WEBPACK_IMPORTED_MODULE_2__.Statistic.interQuartileMean(options.reference)
            : null;
        const anyErrors = options.measurements.some(result => result.errors != null && result.errors.length !== 0);
        const results = options.measurements.map(result => {
            // Make a copy
            result = { ...result };
            // https://github.com/jupyterlab/lumino/issues/448
            if (result['content']) {
                result['content'] = result['content'].substring(0, 500);
            }
            result['times'] = result.times.map(t => _statistics__WEBPACK_IMPORTED_MODULE_2__.Statistic.round(t, 1));
            result['min'] = _statistics__WEBPACK_IMPORTED_MODULE_2__.Statistic.round(_statistics__WEBPACK_IMPORTED_MODULE_2__.Statistic.min(result.times), 1);
            result['mean'] = _statistics__WEBPACK_IMPORTED_MODULE_2__.Statistic.round(_statistics__WEBPACK_IMPORTED_MODULE_2__.Statistic.mean(result.times), 1);
            result['IQM'] = _statistics__WEBPACK_IMPORTED_MODULE_2__.Statistic.round(_statistics__WEBPACK_IMPORTED_MODULE_2__.Statistic.interQuartileMean(result.times), 1);
            if (referenceIQM !== null) {
                result['Δ'] = _statistics__WEBPACK_IMPORTED_MODULE_2__.Statistic.round(_statistics__WEBPACK_IMPORTED_MODULE_2__.Statistic.interQuartileMean(result.times) - referenceIQM, 1);
                result['Δ%'] = _statistics__WEBPACK_IMPORTED_MODULE_2__.Statistic.round((100 * result['Δ']) / referenceIQM, 1);
            }
            if (result.source) {
                result['source'] = result['source']
                    .replace('webpack://./', '')
                    .replace('node_modules', '📦');
            }
            if (result['totalTime']) {
                result['totalTime'] = _statistics__WEBPACK_IMPORTED_MODULE_2__.Statistic.round(result.totalTime, 1);
            }
            if (result['rulesInBlock']) {
                result['rulesInBlock'] = result['rulesInBlock'].map(rule => {
                    return rule.selector;
                });
            }
            if (!anyErrors) {
                delete result['errors'];
            }
            return result;
        });
        this.results = results;
        this.columnNames = results.length > 0 ? Object.keys(results[0]) : [];
        this.sortColumn = options.sortColumn || 'IQM';
        this.sortOrder = options.lowerIsBetter ? 'ascending' : 'descending';
        this._setupDataModel();
        this.setupColumnWidths();
    }
    _createSortFunction() {
        const first = this.results.length > 0 ? this.results[0] : null;
        if (first !== null && typeof first[this.sortColumn] === 'number') {
            if (this.sortOrder === 'ascending') {
                return ((a, b) => b[this.sortColumn] - a[this.sortColumn]).bind(this);
            }
            else {
                return ((a, b) => a[this.sortColumn] - b[this.sortColumn]).bind(this);
            }
        }
        else {
            if (this.sortOrder === 'ascending') {
                return ((a, b) => (b[this.sortColumn] || '')
                    .toString()
                    .localeCompare((a[this.sortColumn] || '').toString())).bind(this);
            }
            else {
                return ((a, b) => (a[this.sortColumn] || '')
                    .toString()
                    .localeCompare((b[this.sortColumn] || '').toString())).bind(this);
            }
        }
    }
    _setupDataModel(keepColumnSize = false) {
        let sizes = [];
        let selectionArgs = null;
        if (this.selectionModel) {
            const selection = this.selectionModel.currentSelection();
            if (selection) {
                selectionArgs = {
                    cursorColumn: this.selectionModel.cursorColumn,
                    cursorRow: this.selectionModel.cursorRow,
                    clear: 'all',
                    ...selection
                };
            }
        }
        if (keepColumnSize) {
            sizes = this.columnNames.map((name, i) => this.columnSize('body', i));
        }
        const sort = this._createSortFunction();
        this.dataModel = new _lumino_datagrid__WEBPACK_IMPORTED_MODULE_1__.JSONModel({
            data: this.results.sort(sort),
            schema: {
                fields: this.columnNames.map(key => {
                    return {
                        name: key,
                        type: 'string'
                    };
                })
            }
        });
        this.selectionModel = new _lumino_datagrid__WEBPACK_IMPORTED_MODULE_1__.BasicSelectionModel({
            dataModel: this.dataModel
        });
        if (keepColumnSize) {
            sizes.map((size, index) => {
                this.resizeColumn('body', index, size);
            });
        }
        if (selectionArgs) {
            this.selectionModel.select(selectionArgs);
        }
    }
    handleClick(hit) {
        if (hit.region === 'column-header') {
            const newSortColumn = this.dataModel.data(hit.region, hit.row, hit.column);
            if (newSortColumn === this.sortColumn) {
                this.sortOrder =
                    this.sortOrder === 'ascending' ? 'descending' : 'ascending';
            }
            else {
                this.sortColumn = newSortColumn;
            }
            this._setupDataModel(true);
            this.update();
        }
    }
}


/***/ }),

/***/ "./lib/templates.js":
/*!**************************!*\
  !*** ./lib/templates.js ***!
  \**************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "CustomArrayTemplateFactory": () => (/* binding */ CustomArrayTemplateFactory),
/* harmony export */   "CustomObjectTemplateFactory": () => (/* binding */ CustomObjectTemplateFactory),
/* harmony export */   "CustomTemplateFactory": () => (/* binding */ CustomTemplateFactory)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _rjsf_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @rjsf/core */ "../../node_modules/@rjsf/core/dist/es/index.js");
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/


// TODO export those templates upstream to avoid copy-pasting them
// TODO stop relying on settings to get defaults?
/**
 * Template to allow for custom buttons to re-order/remove entries in an array.
 * Necessary to create accessible buttons.
 */
const CustomArrayTemplateFactory = (translator) => {
    const trans = translator.load('jupyterlab');
    const factory = (props) => {
        return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: props.className },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(props.TitleField, { title: props.title, required: props.required, id: `${props.idSchema.$id}-title` }),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(props.DescriptionField, { id: `${props.idSchema.$id}-description`, description: props.schema.description ?? '' }),
            props.items.map(item => {
                return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { key: item.key, className: item.className },
                    item.children,
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "jp-ArrayOperations" },
                        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { className: "jp-mod-styled jp-mod-reject", onClick: item.onReorderClick(item.index, item.index - 1), disabled: !item.hasMoveUp }, trans.__('Move Up')),
                        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { className: "jp-mod-styled jp-mod-reject", onClick: item.onReorderClick(item.index, item.index + 1), disabled: !item.hasMoveDown }, trans.__('Move Down')),
                        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { className: "jp-mod-styled jp-mod-warn", onClick: item.onDropIndexClick(item.index), disabled: !item.hasRemove }, trans.__('Remove')))));
            }),
            props.canAdd && (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { className: "jp-mod-styled jp-mod-reject", onClick: props.onAddClick }, trans.__('Add')))));
    };
    factory.displayName = 'JupyterLabArrayTemplate';
    return factory;
};
/**
 * Template with custom add button, necessary for accessiblity and internationalization.
 */
const CustomObjectTemplateFactory = (translator) => {
    const trans = translator.load('jupyterlab');
    const factory = (props) => {
        const { TitleField, DescriptionField } = props;
        return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("fieldset", { id: props.idSchema.$id },
            (props.uiSchema['ui:title'] || props.title) && (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(TitleField, { id: `${props.idSchema.$id}__title`, title: props.title || props.uiSchema['ui:title'], required: props.required })),
            props.description && (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(DescriptionField, { id: `${props.idSchema.$id}__description`, description: props.description })),
            props.properties.map(property => property.content),
            _rjsf_core__WEBPACK_IMPORTED_MODULE_1__.utils.canExpand(props.schema, props.uiSchema, props.formData) && (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { className: "jp-mod-styled jp-mod-reject", onClick: props.onAddClick(props.schema), disabled: props.disabled || props.readonly }, trans.__('Add')))));
    };
    factory.displayName = 'JupyterLabObjectTemplate';
    return factory;
};
/**
 * Renders the modified indicator and errors
 */
const CustomTemplateFactory = (translator) => {
    const trans = translator.load('jupyterlab');
    const factory = (props) => {
        const { schema, label, displayLabel, id, errors, rawErrors, children, onKeyChange, onDropPropertyClick } = props;
        /**
         * Determine if the field has been modified
         * Schema Id is formatted as 'root_<field name>.<nexted field name>'
         * This logic parses out the field name to find the default value
         * before determining if the field has been modified.
         */
        const schemaIds = id.split('_');
        schemaIds.shift();
        const schemaId = schemaIds.join('.');
        const isRoot = schemaId === '';
        const needsDescription = !isRoot && schema.type !== 'object';
        // While we can implement "remove" button for array items in array template,
        // object templates do not provide a way to do this; instead we need to add
        // buttons here (and first check if the field can be removed = is additional).
        const isAdditional = Object.prototype.hasOwnProperty.call(schema, _rjsf_core__WEBPACK_IMPORTED_MODULE_1__.utils.ADDITIONAL_PROPERTY_FLAG);
        return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: `form-group ${displayLabel || schema.type === 'boolean' ? 'small-field' : ''}` },
            // Shows a red indicator for fields that have validation errors
            rawErrors && (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "jp-modifiedIndicator jp-errorIndicator" })),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "jp-FormGroup-content" },
                displayLabel && !isRoot && label && !isAdditional && (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("h3", { className: "jp-FormGroup-fieldLabel jp-FormGroup-contentItem" }, label)),
                isAdditional && (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("input", { className: "jp-FormGroup-contentItem jp-mod-styled", type: "text", onBlur: event => onKeyChange(event.target.value), defaultValue: label })),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: `${isRoot
                        ? 'jp-root'
                        : schema.type === 'object'
                            ? 'jp-objectFieldWrapper'
                            : 'jp-inputFieldWrapper jp-FormGroup-contentItem'}` }, children),
                isAdditional && (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { className: "jp-FormGroup-contentItem jp-mod-styled jp-mod-warn jp-FormGroup-removeButton", onClick: onDropPropertyClick(label) }, trans.__('Remove'))),
                schema.description && needsDescription && (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "jp-FormGroup-description" }, schema.description)),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "validationErrors" }, errors))));
    };
    factory.displayName = 'JupyterLabFieldTemplate';
    return factory;
};


/***/ }),

/***/ "./lib/ui.js":
/*!*******************!*\
  !*** ./lib/ui.js ***!
  \*******************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "BenchmarkHistory": () => (/* binding */ BenchmarkHistory),
/* harmony export */   "BenchmarkLauncher": () => (/* binding */ BenchmarkLauncher),
/* harmony export */   "BenchmarkMonitor": () => (/* binding */ BenchmarkMonitor),
/* harmony export */   "BenchmarkResult": () => (/* binding */ BenchmarkResult),
/* harmony export */   "ProfileTrace": () => (/* binding */ ProfileTrace),
/* harmony export */   "UIProfiler": () => (/* binding */ UIProfiler),
/* harmony export */   "renderBlockResult": () => (/* binding */ renderBlockResult),
/* harmony export */   "renderProfile": () => (/* binding */ renderProfile)
/* harmony export */ });
/* harmony import */ var _rjsf_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @rjsf/core */ "../../node_modules/@rjsf/core/dist/es/index.js");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/statusbar */ "webpack/sharing/consume/default/@jupyterlab/statusbar");
/* harmony import */ var _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_7__);
/* harmony import */ var _jupyterlab_json_extension_lib_component__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! @jupyterlab/json-extension/lib/component */ "../../node_modules/@jupyterlab/json-extension/lib/component.js");
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! ./utils */ "./lib/utils.js");
/* harmony import */ var _jsBenchmarks__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./jsBenchmarks */ "./lib/jsBenchmarks.js");
/* harmony import */ var _templates__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! ./templates */ "./lib/templates.js");
/* harmony import */ var _statistics__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./statistics */ "./lib/statistics.js");
/* harmony import */ var _table__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./table */ "./lib/table.js");
/* harmony import */ var _lumino__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ./lumino */ "./lib/lumino.js");















class ProfileTrace extends (react__WEBPACK_IMPORTED_MODULE_1___default().Component) {
    constructor(props) {
        super(props);
        this.deepest = 0;
        this.contentWidth = 100;
        this.contentHeight = 100;
        this.initialWidth = 100;
        this.state = {
            scale: { x: 1, y: 1 },
            position: { x: 0, y: 0 },
            dimensions: null,
            inDrag: false
        };
        this.handleMouseUp = this.handleMouseUp.bind(this);
        this.handleMouseDown = this.handleMouseDown.bind(this);
        this.handleMouseMove = this.handleMouseMove.bind(this);
        this.handleWheel = this.handleWheel.bind(this);
        this.container = react__WEBPACK_IMPORTED_MODULE_1___default().createRef();
        this.resizeObserver = new ResizeObserver(this.updateSizeInfo.bind(this));
    }
    componentDidMount() {
        const trace = this.props.trace;
        const first = trace.samples[0].timestamp;
        const initialWidth = Math.max(...trace.samples.map(sample => sample.timestamp - first));
        const dimensions = {
            width: this.container.current.offsetWidth,
            height: this.container.current.offsetHeight
        };
        this.setState({
            scale: { x: dimensions.width / initialWidth, y: 1 },
            dimensions
        });
        this.resizeObserver.observe(this.container.current);
    }
    componentWillUnmount() {
        this.resizeObserver.disconnect();
    }
    updateSizeInfo() {
        this.setState({
            dimensions: {
                width: this.container.current.offsetWidth,
                height: this.container.current.offsetHeight
            }
        });
    }
    handleWheel(e) {
        const scale = this.state.scale;
        const newScale = scale.x - e.deltaY / 100;
        if (newScale > 0) {
            this.setState({
                scale: {
                    x: newScale,
                    y: scale.y
                }
            });
        }
    }
    handleMouseMove(e) {
        if (this.state.inDrag) {
            const position = this.state.position;
            const cushion = 50;
            this.setState({
                position: {
                    x: Math.max(Math.min(position.x + e.movementX, this.state.dimensions.width - cushion), -this.contentWidth + cushion),
                    y: 0
                }
            });
        }
    }
    handleMouseUp() {
        this.setState({ inDrag: false });
        document.removeEventListener('mousemove', this.handleMouseMove);
        document.removeEventListener('mouseup', this.handleMouseUp);
    }
    handleMouseDown() {
        this.setState({ inDrag: true });
        document.addEventListener('mousemove', this.handleMouseMove);
        document.addEventListener('mouseup', this.handleMouseUp);
    }
    renderContent() {
        const { trace, itemHeight } = this.props;
        if (!trace.samples) {
            return react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", null, "No samples in trace");
        }
        const first = trace.samples[0].timestamp;
        const frameLocations = [...(0,_jsBenchmarks__WEBPACK_IMPORTED_MODULE_8__.iterateFrames)(trace)];
        this.deepest = Math.max(...frameLocations.map(frame => frame.stackDepth));
        const scale = this.state.scale;
        const samples = trace.samples.map((sample, i) => {
            const nextSample = trace.samples[i + 1];
            const style = {
                width: (nextSample?.timestamp - sample.timestamp) * scale.x,
                left: (sample.timestamp - first) * scale.x
            };
            return (react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { className: "up-ProfileTrace-sample", key: 'sample-' + i, style: style }));
        });
        let contentWidth = 0;
        const frames = frameLocations.map((location, i) => {
            const frame = trace.frames[location.frameId];
            const left = (location.start - first) * scale.x;
            const width = location.duration * scale.x;
            contentWidth = Math.max(contentWidth, left + width);
            const style = {
                width: width,
                top: (location.stackDepth - 1) * itemHeight * scale.y,
                left: left,
                height: itemHeight
            };
            return (react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { className: 'up-ProfileTrace-frame ' +
                    (typeof frame.resourceId === 'undefined'
                        ? 'up-ProfileTrace-frame-native'
                        : ''), key: 'frame-' + i, style: style, title: [
                    frame.name,
                    _statistics__WEBPACK_IMPORTED_MODULE_9__.Statistic.round(location.duration, 1) + 'ms'
                ].join('\n') }, frame.name));
        });
        this.contentWidth = contentWidth;
        this.contentHeight = (2 + this.deepest) * this.props.itemHeight * scale.y;
        // TODO: also show samples as dotted horizontal line with absolute positioning for reference
        return (react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { className: "up-ProfileTrace-content", style: {
                transform: `translate(${this.state.position.x}px, ${this.state.position.y}px)`,
                width: contentWidth + 'px',
                height: this.contentHeight + 'px'
            } },
            frames,
            samples));
    }
    render() {
        return (react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { className: "up-ProfileTrace", onWheel: this.handleWheel, onMouseDown: this.handleMouseDown, ref: this.container }, this.state.dimensions ? this.renderContent() : 'Loading'));
    }
}
function renderProfile(props) {
    // Cache the function table.
    const functionWidget = react__WEBPACK_IMPORTED_MODULE_1___default().useRef(null);
    const [selectedTrace, setTraceSelection] = react__WEBPACK_IMPORTED_MODULE_1___default().useState(0);
    if (functionWidget.current === null ||
        functionWidget.current.stateSource !== props.outcome) {
        const functionTimings = {};
        for (const result of props.outcome.results) {
            for (const trace of result.traces) {
                for (const timing of (0,_jsBenchmarks__WEBPACK_IMPORTED_MODULE_8__.extractTimes)(trace)) {
                    const timingId = [
                        timing.name,
                        timing.resource,
                        timing.column,
                        timing.line
                    ].join('-');
                    if (timingId in functionTimings) {
                        functionTimings[timingId].times.push(timing.time);
                        functionTimings[timingId].totalTime += timing.time;
                        functionTimings[timingId].calls += 1;
                    }
                    else {
                        const entry = {
                            name: timing.name,
                            times: [timing.time],
                            resource: timing.resource,
                            column: timing.column,
                            line: timing.line,
                            calls: 1,
                            totalTime: timing.time
                        };
                        functionTimings[timingId] = entry;
                    }
                }
            }
        }
        const filteredTimings = [...Object.values(functionTimings)].filter(timing => {
            const isNativeProfilerCall = typeof timing.resource === 'undefined' && timing.name === 'Profiler';
            const isOurProfilerCode = timing.resource &&
                timing.resource.includes('@jupyterlab-benchmarks/ui-profiler');
            return !isNativeProfilerCall && !isOurProfilerCode;
        });
        if (filteredTimings.length !== 0) {
            functionWidget.current = new _table__WEBPACK_IMPORTED_MODULE_10__.TimingTable({
                measurements: filteredTimings,
                stateSource: props.outcome,
                sortColumn: 'totalTime',
                lowerIsBetter: true
            });
        }
        else {
            functionWidget.current = null;
        }
    }
    if (selectedTrace > props.outcome.results[0].traces.length) {
        // reset trace
        setTraceSelection(0);
        return react__WEBPACK_IMPORTED_MODULE_1___default().createElement((react__WEBPACK_IMPORTED_MODULE_1___default().Fragment), null);
    }
    return (react__WEBPACK_IMPORTED_MODULE_1___default().createElement((react__WEBPACK_IMPORTED_MODULE_1___default().Fragment), null,
        react__WEBPACK_IMPORTED_MODULE_1___default().createElement("select", { value: selectedTrace, onChange: e => {
                setTraceSelection(Number(e.target.value));
            } }, props.outcome.results[0].traces.map((trace, i) => (react__WEBPACK_IMPORTED_MODULE_1___default().createElement("option", { value: i, key: 'trace-' + i },
            "Trace ",
            i,
            " (",
            trace.samples.length,
            " samples)")))),
        react__WEBPACK_IMPORTED_MODULE_1___default().createElement(ProfileTrace, { trace: props.outcome.results[0].traces[selectedTrace], itemHeight: 20 }),
        functionWidget.current ? (react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_lumino__WEBPACK_IMPORTED_MODULE_11__.LuminoWidget, { widget: functionWidget.current })) : ('No results available. Reduce sampling interval, use macro mode, and/or increase the number of repeats.')));
}
function renderBlockResult(props) {
    const results = props.outcome.results;
    const [display, setDisplay] = react__WEBPACK_IMPORTED_MODULE_1___default().useState('block');
    // Cache the blocks table.
    const blocksWidget = react__WEBPACK_IMPORTED_MODULE_1___default().useRef(null);
    if (blocksWidget.current === null ||
        blocksWidget.current.stateSource !== props.outcome) {
        blocksWidget.current = new _table__WEBPACK_IMPORTED_MODULE_10__.TimingTable({
            measurements: results,
            reference: props.outcome.reference,
            stateSource: props.outcome,
            lowerIsBetter: false
        });
    }
    // Cache the rules table.
    const rulesWidget = react__WEBPACK_IMPORTED_MODULE_1___default().useRef(null);
    if (rulesWidget.current === null ||
        rulesWidget.current.stateSource !== props.outcome) {
        const ruleResults = {};
        for (const block of results) {
            for (const rule of block.rulesInBlock) {
                if (rule.selector in ruleResults) {
                    ruleResults[rule.selector].times.push(...block.times);
                }
                else {
                    const entry = {
                        ...rule,
                        times: [...block.times],
                        errors: block.errors ? [...block.errors] : []
                    };
                    delete entry.sheet;
                    delete entry.rule;
                    ruleResults[rule.selector] = entry;
                }
            }
        }
        rulesWidget.current = new _table__WEBPACK_IMPORTED_MODULE_10__.TimingTable({
            measurements: [...Object.values(ruleResults)],
            reference: props.outcome.reference,
            stateSource: props.outcome,
            lowerIsBetter: false
        });
    }
    return (react__WEBPACK_IMPORTED_MODULE_1___default().createElement((react__WEBPACK_IMPORTED_MODULE_1___default().Fragment), null,
        react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { onChange: (event) => {
                setDisplay(event.target.value);
            } },
            react__WEBPACK_IMPORTED_MODULE_1___default().createElement("label", null,
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement("input", { type: "radio", checked: display === 'block', value: "block" }),
                "Blocks"),
            react__WEBPACK_IMPORTED_MODULE_1___default().createElement("label", null,
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement("input", { type: "radio", checked: display === 'rule', value: "rule" }),
                "Rules")),
        display === 'block' ? (react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_lumino__WEBPACK_IMPORTED_MODULE_11__.LuminoWidget, { widget: blocksWidget.current })) : (react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_lumino__WEBPACK_IMPORTED_MODULE_11__.LuminoWidget, { widget: rulesWidget.current }))));
}
class UIProfiler extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.ReactWidget {
    constructor(props) {
        super();
        this.props = props;
        this.result = null;
        this.progress = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_7__.Signal(this);
        this.handleResult = this.handleResult.bind(this);
        this.loadResult = this.loadResult.bind(this);
        this.manager = new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_3__.ServiceManager();
        this.resultAdded = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_7__.Signal(this);
        this.manager.contents.save(this.props.resultLocation, {
            type: 'directory'
        });
    }
    handleResult(result) {
        this.result = result;
        this.update();
        this.resultAdded.emit(result);
    }
    async loadResult(file) {
        file = await this.manager.contents.get(file.path);
        this.handleResult(JSON.parse(file.content));
    }
    render() {
        return (react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { className: "up-UIProfiler" },
            react__WEBPACK_IMPORTED_MODULE_1___default().createElement(BenchmarkLauncher, Object.assign({ onResult: this.handleResult, progress: this.progress }, this.props)),
            react__WEBPACK_IMPORTED_MODULE_1___default().createElement(BenchmarkHistory, Object.assign({ resultAdded: this.resultAdded, manager: this.manager, onSelect: this.loadResult }, this.props)),
            react__WEBPACK_IMPORTED_MODULE_1___default().createElement(BenchmarkResult, { result: this.result, scenarios: this.props.scenarios, benchmarks: this.props.benchmarks.filter(b => b.id === this.result?.benchmark) })));
    }
}
class BenchmarkHistory extends (react__WEBPACK_IMPORTED_MODULE_1___default().Component) {
    constructor(props) {
        super(props);
        this._handle = null;
        this.state = {
            files: [],
            current: null
        };
        this.update();
        this.update = this.update.bind(this);
        this.props.resultAdded.connect(async (_, result) => {
            await this.update();
            this.setState({
                current: benchmarkFilename(result)
            });
        });
    }
    async update() {
        const dirModel = await this.props.manager.contents.get(this.props.resultLocation);
        const files = dirModel.content.filter((a) => a.path.endsWith('.profile.json'));
        files.sort((a, b) => new Date(b.created).getTime() - new Date(a.created).getTime());
        this.setState({
            files: files
        });
    }
    componentDidMount() {
        this._handle = window.setInterval(this.update, 2000);
    }
    componentWillUnmount() {
        if (this._handle !== null) {
            window.clearInterval(this._handle);
        }
    }
    render() {
        const list = this.state.files.map(file => (react__WEBPACK_IMPORTED_MODULE_1___default().createElement("li", { className: this.state.current === file.name
                ? 'up-BenchmarkHistory-file up-BenchmarkHistory-file-active'
                : 'up-BenchmarkHistory-file', onClick: () => {
                this.props.onSelect(file);
                this.setState({
                    current: file.path
                });
            } }, file.name.replace('.profile.json', ''))));
        return (react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { className: "up-BenchmarkHistory" },
            react__WEBPACK_IMPORTED_MODULE_1___default().createElement("h3", { className: "up-widget-heading" }, "History"),
            react__WEBPACK_IMPORTED_MODULE_1___default().createElement("ul", { className: "up-BenchmarkHistory-files" }, list)));
    }
}
function timingSummary(timing) {
    return (react__WEBPACK_IMPORTED_MODULE_1___default().createElement((react__WEBPACK_IMPORTED_MODULE_1___default().Fragment), null,
        react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { title: timing.reference.sort().map(_statistics__WEBPACK_IMPORTED_MODULE_9__.Statistic.round).join(' ms\n') + ' ms' },
            "Reference: IQM:",
            ' ',
            _statistics__WEBPACK_IMPORTED_MODULE_9__.Statistic.round(_statistics__WEBPACK_IMPORTED_MODULE_9__.Statistic.interQuartileMean(timing.reference), 1),
            " ms, mean: ",
            _statistics__WEBPACK_IMPORTED_MODULE_9__.Statistic.round(_statistics__WEBPACK_IMPORTED_MODULE_9__.Statistic.mean(timing.reference), 1),
            " ms, min:",
            ' ',
            _statistics__WEBPACK_IMPORTED_MODULE_9__.Statistic.round(_statistics__WEBPACK_IMPORTED_MODULE_9__.Statistic.min(timing.reference), 1),
            " ms"),
        react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", null,
            "Total time: ",
            (0,_utils__WEBPACK_IMPORTED_MODULE_12__.formatTime)(timing.totalTime))));
}
function profilingSummary(profile) {
    const first = profile.results[0];
    return (react__WEBPACK_IMPORTED_MODULE_1___default().createElement((react__WEBPACK_IMPORTED_MODULE_1___default().Fragment), null,
        react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", null,
            "Traces: ",
            first.traces.length,
            ". Average number of samples:",
            ' ',
            _statistics__WEBPACK_IMPORTED_MODULE_9__.Statistic.round(_statistics__WEBPACK_IMPORTED_MODULE_9__.Statistic.mean(first.traces.map(trace => trace.samples.length)), 1),
            ", frames:",
            ' ',
            _statistics__WEBPACK_IMPORTED_MODULE_9__.Statistic.round(_statistics__WEBPACK_IMPORTED_MODULE_9__.Statistic.mean(first.traces.map(trace => trace.frames.length)), 1),
            ".",
            ' ',
            react__WEBPACK_IMPORTED_MODULE_1___default().createElement("span", { title: 'Average recorderd: ' +
                    _statistics__WEBPACK_IMPORTED_MODULE_9__.Statistic.round(first.averageSampleInterval, 1) },
                "Sampling interval: ",
                _statistics__WEBPACK_IMPORTED_MODULE_9__.Statistic.round(first.samplingInterval, 1),
                " ms")),
        react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", null,
            "Total time: ",
            (0,_utils__WEBPACK_IMPORTED_MODULE_12__.formatTime)(profile.totalTime))));
}
class BenchmarkResult extends (react__WEBPACK_IMPORTED_MODULE_1___default().Component) {
    constructor() {
        super(...arguments);
        this._table = null;
        this._previousResult = null;
    }
    render() {
        const { result, benchmarks, scenarios } = this.props;
        const wrap = (el) => (react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { className: "up-BenchmarkResult" }, el));
        if (!result) {
            return wrap(react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", null, "Choose a result from the panel, or run a new benchmark."));
        }
        const scenario = scenarios.find(candidate => candidate.id === result.scenario);
        const benchmark = benchmarks.find(candidate => candidate.id === result.benchmark);
        if (!scenario) {
            return wrap(react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", null,
                "Unknown scenario: ",
                result.scenario));
        }
        if (!benchmark) {
            return wrap(react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", null,
                "Unknown benchmark: ",
                result.benchmark));
        }
        if (!benchmark.render && this._previousResult !== result.id) {
            if (result.result.type === 'time') {
                this._table = new _table__WEBPACK_IMPORTED_MODULE_10__.TimingTable({
                    measurements: result.result.results,
                    reference: result.result.reference,
                    sortColumn: benchmark.sortColumn,
                    stateSource: null,
                    lowerIsBetter: false
                });
            }
            else {
                // should there be a default ProfileTable?
                this._table = null;
            }
        }
        const tagsSummary = [...Object.entries(result.result.tags)]
            .map(([tag, count]) => `${tag}:  ${count}`)
            .join('\n');
        const totalTags = _statistics__WEBPACK_IMPORTED_MODULE_9__.Statistic.sum([...Object.values(result.result.tags)]);
        return wrap(react__WEBPACK_IMPORTED_MODULE_1___default().createElement((react__WEBPACK_IMPORTED_MODULE_1___default().Fragment), null,
            react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { className: "up-BenchmarkResult-summary" },
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { className: "up-BenchmarkResult-benchmarkInfo" },
                    react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", null,
                        benchmark.name,
                        " ",
                        scenario.name),
                    result.result.type === 'time'
                        ? timingSummary(result.result)
                        : profilingSummary(result.result)),
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { className: "up-BenchmarkResult-environmentInfo" },
                    react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", null,
                        "Application: ",
                        result.jupyter.client,
                        " ",
                        result.jupyter.version,
                        ' ',
                        result.jupyter.devMode ? 'dev mode' : null,
                        " ",
                        result.jupyter.mode),
                    react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", null,
                        react__WEBPACK_IMPORTED_MODULE_1___default().createElement("span", { title: result.userAgent },
                            "Browser: ",
                            (0,_utils__WEBPACK_IMPORTED_MODULE_12__.extractBrowserVersion)(result.userAgent)),
                        ", ",
                        react__WEBPACK_IMPORTED_MODULE_1___default().createElement("span", { title: tagsSummary },
                            "DOM Elements: ",
                            totalTags)),
                    react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", null,
                        "CPU cores: ",
                        result.hardwareConcurrency))),
            react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { className: "up-BenchmarkResult-options" },
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement("details", null,
                    react__WEBPACK_IMPORTED_MODULE_1___default().createElement("summary", null, "Options"),
                    react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { className: "up-BenchmarkResult-options-benchmark" },
                        react__WEBPACK_IMPORTED_MODULE_1___default().createElement("b", null, "Benchmark"),
                        react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_jupyterlab_json_extension_lib_component__WEBPACK_IMPORTED_MODULE_13__.Component, { data: result.options.benchmark })),
                    react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { className: "up-BenchmarkResult-options-scenario" },
                        react__WEBPACK_IMPORTED_MODULE_1___default().createElement("b", null, "Scenario"),
                        typeof result.options.scenario === 'undefined' ? (react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", null, "No options")) : (react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_jupyterlab_json_extension_lib_component__WEBPACK_IMPORTED_MODULE_13__.Component, { data: result.options.scenario }))))),
            react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { className: "up-BenchmarkResult-details" },
                benchmark.interpretation ? (react__WEBPACK_IMPORTED_MODULE_1___default().createElement("details", null,
                    react__WEBPACK_IMPORTED_MODULE_1___default().createElement("summary", null, "Interpretation"),
                    benchmark.interpretation)) : null,
                benchmark.render ? (react__WEBPACK_IMPORTED_MODULE_1___default().createElement(benchmark.render, { outcome: result.result })) : this._table ? (react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_lumino__WEBPACK_IMPORTED_MODULE_11__.LuminoWidget, { widget: this._table })) : null)));
    }
}
class BenchmarkMonitor extends (react__WEBPACK_IMPORTED_MODULE_1___default().Component) {
    constructor() {
        super(...arguments);
        this.start = null;
        this.end = null;
    }
    render() {
        return (react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { className: "up-BenchmarkMonitor" },
            react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.UseSignal, { signal: this.props.progress, initialArgs: { percentage: -1 } }, (sender, args) => {
                if (!args) {
                    args = {
                        percentage: -1
                    };
                }
                if (args.percentage === 0) {
                    this.start = new Date();
                }
                let elapsed = NaN;
                let remaining = NaN;
                let status;
                if (this.start) {
                    const now = args.percentage === 100 && this.end ? this.end : new Date();
                    this.end = now;
                    elapsed = now.getTime() - this.start.getTime();
                    remaining = ((100 - args.percentage) * elapsed) / args.percentage;
                    status = args.percentage === 100 ? 'up-mod-completed' : '';
                }
                else {
                    status = 'up-mod-waiting';
                }
                return (react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { className: status + ' up-BenchmarkMonitor-content' },
                    react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", null,
                        "Elapsed: ",
                        (0,_utils__WEBPACK_IMPORTED_MODULE_12__.formatTime)(elapsed),
                        ". Remaining:",
                        ' ',
                        (0,_utils__WEBPACK_IMPORTED_MODULE_12__.formatTime)(remaining)),
                    react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_4__.ProgressBar, { percentage: args.percentage })));
            })));
    }
}
function benchmarkId(result) {
    return [
        result.benchmark,
        result.scenario,
        result.completed.toISOString()
    ].join('_');
}
function benchmarkFilename(result) {
    return result.id + '.profile.json';
}
function OptionsStub(props) {
    return (react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { className: "rjsf" },
        react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { className: "jp-root" },
            react__WEBPACK_IMPORTED_MODULE_1___default().createElement("fieldset", null,
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement("legend", null,
                    props.name,
                    " configuration"),
                "No options available for ",
                props.name,
                "."))));
}
class BenchmarkLauncher extends (react__WEBPACK_IMPORTED_MODULE_1___default().Component) {
    constructor(props) {
        super(props);
        this._config = {
            scenarios: {},
            benchmarks: {}
        };
        this.state = {
            benchmarks: [props.benchmarks[0]],
            scenarios: [props.scenarios[0]],
            fieldTemplate: (0,_templates__WEBPACK_IMPORTED_MODULE_14__.CustomTemplateFactory)(this.props.translator),
            arrayFieldTemplate: (0,_templates__WEBPACK_IMPORTED_MODULE_14__.CustomArrayTemplateFactory)(this.props.translator),
            objectFieldTemplate: (0,_templates__WEBPACK_IMPORTED_MODULE_14__.CustomObjectTemplateFactory)(this.props.translator),
            isRunning: false
        };
        this.runSelected = this.runSelected.bind(this);
    }
    async runBenchmark(scenario, benchmark, config) {
        const options = _lumino_coreutils__WEBPACK_IMPORTED_MODULE_5__.JSONExt.deepCopy({
            scenario: config.scenarios[scenario.id],
            benchmark: config.benchmarks[benchmark.id]
        });
        scenario.setOptions(options.scenario);
        this.props.progress.emit({ percentage: 0 });
        const result = (await benchmark.run(scenario, options.benchmark, this.props.progress));
        this.props.progress.emit({ percentage: 100 });
        const data = {
            result: result,
            options: options,
            benchmark: benchmark.id,
            scenario: scenario.id,
            userAgent: window.navigator.userAgent,
            hardwareConcurrency: window.navigator.hardwareConcurrency,
            completed: new Date(),
            windowSize: {
                width: window.innerWidth,
                height: window.innerHeight
            },
            jupyter: this.props.getJupyterState()
        };
        return {
            ...data,
            id: benchmarkId(data)
        };
    }
    onBenchmarkChanged(event) {
        const matched = this.props.benchmarks.find(benchmark => benchmark.id === event.target.value);
        if (!matched) {
            throw Error(`Benchmark not matched ${event.target.value}`);
        }
        let activeBenchmarks = [...this.state.benchmarks];
        if (event.target.checked) {
            activeBenchmarks.push(matched);
        }
        else {
            activeBenchmarks = activeBenchmarks.filter(b => b.id !== matched.id);
        }
        const referenceOrder = this.props.benchmarks.map(s => s.id);
        activeBenchmarks.sort((a, b) => referenceOrder.indexOf(a.id) - referenceOrder.indexOf(b.id));
        this.setState({
            benchmarks: activeBenchmarks
        });
    }
    onScenarioChanged(event) {
        const matched = this.props.scenarios.find(scenario => scenario.id === event.target.value);
        if (!matched) {
            throw Error(`Scenario not matched ${event.target.value}`);
        }
        let activeScenarios = [...this.state.scenarios];
        if (event.target.checked) {
            activeScenarios.push(matched);
        }
        else {
            activeScenarios = activeScenarios.filter(s => s.id !== matched.id);
        }
        const referenceOrder = this.props.scenarios.map(s => s.id);
        activeScenarios.sort((a, b) => referenceOrder.indexOf(a.id) - referenceOrder.indexOf(b.id));
        this.setState({
            scenarios: activeScenarios
        });
    }
    async runSelected() {
        this.setState({
            isRunning: true
        });
        try {
            // copy to prevent user inadvertedly changing what is being run
            const scheduledBenchmarks = [...this.state.benchmarks];
            const scheduledScenarios = [...this.state.scenarios];
            const config = _lumino_coreutils__WEBPACK_IMPORTED_MODULE_5__.JSONExt.deepCopy(this._config);
            for (const benchmark of scheduledBenchmarks) {
                for (const scenario of scheduledScenarios) {
                    const result = await this.runBenchmark(scenario, benchmark, config);
                    const filename = benchmarkFilename(result);
                    this.props.upload(new File(JSON.stringify(result).split('\n'), _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_6__.PathExt.join(this.props.resultLocation, filename), {
                        type: 'application/json'
                    }));
                    this.props.onResult(result);
                }
            }
        }
        catch (e) {
            void (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.showErrorMessage)('Benchmark failed', e);
        }
        this.setState({
            isRunning: false
        });
    }
    render() {
        const benchmarks = this.props.benchmarks.map(benchmark => {
            const disabled = benchmark.isAvailable ? !benchmark.isAvailable() : false;
            return (react__WEBPACK_IMPORTED_MODULE_1___default().createElement("label", { key: benchmark.id, className: disabled ? 'up-label-disabled' : '', title: disabled ? 'This benchmark is not available on this browser' : '' },
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement("input", { type: "checkbox", checked: this.state.benchmarks.includes(benchmark), className: "up-BenchmarkLauncher-choice-input", disabled: disabled, value: benchmark.id }),
                benchmark.name));
        });
        const scenarios = this.props.scenarios.map(scenario => {
            return (react__WEBPACK_IMPORTED_MODULE_1___default().createElement("label", { key: scenario.id },
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement("input", { type: "checkbox", checked: this.state.scenarios.includes(scenario), className: "up-BenchmarkLauncher-choice-input", value: scenario.id }),
                scenario.name));
        });
        // TODO: stop button
        // TODO: custom widget for path selection, FileDialog.getOpenFiles
        return (react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { className: "up-BenchmarkLauncher", style: { height: '450px' } },
            react__WEBPACK_IMPORTED_MODULE_1___default().createElement("h3", { className: "up-widget-heading" }, "Launch"),
            react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { className: "up-BenchmarkLauncher-cards" },
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { className: "up-BenchmarkLauncher-card" },
                    react__WEBPACK_IMPORTED_MODULE_1___default().createElement("h4", { className: "up-card-heading" }, "Benchmark"),
                    react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { className: "up-BenchmarkLauncher-choices", onChange: this.onBenchmarkChanged.bind(this) }, benchmarks),
                    react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { className: "up-BenchmarkLauncher-forms" }, this.state.benchmarks.map(benchmark => {
                        const properties = benchmark.configSchema.properties;
                        if (!properties || Object.keys(properties).length === 0) {
                            return react__WEBPACK_IMPORTED_MODULE_1___default().createElement(OptionsStub, { name: benchmark.name });
                        }
                        benchmark.configSchema.title =
                            benchmark.name + ' configuration';
                        return (react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_rjsf_core__WEBPACK_IMPORTED_MODULE_0__["default"], { key: 'up-profiler-benchmark-' + benchmark.id, schema: benchmark.configSchema, idPrefix: 'up-profiler-benchmark', onChange: form => {
                                this._config.benchmarks[benchmark.id] =
                                    form.formData;
                            }, FieldTemplate: this.state.fieldTemplate, ArrayFieldTemplate: this.state.arrayFieldTemplate, ObjectFieldTemplate: this.state.objectFieldTemplate, liveValidate: true }));
                    }))),
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { className: "up-BenchmarkLauncher-card" },
                    react__WEBPACK_IMPORTED_MODULE_1___default().createElement("h4", { className: "up-card-heading" }, "Scenario"),
                    react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { className: "up-BenchmarkLauncher-choices", onChange: this.onScenarioChanged.bind(this) }, scenarios),
                    react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { className: "up-BenchmarkLauncher-forms" }, this.state.scenarios.map(scenario => {
                        const properties = scenario.configSchema.properties;
                        if (!properties || Object.keys(properties).length === 0) {
                            return react__WEBPACK_IMPORTED_MODULE_1___default().createElement(OptionsStub, { name: scenario.name });
                        }
                        scenario.configSchema.title = scenario.name + ' configuration';
                        return (react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_rjsf_core__WEBPACK_IMPORTED_MODULE_0__["default"], { key: 'up-profiler-scenario-' + scenario.id, schema: scenario.configSchema, idPrefix: 'up-profiler-scenario-' + scenario.id, onChange: form => {
                                this._config.scenarios[scenario.id] =
                                    form.formData;
                            }, FieldTemplate: this.state.fieldTemplate, ArrayFieldTemplate: this.state.arrayFieldTemplate, ObjectFieldTemplate: this.state.objectFieldTemplate, liveValidate: true }));
                    })))),
            react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { className: "up-BenchmarkLauncher-launchbar" },
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement(BenchmarkMonitor, Object.assign({}, this.props)),
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { className: "up-BenchmarkLauncher-launchbar-buttons" },
                    react__WEBPACK_IMPORTED_MODULE_1___default().createElement("button", { onClick: this.runSelected, className: "jp-mod-styled jp-mod-accept", disabled: this.state.scenarios.length === 0 ||
                            this.state.benchmarks.length === 0 ||
                            this.state.isRunning }, "Start")))));
    }
}


/***/ }),

/***/ "./lib/utils.js":
/*!**********************!*\
  !*** ./lib/utils.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "extractBrowserVersion": () => (/* binding */ extractBrowserVersion),
/* harmony export */   "formatTime": () => (/* binding */ formatTime),
/* harmony export */   "iterateAffectedNodes": () => (/* binding */ iterateAffectedNodes),
/* harmony export */   "iterateSubtree": () => (/* binding */ iterateSubtree),
/* harmony export */   "reportTagCounts": () => (/* binding */ reportTagCounts),
/* harmony export */   "shuffled": () => (/* binding */ shuffled)
/* harmony export */ });
function shuffled(array) {
    return array
        .map(value => ({ value, sort: Math.random() }))
        .sort((a, b) => a.sort - b.sort)
        .map(({ value }) => value);
}
function reportTagCounts() {
    const allElements = document.querySelectorAll('*');
    const counts = {};
    for (const elements of allElements.values()) {
        const tagName = elements.tagName.toLocaleLowerCase();
        if (!Object.prototype.hasOwnProperty.call(counts, tagName)) {
            counts[tagName] = 1;
        }
        else {
            counts[tagName] += 1;
        }
    }
    return counts;
}
function formatTime(miliseconds) {
    if (isNaN(miliseconds)) {
        return '-';
    }
    const seconds = miliseconds / 1000;
    const minutes = Math.floor(seconds / 60);
    let formatted = Math.round(seconds - minutes * 60) + ' seconds';
    if (minutes < 1) {
        return formatted;
    }
    const hours = Math.floor(minutes / 60);
    formatted = Math.round(minutes - hours * 60) + ' minutes ' + formatted;
    if (hours < 1) {
        return formatted;
    }
    formatted = Math.round(hours) + ' hours ' + formatted;
    return formatted;
}
/**
 * Simplistic extraction of major browsers data, based on
 * https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/User-Agent
 */
function extractBrowserVersion(userAgent) {
    // order matters!
    const expressions = [
        /Firefox\/\d+/,
        /OPR\/\d+/,
        /Edg\/\d+/,
        /Mobile\/.* Safari\/\d+/,
        /Chrome\/\d+/
    ];
    for (const expr of expressions) {
        const match = userAgent.match(expr);
        if (match) {
            return match[0];
        }
    }
    return 'Unknown browser';
}
function* iterateSubtree(node) {
    for (const child of node.childNodes) {
        yield child;
        yield* iterateSubtree(child);
    }
}
function* iterateAffectedNodes(mutations) {
    for (const mutation of mutations) {
        yield mutation.target;
        for (const node of mutation.addedNodes) {
            if (node === document.body) {
                continue;
            }
            yield node;
            for (const child of iterateSubtree(node)) {
                yield child;
            }
        }
        for (const node of mutation.removedNodes) {
            if (node === document.body) {
                continue;
            }
            yield node;
            for (const child of iterateSubtree(node)) {
                yield child;
            }
        }
    }
}


/***/ }),

/***/ "./lib/schema/benchmark-base.json":
/*!****************************************!*\
  !*** ./lib/schema/benchmark-base.json ***!
  \****************************************/
/***/ ((module) => {

module.exports = JSON.parse('{"title":"Benchmark Options","type":"object","properties":{"repeats":{"title":"Number of repeats","type":"integer","minimum":1,"default":5}}}');

/***/ }),

/***/ "./lib/schema/benchmark-profile.json":
/*!*******************************************!*\
  !*** ./lib/schema/benchmark-profile.json ***!
  \*******************************************/
/***/ ((module) => {

module.exports = JSON.parse('{"title":"Profile Benchmark Options","type":"object","properties":{"repeats":{"title":"Number of repeats","type":"integer","minimum":1,"default":100},"scale":{"title":"Profiling scale","description":"Whether to take multiple profiles, one for each repeat (mico) or one profile averaging across all repeats (macro). Macro-profiling includes setup and cleanup steps which may bias the results for scenarios where expensive operations are performed in these steps. Micro-profiling may be unsuitable for very fast scenarios, and when the browser limits the sampling interval.","type":"string","enum":["micro","macro"],"default":"micro"},"sampleInterval":{"title":"Sample interval","description":"Sampling interval (in milliseconds). Browsers are not required to take samples at this rate and may increase it (Chrome uses 16ms on Windows and 10ms elsewhere).","type":"integer","exclusiveMinimum":0,"default":5},"maxBufferSize":{"title":"Sample buffer size limit","description":"When the limit of samples gets exceeded, the profiling will stop prematurely.","type":"number","exclusiveMinimum":0,"default":10000}},"required":["repeats","scale","sampleInterval","maxBufferSize"]}');

/***/ }),

/***/ "./lib/schema/benchmark-rule-group.json":
/*!**********************************************!*\
  !*** ./lib/schema/benchmark-rule-group.json ***!
  \**********************************************/
/***/ ((module) => {

module.exports = JSON.parse('{"title":"Style Rule Group Benchmark Options","type":"object","properties":{"repeats":{"title":"Number of repeats","type":"integer","minimum":1,"default":5},"skipPattern":{"title":"Regular expression to filter out rules","type":"string","default":"(fa-|Icon|bp3|mod-hidden)"},"minBlocks":{"title":"Block size to start with","type":"integer","minimum":1,"default":3},"maxBlocks":{"title":"Maximal block size","type":"integer","minimum":1,"default":5},"sheetRandomizations":{"title":"Number of sheet randomizations","type":"integer","minimum":0,"default":5}}}');

/***/ }),

/***/ "./lib/schema/benchmark-rule-usage.json":
/*!**********************************************!*\
  !*** ./lib/schema/benchmark-rule-usage.json ***!
  \**********************************************/
/***/ ((module) => {

module.exports = JSON.parse('{"title":"Style Rule Usage Options","type":"object","properties":{"repeats":{"title":"Number of repeats","type":"integer","minimum":1,"default":5},"skipPattern":{"title":"Regular expression to filter out rules","type":"string","default":"::"},"excludeMatchPattern":{"title":"Regular expression to filter out classes used for rule discovery","type":"string","default":"(fa-|jp-icon|Icon|lm-Widget|lm-mod-|jp-mod-|p-mod-|p-Widget)"}}}');

/***/ }),

/***/ "./lib/schema/benchmark-rule.json":
/*!****************************************!*\
  !*** ./lib/schema/benchmark-rule.json ***!
  \****************************************/
/***/ ((module) => {

module.exports = JSON.parse('{"title":"Style Rule Benchmark Options","type":"object","properties":{"repeats":{"title":"Number of repeats","type":"integer","minimum":1,"default":3},"skipPattern":{"title":"Regular expression to filter out rules","type":"string","default":"(fa-|Icon|bp3|mod-hidden)"}}}');

/***/ }),

/***/ "./lib/schema/scenario-base.json":
/*!***************************************!*\
  !*** ./lib/schema/scenario-base.json ***!
  \***************************************/
/***/ ((module) => {

module.exports = JSON.parse('{"title":"Scenario Options","type":"object","properties":{}}');

/***/ }),

/***/ "./lib/schema/scenario-completer.json":
/*!********************************************!*\
  !*** ./lib/schema/scenario-completer.json ***!
  \********************************************/
/***/ ((module) => {

module.exports = JSON.parse('{"title":"Completer Scenario Options","type":"object","properties":{"editor":{"title":"Editor type","description":"Editor widget to test completion in","type":"string","enum":["Notebook","File Editor"],"default":"File Editor"},"path":{"title":"Path to document","description":"Optional path to an existing document of specified editor type. When empty (default) a new temporary file will be created.","type":"string","default":""},"setup":{"title":"Editor setup for completion","description":"How should the editor be populated?","default":{"tokenCount":1000,"tokenSize":50},"anyOf":[{"type":"object","title":"Auto-generate tokens to complete","properties":{"tokenCount":{"title":"Token count","description":"The number of completion items to generate","type":"number","minimum":1,"default":1000},"tokenSize":{"title":"Token size","description":"The number characters in each token","type":"number","minimum":1,"default":50}},"required":["tokenCount","tokenSize"]},{"type":"object","title":"I will provide a custom text","properties":{"setupText":{"title":"Path","description":"Text to enter into the editor. Last line should include a partial token on which the completion will be riggered.","type":"string","default":""}},"required":["setupText"]}]}},"required":["editor","setup"],"additionalProperties":false}');

/***/ }),

/***/ "./lib/schema/scenario-menu-open.json":
/*!********************************************!*\
  !*** ./lib/schema/scenario-menu-open.json ***!
  \********************************************/
/***/ ((module) => {

module.exports = JSON.parse('{"title":"Menu Open Scenario Options","type":"object","properties":{"menu":{"title":"The menu to open","type":"string","default":"file","enum":["file","edit","view","run","kernel","settings","help"]}},"required":["menu"]}');

/***/ }),

/***/ "./lib/schema/scenario-scroll.json":
/*!*****************************************!*\
  !*** ./lib/schema/scenario-scroll.json ***!
  \*****************************************/
/***/ ((module) => {

module.exports = JSON.parse('{"title":"Scroll Scenario Options","type":"object","properties":{"scrollTop":{"title":"Scroll from top","description":"Number of pixes to scroll by","type":"number","minimum":0,"default":10000},"scrollBehavior":{"title":"Scroll behaviour","description":"Behavior of scroll, either \'smooth\' for smooth scrolling, or \'auto\' for instant scrolling.","type":"string","enum":["smooth","auto"],"default":"smooth"},"cellByCell":{"title":"Traverse cell-by-cell","description":"Instead of scrolling, traverse notebook cell-by-cell (which also combines stepwise scrolling and cell activation/deactivation). Small number of cells (50-100) is recommended for benchmarking such scenario. \'scrollTop\' and \'scrollBehavior\' have no effect if this variant is enabled. Has no effect in file editor.","type":"boolean","default":false},"editor":{"title":"Editor type","description":"Editor widget to test completion in","type":"string","enum":["Notebook","File Editor"],"default":"Notebook"},"path":{"title":"Path to document","description":"Optional path to an existing document of specified editor type. When empty (default) a new temporary file will be created.","type":"string","default":""},"cells":{"title":"Number of cells/blocks to append","description":"If using a notebook, how many cell should be created? For file editor, how many lines?","type":"number","minimum":0,"default":1000},"editorContent":{"title":"Editor/cell content","description":"Text to populate editors/cells with.","type":"string","default":"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."}},"required":["editor","cells","scrollTop","scrollBehavior"],"additionalProperties":false}');

/***/ }),

/***/ "./lib/schema/scenario-sidebars.json":
/*!*******************************************!*\
  !*** ./lib/schema/scenario-sidebars.json ***!
  \*******************************************/
/***/ ((module) => {

module.exports = JSON.parse('{"title":"Sidebars Scenario Options","type":"object","properties":{"sidebars":{"title":"The sidebars to open","type":"array","default":["table-of-contents","jp-debugger-sidebar","jp-property-inspector","filebrowser","extensionmanager.main-view","jp-running-sessions"],"items":{"type":"string"}}},"required":["sidebars"]}');

/***/ }),

/***/ "./lib/schema/scenario-tabs.json":
/*!***************************************!*\
  !*** ./lib/schema/scenario-tabs.json ***!
  \***************************************/
/***/ ((module) => {

module.exports = JSON.parse('{"title":"Tab Scenario Options","type":"object","definitions":{"tab":{"description":"Tab to open","type":"object","default":{"type":"launcher"},"anyOf":[{"type":"object","title":"File","properties":{"path":{"title":"Path","description":"Path to the file/notebook to open as a tab","type":"string"},"type":{"title":"Type","description":"Type of the tab","type":"string","enum":["file"],"default":"file"}},"required":["type"]},{"type":"object","title":"Launcher","properties":{"type":{"title":"Type","description":"Type of the tab","type":"string","enum":["launcher"],"default":"launcher"}},"required":["type"]}]}},"properties":{"tabs":{"title":"List of tabs to use in scenario","description":"Series of two or more tabs","type":"array","items":{"$ref":"#/definitions/tab"},"default":[{"type":"launcher"},{"type":"launcher"}]}},"required":["tabs"]}');

/***/ })

}]);
//# sourceMappingURL=lib_index_js.f76895f98fd725cf2ece.js.map