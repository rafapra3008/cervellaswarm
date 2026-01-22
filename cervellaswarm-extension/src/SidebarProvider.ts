import * as vscode from 'vscode';

/**
 * SidebarProvider - CervellaSwarm Control Panel
 *
 * Provides a webview sidebar for:
 * - Running tasks via CLI
 * - Displaying worker status
 * - Task history
 */
export class SidebarProvider implements vscode.WebviewViewProvider {
    public static readonly viewType = 'cervellaswarm.sidebar';
    private _view?: vscode.WebviewView;
    private _terminal?: vscode.Terminal;

    constructor(private readonly _extensionUri: vscode.Uri) {}

    public resolveWebviewView(
        webviewView: vscode.WebviewView,
        _context: vscode.WebviewViewResolveContext,
        _token: vscode.CancellationToken
    ) {
        this._view = webviewView;

        webviewView.webview.options = {
            enableScripts: true,
            localResourceRoots: [this._extensionUri]
        };

        webviewView.webview.html = this._getHtmlContent(webviewView.webview);

        // Handle messages from webview
        webviewView.webview.onDidReceiveMessage(async (data) => {
            switch (data.type) {
                case 'runTask': {
                    await this._runTask(data.task);
                    break;
                }
                case 'spawnWorker': {
                    await this._spawnWorker(data.worker);
                    break;
                }
                case 'checkStatus': {
                    await this._checkSwarmStatus();
                    break;
                }
            }
        });
    }

    /**
     * Run a task via cervellaswarm CLI
     */
    private async _runTask(task: string): Promise<void> {
        if (!task || task.trim() === '') {
            vscode.window.showWarningMessage('Please enter a task description');
            return;
        }

        // Create or reuse terminal
        this._terminal = this._getOrCreateTerminal();
        this._terminal.show();

        // Run the task command
        this._terminal.sendText(`cervellaswarm task "${task}"`);

        // Update webview status
        this._updateStatus('working', `Running: ${task}`);

        vscode.window.showInformationMessage(`Task started: ${task}`);
    }

    /**
     * Spawn a specific worker
     */
    private async _spawnWorker(worker: string): Promise<void> {
        this._terminal = this._getOrCreateTerminal();
        this._terminal.show();

        // Use spawn-workers script
        this._terminal.sendText(`spawn-workers --${worker}`);

        this._updateStatus('working', `Spawning: ${worker}`);
        vscode.window.showInformationMessage(`Spawning cervella-${worker}...`);
    }

    /**
     * Check swarm status
     */
    private async _checkSwarmStatus(): Promise<void> {
        this._terminal = this._getOrCreateTerminal();
        this._terminal.show();

        this._terminal.sendText('cervellaswarm status');
    }

    /**
     * Get or create the CervellaSwarm terminal
     */
    private _getOrCreateTerminal(): vscode.Terminal {
        // Find existing terminal
        const existing = vscode.window.terminals.find(t => t.name === 'CervellaSwarm');
        if (existing) {
            return existing;
        }

        // Create new terminal
        return vscode.window.createTerminal({
            name: 'CervellaSwarm',
            iconPath: new vscode.ThemeIcon('hubot')
        });
    }

    /**
     * Update status in webview
     */
    private _updateStatus(status: string, message: string): void {
        if (this._view) {
            this._view.webview.postMessage({
                type: 'statusUpdate',
                status,
                message
            });
        }
    }

