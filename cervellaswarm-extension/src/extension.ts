import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';

/**
 * Extension activation entry point
 */
export function activate(context: vscode.ExtensionContext) {
	console.log('CervellaSwarm extension activated!');

	// Register all commands
	const commands = [
		vscode.commands.registerCommand('cervellaswarm.initialize', initializeWorkspace),
		vscode.commands.registerCommand('cervellaswarm.installAgents', installAgents),
		vscode.commands.registerCommand('cervellaswarm.checkStatus', checkStatus),
		vscode.commands.registerCommand('cervellaswarm.openDashboard', openDashboard),
		vscode.commands.registerCommand('cervellaswarm.launchAgent', launchAgent),
		vscode.commands.registerCommand('cervellaswarm.showHelp', showHelp),
	];

	context.subscriptions.push(...commands);
}

/**
 * 1. Initialize Workspace
 * Creates .vscode/agents folder if it doesn't exist
 */
async function initializeWorkspace(): Promise<boolean> {
	try {
		const workspaceFolder = vscode.workspace.workspaceFolders?.[0];

		if (!workspaceFolder) {
			vscode.window.showErrorMessage('No workspace folder open. Please open a folder first.');
			return false;
		}

		const agentsPath = path.join(workspaceFolder.uri.fsPath, '.vscode', 'agents');

		// Create .vscode/agents if doesn't exist
		if (!fs.existsSync(agentsPath)) {
			fs.mkdirSync(agentsPath, { recursive: true });
			vscode.window.showInformationMessage(
				'CervellaSwarm initialized! Created .vscode/agents folder.'
			);
		} else {
			vscode.window.showInformationMessage(
				'CervellaSwarm already initialized! .vscode/agents folder exists.'
			);
		}

		return true;
	} catch (error) {
		vscode.window.showErrorMessage(`Failed to initialize workspace: ${error}`);
		return false;
	}
}

/**
 * 2. Install Agents
 * Placeholder for future implementation
 */
async function installAgents(): Promise<void> {
	vscode.window.showInformationMessage(
		'Install Agents feature coming soon! For now, manually copy agent files to .vscode/agents/'
	);
	// TODO: Copy agent files from extension to workspace
}

/**
 * 3. Check Status
 * Verifies workspace setup and counts installed agents
 */
async function checkStatus(): Promise<void> {
	try {
		const workspaceFolder = vscode.workspace.workspaceFolders?.[0];

		if (!workspaceFolder) {
			vscode.window.showWarningMessage('No workspace folder open.');
			return;
		}

		const agentsPath = path.join(workspaceFolder.uri.fsPath, '.vscode', 'agents');

		if (!fs.existsSync(agentsPath)) {
			vscode.window.showWarningMessage(
				'Workspace not initialized. Run "Initialize Workspace" first.'
			);
			return;
		}

		// Count .md files in agents folder
		const files = fs.readdirSync(agentsPath);
		const agentFiles = files.filter(f => f.endsWith('.md'));
		const count = agentFiles.length;

		vscode.window.showInformationMessage(
			`CervellaSwarm Status: ${count} agent${count !== 1 ? 's' : ''} installed in .vscode/agents/`
		);
	} catch (error) {
		vscode.window.showErrorMessage(`Failed to check status: ${error}`);
	}
}

/**
 * 4. Open Dashboard
 * Placeholder for future webview implementation
 */
async function openDashboard(): Promise<void> {
	vscode.window.showInformationMessage(
		'Dashboard coming soon! Stay tuned for the interactive agent management interface.'
	);
	// TODO: Open webview dashboard
}

/**
 * 5. Launch Agent
 * Shows QuickPick to select and launch an agent
 */
async function launchAgent(): Promise<void> {
	const agents = [
		{ label: '🎨 cervella-frontend', description: 'React, CSS, UI/UX specialist' },
		{ label: '⚙️ cervella-backend', description: 'Python, FastAPI, API specialist' },
		{ label: '🧪 cervella-tester', description: 'Testing, Debug, QA specialist' },
		{ label: '📋 cervella-reviewer', description: 'Code review specialist' },
		{ label: '🔬 cervella-researcher', description: 'Research and analysis specialist' },
	];

	const selected = await vscode.window.showQuickPick(agents, {
		placeHolder: 'Select an agent to launch',
		title: 'CervellaSwarm - Launch Agent'
	});

	if (selected) {
		const agentName = selected.label.split(' ')[1]; // Extract name without emoji
		vscode.window.showInformationMessage(`Launching ${agentName}...`);
		// TODO: Actual agent launch logic
	}
}

/**
 * 6. Show Help
 * Opens documentation in external browser
 */
async function showHelp(): Promise<void> {
	const url = 'https://github.com/rafapra/CervellaSwarm#readme';
	vscode.env.openExternal(vscode.Uri.parse(url));
}

/**
 * Extension deactivation cleanup
 */
export function deactivate() {
	console.log('CervellaSwarm extension deactivated.');
}
