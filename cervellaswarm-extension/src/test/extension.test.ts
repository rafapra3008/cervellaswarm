import * as assert from 'assert';
import * as vscode from 'vscode';

suite('CervellaSwarm Extension Test Suite', () => {

	test('Extension should be present', () => {
		const extension = vscode.extensions.getExtension('rafapra.cervellaswarm');
		assert.ok(extension, 'Extension should be installed');
	});

	test('Extension should activate', async () => {
		const extension = vscode.extensions.getExtension('rafapra.cervellaswarm');
		assert.ok(extension, 'Extension should be installed');

		// Activate extension
		await extension.activate();
		assert.ok(extension.isActive, 'Extension should be active');
	});

	test('All commands should be registered', async () => {
		const commands = await vscode.commands.getCommands(true);

		const expectedCommands = [
			'cervellaswarm.initialize',
			'cervellaswarm.installAgents',
			'cervellaswarm.checkStatus',
			'cervellaswarm.openDashboard',
			'cervellaswarm.launchAgent',
			'cervellaswarm.showHelp',
		];

		for (const cmd of expectedCommands) {
			assert.ok(
				commands.includes(cmd),
				`Command "${cmd}" should be registered`
			);
		}
	});

	test('Initialize command should work', async function() {
		// Skip if no workspace folder
		if (!vscode.workspace.workspaceFolders?.[0]) {
			this.skip();
			return;
		}

		// Execute initialize command
		const result = await vscode.commands.executeCommand('cervellaswarm.initialize');

		// Command should complete (returns boolean)
		assert.ok(result !== undefined, 'Initialize command should return a result');
	});

	test('Check status command should work', async function() {
		// Skip if no workspace folder
		if (!vscode.workspace.workspaceFolders?.[0]) {
			this.skip();
			return;
		}

		// Execute check status command - should not throw
		try {
			await vscode.commands.executeCommand('cervellaswarm.checkStatus');
			assert.ok(true, 'Check status command executed successfully');
		} catch (error) {
			assert.fail(`Check status command failed: ${error}`);
		}
	});

	test('Launch agent command should be executable', async () => {
		// Just verify the command exists and is callable
		const commands = await vscode.commands.getCommands(true);
		assert.ok(
			commands.includes('cervellaswarm.launchAgent'),
			'Launch agent command should be available'
		);
	});

	test('Sidebar view should be registered', () => {
		// Verify sidebar contribution in package.json is recognized
		const extension = vscode.extensions.getExtension('rafapra.cervellaswarm');
		assert.ok(extension, 'Extension should be installed');

		const packageJSON = extension.packageJSON;
		const views = packageJSON?.contributes?.views?.cervellaswarm;

		assert.ok(views, 'Sidebar views should be defined');
		assert.ok(views.length > 0, 'At least one view should be defined');
		assert.strictEqual(views[0].id, 'cervellaswarm.sidebar', 'Sidebar view ID should match');
	});

	test('Configuration should be available', () => {
		const config = vscode.workspace.getConfiguration('cervellaswarm');

		// Verify default config values
		const tier = config.get('tier');
		assert.ok(tier !== undefined, 'Tier configuration should exist');

		const agentsPath = config.get('agentsPath');
		assert.ok(agentsPath !== undefined, 'AgentsPath configuration should exist');

		const enabledAgents = config.get('enabledAgents');
		assert.ok(Array.isArray(enabledAgents), 'EnabledAgents should be an array');
	});
});
