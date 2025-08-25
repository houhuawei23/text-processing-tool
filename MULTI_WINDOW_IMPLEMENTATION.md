# Multi-Window Functionality Implementation

## Overview

This document describes the implementation of multi-window input and output functionality for the text processing application. The feature allows users to add multiple input windows for text entry and corresponding output windows for displaying processing results.

## Features Implemented

### 1. Multi-Input Windows
- **Dynamic Addition**: Users can add new input windows using the "+" button
- **Dynamic Removal**: Users can remove input windows using the "-" button (minimum 1 window maintained)
- **Character Counting**: Total character count across all input windows
- **Independent Text Entry**: Each window can contain different text content

### 2. Multi-Output Windows
- **Automatic Creation**: Output windows are automatically created to match input windows
- **Multiple Views**: Each output window supports three views:
  - Processed Text
  - Statistics Information
  - Text Analysis
- **Synchronized View Switching**: All output windows switch views together

### 3. Processing Integration
- **Batch Processing**: All input windows are processed simultaneously
- **Parallel API Calls**: Multiple API requests are made in parallel for efficiency
- **Result Mapping**: Each input window's result is displayed in a corresponding output window
- **Error Handling**: Individual window failures don't affect other windows

## Technical Implementation

### JavaScript Changes

#### New Class Properties
```javascript
class TextProcessorApp {
    constructor() {
        this.inputWindows = [];        // Array of input window objects
        this.outputWindows = [];       // Array of output window objects
        this.nextWindowId = 2;         // Next available window ID
    }
}
```

#### Window Management Methods
- `initializeWindows()`: Sets up initial input and output windows
- `addInputWindow()`: Creates new input window with unique ID
- `removeInputWindow()`: Removes last input window (maintains minimum 1)
- `addOutputWindow()`: Creates new output window with all view types
- `removeOutputWindow()`: Removes last output window (maintains minimum 1)
- `updateWindowControlButtons()`: Enables/disables remove buttons based on window count

#### Enhanced Processing Methods
- `processText()`: Processes all input windows and distributes results to output windows
- `processRegex()`: Applies regex rules to all input windows
- `translateText()`: Translates text from all input windows
- `updateUIWithMultipleResults()`: Updates all output windows with corresponding results

#### View Management
- `setupViewToggle()`: Handles view switching across all output windows
- `switchToView()`: Switches all output windows to specified view type

### HTML Structure Changes

#### Input Section
```html
<div class="input-window">
    <div class="section-header">
        <h2>输入文本</h2>
        <div class="input-controls">
            <div class="text-counter">
                <span id="charCount">0</span> 字符
            </div>
            <div class="window-controls">
                <button id="addInputWindow" class="btn btn-sm btn-outline">+</button>
                <button id="removeInputWindow" class="btn btn-sm btn-outline" disabled>-</button>
            </div>
        </div>
    </div>
    <div class="input-windows-container">
        <!-- Dynamic input windows -->
    </div>
</div>
```

#### Output Section
```html
<div class="output-window">
    <div class="section-header">
        <h2>处理结果</h2>
        <div class="output-controls">
            <div class="view-toggle">
                <!-- View toggle buttons -->
            </div>
            <div class="window-controls">
                <button id="addOutputWindow" class="btn btn-sm btn-outline">+</button>
                <button id="removeOutputWindow" class="btn btn-sm btn-outline" disabled>-</button>
            </div>
        </div>
    </div>
    <div class="output-windows-container">
        <!-- Dynamic output windows -->
    </div>
</div>
```

### CSS Styling

#### Window Controls
```css
.input-controls,
.output-controls {
    display: flex;
    align-items: center;
    gap: 15px;
}

.window-controls {
    display: flex;
    gap: 8px;
}

.window-controls .btn {
    padding: 6px 10px;
    font-size: 12px;
    min-width: 32px;
    height: 32px;
}
```

#### Window Containers
```css
.input-windows-container,
.output-windows-container {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.input-window-item,
.output-window-item {
    border: 1px solid var(--border-color);
    border-radius: var(--border-radius);
    padding: 15px;
    position: relative;
}
```

#### Window Identifiers
```css
.input-window-item::before,
.output-window-item::before {
    content: attr(data-window-id);
    position: absolute;
    top: -8px;
    left: 15px;
    background: var(--primary-color);
    color: white;
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 11px;
    font-weight: 600;
}
```

## Usage Examples

### Adding Input Windows
1. Click the "+" button in the input section header
2. A new input window appears with a unique ID
3. Enter text in the new window
4. Character count updates to show total across all windows

### Processing Multiple Texts
1. Enter different text in each input window
2. Click "处理文本" (Process Text) button
3. System processes all input windows simultaneously
4. Results appear in corresponding output windows
5. Additional output windows are created automatically if needed

### View Switching
1. Use view toggle buttons (处理文本, 统计信息, 文本分析)
2. All output windows switch to the selected view simultaneously
3. Each window maintains its own content for each view type

## Benefits

1. **Efficiency**: Process multiple texts simultaneously instead of sequentially
2. **Comparison**: Easily compare results from different input texts
3. **Organization**: Keep related texts and results grouped together
4. **Flexibility**: Add or remove windows as needed for different workflows
5. **Scalability**: Handle varying numbers of input/output pairs dynamically

## Error Handling

- **Minimum Windows**: System prevents removal of the last input/output window
- **API Failures**: Individual window processing failures don't affect other windows
- **Validation**: Empty input windows are filtered out before processing
- **User Feedback**: Clear success/error messages for all operations

## Future Enhancements

1. **Window Persistence**: Save window configurations between sessions
2. **Drag & Drop**: Reorder windows by dragging
3. **Window Templates**: Pre-configured window layouts for common workflows
4. **Batch Operations**: Apply operations to specific window groups
5. **Export/Import**: Save and restore window contents and configurations

## Testing

A test file `test_multi_window.html` is provided to verify the basic multi-window functionality works correctly. This can be used to test the core features before integrating with the main application.

## Conclusion

The multi-window functionality significantly enhances the text processing application by allowing users to work with multiple texts simultaneously. The implementation is robust, user-friendly, and maintains backward compatibility while adding powerful new capabilities.