    /**
     * Generate HTML content for the webview
     */
    private _getHtmlContent(webview: vscode.Webview): string {
        return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CervellaSwarm</title>
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }
        body {
            font-family: var(--vscode-font-family);
            font-size: var(--vscode-font-size);
            color: var(--vscode-foreground);
            background: var(--vscode-sideBar-background);
            padding: 12px;
        }
        h2 {
            font-size: 14px;
            font-weight: 600;
            margin-bottom: 12px;
            color: var(--vscode-sideBarSectionHeader-foreground);
        }
        .section {
            margin-bottom: 20px;
        }
        input[type="text"] {
            width: 100%;
            padding: 8px;
            border: 1px solid var(--vscode-input-border);
            background: var(--vscode-input-background);
            color: var(--vscode-input-foreground);
            border-radius: 4px;
            font-size: 13px;
        }
        input[type="text"]:focus {
            outline: 1px solid var(--vscode-focusBorder);
        }
        button {
            width: 100%;
            padding: 8px 12px;
            margin-top: 8px;
            background: var(--vscode-button-background);
            color: var(--vscode-button-foreground);
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 13px;
        }
        button:hover {
            background: var(--vscode-button-hoverBackground);
        }
        button.secondary {
            background: var(--vscode-button-secondaryBackground);
            color: var(--vscode-button-secondaryForeground);
        }
        .worker-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 8px;
        }
        .worker-btn {
            padding: 6px;
            font-size: 11px;
        }
        .status-box {
            padding: 12px;
            background: var(--vscode-editor-background);
            border: 1px solid var(--vscode-panel-border);
            border-radius: 4px;
            font-size: 12px;
        }
        .status-idle { border-left: 3px solid var(--vscode-charts-green); }
        .status-working { border-left: 3px solid var(--vscode-charts-yellow); }
        .status-error { border-left: 3px solid var(--vscode-charts-red); }
        .status-label {
            font-weight: 600;
            text-transform: uppercase;
            font-size: 10px;
            letter-spacing: 0.5px;
            margin-bottom: 4px;
        }
        .status-message {
            color: var(--vscode-descriptionForeground);
        }
        .divider {
            height: 1px;
            background: var(--vscode-panel-border);
            margin: 16px 0;
        }
    </style>
</head>
<body>
    <div class="section">
        <h2>New Task</h2>
        <input type="text" id="taskInput" placeholder="Describe your task..." />
        <button id="runTaskBtn">Run Task</button>
    </div>

    <div class="divider"></div>

    <div class="section">
        <h2>Status</h2>
        <div id="statusBox" class="status-box status-idle">
            <div class="status-label">IDLE</div>
            <div class="status-message">Ready for tasks</div>
        </div>
    </div>

    <div class="divider"></div>

    <div class="section">
        <h2>Quick Spawn</h2>
        <div class="worker-grid">
            <button class="worker-btn secondary" data-worker="backend">Backend</button>
            <button class="worker-btn secondary" data-worker="frontend">Frontend</button>
            <button class="worker-btn secondary" data-worker="tester">Tester</button>
            <button class="worker-btn secondary" data-worker="researcher">Researcher</button>
        </div>
    </div>

    <div class="divider"></div>

    <div class="section">
        <button id="checkStatusBtn" class="secondary">Check Swarm Status</button>
    </div>

    <script>
        const vscode = acquireVsCodeApi();

        // Task input handling
        const taskInput = document.getElementById('taskInput');
        const runTaskBtn = document.getElementById('runTaskBtn');

        runTaskBtn.addEventListener('click', () => {
            const task = taskInput.value.trim();
            if (task) {
                vscode.postMessage({ type: 'runTask', task });
                taskInput.value = '';
            }
        });

        taskInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                runTaskBtn.click();
            }
        });

        // Worker spawn buttons
        document.querySelectorAll('.worker-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const worker = btn.dataset.worker;
                vscode.postMessage({ type: 'spawnWorker', worker });
            });
        });

        // Check status button
        document.getElementById('checkStatusBtn').addEventListener('click', () => {
            vscode.postMessage({ type: 'checkStatus' });
        });

        // Handle messages from extension
        window.addEventListener('message', event => {
            const message = event.data;
            switch (message.type) {
                case 'statusUpdate': {
                    const statusBox = document.getElementById('statusBox');
                    statusBox.className = 'status-box status-' + message.status;
                    statusBox.querySelector('.status-label').textContent = message.status.toUpperCase();
                    statusBox.querySelector('.status-message').textContent = message.message;
                    break;
                }
            }
        });
    </script>
</body>
</html>`;
    }
}
