// SPDX-License-Identifier: Apache-2.0
// Copyright 2026 CervellaSwarm Contributors

/**
 * VS Code extension client for the Lingua Universale language server.
 *
 * Launches `lu lsp` as a subprocess and connects via STDIO.
 * Requires: pip install cervellaswarm-lingua-universale[lsp]
 */

import { workspace, ExtensionContext, window } from "vscode";
import {
  LanguageClient,
  LanguageClientOptions,
  ServerOptions,
  TransportKind,
} from "vscode-languageclient/node";

let client: LanguageClient | undefined;

export function activate(context: ExtensionContext) {
  // Find the `lu` command -- respect user's PATH
  const luCommand = workspace
    .getConfiguration("lingua-universale")
    .get<string>("luPath", "lu");

  const serverOptions: ServerOptions = {
    command: luCommand,
    args: ["lsp"],
    transport: TransportKind.stdio,
  };

  const clientOptions: LanguageClientOptions = {
    documentSelector: [
      { scheme: "file", language: "lingua-universale" },
      { scheme: "untitled", language: "lingua-universale" },
    ],
    synchronize: {
      fileEvents: workspace.createFileSystemWatcher("**/*.lu"),
    },
  };

  client = new LanguageClient(
    "lingua-universale",
    "Lingua Universale Language Server",
    serverOptions,
    clientOptions
  );

  // Start the client (which also starts the server)
  client.start().catch((err) => {
    window.showWarningMessage(
      `Lingua Universale LSP failed to start: ${err.message}\n` +
        "Install with: pip install cervellaswarm-lingua-universale[lsp]"
    );
  });
}

export function deactivate(): Thenable<void> | undefined {
  if (!client) {
    return undefined;
  }
  return client.stop();
}
