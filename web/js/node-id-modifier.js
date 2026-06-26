import { app } from "/scripts/app.js";

const extension = {
	name: "NodeIDModifier",

	async setup(app) {
		this._app = app;
		this._setupNodeMenu(app);
		this._setupCanvasMenu(app);
		this._setupKeyboardShortcut(app);
	},

	_setupNodeMenu(app) {
		const self = this;
		const originalGetNodeMenuOptions = LiteGraph.LGraphCanvas.prototype.getNodeMenuOptions;

		LiteGraph.LGraphCanvas.prototype.getNodeMenuOptions = function(node, options) {
			options = originalGetNodeMenuOptions ? originalGetNodeMenuOptions.call(this, node, options) : options || [];

			options.push(null);

			options.push({
				content: "Change Node ID",
				callback: function() {
					self._showChangeIdDialog(app, node);
				}
			});

			options.push({
				content: "Normalize All Node IDs",
				callback: function() {
					self._normalizeAllNodeIds(app);
				}
			});

			return options;
		};
	},

	_setupCanvasMenu(app) {
		const self = this;
		const originalGetCanvasMenuOptions = LiteGraph.LGraphCanvas.prototype.getCanvasMenuOptions;

		LiteGraph.LGraphCanvas.prototype.getCanvasMenuOptions = function(options) {
			options = originalGetCanvasMenuOptions ? originalGetCanvasMenuOptions.call(this, options) : options || [];

			options.push(null);

			options.push({
				content: "Normalize All Node IDs",
				callback: function() {
					self._normalizeAllNodeIds(app);
				}
			});

			return options;
		};
	},

	_setupKeyboardShortcut(app) {
		const self = this;
		document.addEventListener("keydown", (e) => {
			if ((e.ctrlKey || e.metaKey) && e.key === "i") {
				if (app.graph.selected_nodes.size === 1) {
					const node = [...app.graph.selected_nodes][0];
					self._showChangeIdDialog(app, node);
				}
			}
		});
	},

	_showChangeIdDialog(app, node) {
		const dialog = document.createElement("div");
		dialog.style.cssText = `
			position: fixed;
			top: 50%;
			left: 50%;
			transform: translate(-50%, -50%);
			background: #2a2a2e;
			border: 1px solid #444;
			border-radius: 8px;
			padding: 20px;
			z-index: 10000;
			min-width: 300px;
			box-shadow: 0 10px 40px rgba(0,0,0,0.5);
		`;

		dialog.innerHTML = `
			<div style="color: #fff; font-size: 16px; font-weight: bold; margin-bottom: 15px;">
				Change Node ID
			</div>
			<div style="color: #aaa; margin-bottom: 10px;">
				Current ID: <span style="color: #4ade80;">${node.id}</span>
			</div>
			<div style="color: #aaa; margin-bottom: 5px;">
				New ID:
			</div>
			<input type="number" id="newNodeId" style="
				width: 100%;
				padding: 8px;
				background: #1e1e20;
				border: 1px solid #444;
				border-radius: 4px;
				color: #fff;
				font-size: 14px;
				box-sizing: border-box;
				margin-bottom: 15px;
			" min="0" value="${node.id}">
			<div style="display: flex; gap: 10px;">
				<button id="cancelBtn" style="
					flex: 1;
					padding: 8px;
					background: #444;
					border: none;
					border-radius: 4px;
					color: #fff;
					cursor: pointer;
					font-size: 14px;
				">Cancel</button>
				<button id="okBtn" style="
					flex: 1;
					padding: 8px;
					background: #4ade80;
					border: none;
					border-radius: 4px;
					color: #000;
					cursor: pointer;
					font-size: 14px;
					font-weight: bold;
				">OK</button>
			</div>
		`;

		const overlay = document.createElement("div");
		overlay.style.cssText = `
			position: fixed;
			top: 0;
			left: 0;
			width: 100%;
			height: 100%;
			background: rgba(0,0,0,0.7);
			z-index: 9999;
		`;

		document.body.appendChild(overlay);
		document.body.appendChild(dialog);

		const input = dialog.querySelector("#newNodeId");
		input.focus();
		input.select();

		const close = () => {
			document.body.removeChild(dialog);
			document.body.removeChild(overlay);
		};

		dialog.querySelector("#cancelBtn").addEventListener("click", close);

		const self = this;
		dialog.querySelector("#okBtn").addEventListener("click", () => {
			const newId = parseInt(input.value);
			if (!isNaN(newId) && newId >= 0) {
				self._changeNodeId(app, node.id, newId);
			}
			close();
		});

		input.addEventListener("keydown", (e) => {
			if (e.key === "Enter") {
				const newId = parseInt(input.value);
				if (!isNaN(newId) && newId >= 0) {
					self._changeNodeId(app, node.id, newId);
				}
				close();
			} else if (e.key === "Escape") {
				close();
			}
		});
	},

	_changeNodeId(app, oldId, newId) {
		if (newId === oldId) return;

		if (app.graph.getNodeById(newId)) {
			alert(`Node with ID ${newId} already exists!`);
			return;
		}

		const oldIdStr = String(oldId);

		const data = app.graph.serialize();

		for (const node of data.nodes) {
			if (node.id === oldId) {
				node.id = newId;
			}
		}

		if (data.links && Array.isArray(data.links)) {
			for (const link of data.links) {
				if (Array.isArray(link)) {
					if (link[1] === oldId || String(link[1]) === oldIdStr) {
						link[1] = newId;
					}
					if (link[3] === oldId || String(link[3]) === oldIdStr) {
						link[3] = newId;
					}
				} else if (typeof link === 'object' && link !== null) {
					if (link.origin_id === oldId || String(link.origin_id) === oldIdStr) {
						link.origin_id = newId;
					}
					if (link.target_id === oldId || String(link.target_id) === oldIdStr) {
						link.target_id = newId;
					}
				}
			}
		}

		if (data.groups && Array.isArray(data.groups)) {
			for (const group of data.groups) {
				if (group.nodes && Array.isArray(group.nodes)) {
					for (let i = 0; i < group.nodes.length; i++) {
						if (group.nodes[i] === oldId || String(group.nodes[i]) === oldIdStr) {
							group.nodes[i] = newId;
						}
					}
				}
			}
		}

		const canvas = app.canvas || app.graph.canvas;
		const selectedNodes = app.graph.selected_nodes ? new Set(app.graph.selected_nodes) : new Set();
		const activeNode = app.graph.getNodeById(oldId);
		if (activeNode) {
			selectedNodes.add(activeNode);
		}

		app.graph.clear();
		app.graph.configure(data);

		if (app.graph.last_node_id !== undefined && newId > app.graph.last_node_id) {
			app.graph.last_node_id = newId;
		}

		if (canvas) {
			try {
				canvas.draw(true);
			} catch (e) {
				console.warn("Canvas draw error:", e);
			}
		}

		const newNode = app.graph.getNodeById(newId);
		if (newNode && app.graph.selected_nodes) {
			app.graph.selected_nodes.add(newNode);
		}

		if (app.ui?.properties?.refresh) {
			try {
				app.ui.properties.refresh();
			} catch (e) {
				console.warn("Properties refresh error:", e);
			}
		}
	},

	_normalizeAllNodeIds(app) {
		const data = app.graph.serialize();

		const idMapping = {};
		let currentId = 1;

		const sortedNodes = [...data.nodes].sort((a, b) => Number(a.id) - Number(b.id));
		for (const node of sortedNodes) {
			idMapping[String(node.id)] = currentId;
			currentId++;
		}

		for (const node of data.nodes) {
			node.id = idMapping[String(node.id)];
		}

		if (data.links && Array.isArray(data.links)) {
			for (const link of data.links) {
				if (Array.isArray(link)) {
					const originIdStr = String(link[1]);
					const targetIdStr = String(link[3]);
					if (idMapping[originIdStr] !== undefined) {
						link[1] = idMapping[originIdStr];
					}
					if (idMapping[targetIdStr] !== undefined) {
						link[3] = idMapping[targetIdStr];
					}
				} else if (typeof link === 'object' && link !== null) {
					const originIdStr = String(link.origin_id);
					const targetIdStr = String(link.target_id);
					if (idMapping[originIdStr] !== undefined) {
						link.origin_id = idMapping[originIdStr];
					}
					if (idMapping[targetIdStr] !== undefined) {
						link.target_id = idMapping[targetIdStr];
					}
				}
			}
		}

		if (data.groups && Array.isArray(data.groups)) {
			for (const group of data.groups) {
				if (group.nodes && Array.isArray(group.nodes)) {
					for (let i = 0; i < group.nodes.length; i++) {
						const idStr = String(group.nodes[i]);
						if (idMapping[idStr] !== undefined) {
							group.nodes[i] = idMapping[idStr];
						}
					}
				}
			}
		}

		const canvas = app.canvas || app.graph.canvas;

		app.graph.clear();
		app.graph.configure(data);

		if (app.graph.last_node_id !== undefined) {
			app.graph.last_node_id = currentId - 1;
		}

		if (canvas) {
			try {
				canvas.draw(true);
			} catch (e) {
				console.warn("Canvas draw error:", e);
			}
		}

		if (app.ui?.properties?.refresh) {
			try {
				app.ui.properties.refresh();
			} catch (e) {
				console.warn("Properties refresh error:", e);
			}
		}
	},

	async beforeRegisterNodeDef(nodeType, nodeData, app) {
		if (nodeType.comfyClass === "NodeIDModifier" ||
			nodeType.comfyClass === "BatchNodeIDModifier" ||
			nodeType.comfyClass === "WorkflowIDNormalizer") {

			const onNodeCreated = nodeType.prototype.onNodeCreated;
			nodeType.prototype.onNodeCreated = function () {
				if (onNodeCreated) onNodeCreated.apply(this, arguments);

				this.addWidget("button", "Load Workflow", null, () => {
					const input = document.createElement("input");
					input.type = "file";
					input.accept = ".json";
					input.onchange = async (e) => {
						const file = e.target.files[0];
						if (file) {
							const text = await file.text();
							const workflowWidget = this.widgets.find(w => w.name === "workflow_json");
							if (workflowWidget) {
								workflowWidget.value = text;
								workflowWidget.callback && workflowWidget.callback(text);
							}
						}
					};
					input.click();
				});

				this.addWidget("button", "Save Workflow", null, () => {
					const resultWidget = this.widgets.find(w => w.name === "modified_workflow" || w.name === "normalized_workflow");
					if (resultWidget && resultWidget.value) {
						const blob = new Blob([resultWidget.value], { type: "application/json" });
						const url = URL.createObjectURL(blob);
						const a = document.createElement("a");
						a.href = url;
						a.download = "modified_workflow.json";
						a.click();
						URL.revokeObjectURL(url);
					}
				});

				this.addWidget("button", "Clear", null, () => {
					this.widgets.forEach(w => {
						if (w.name === "workflow_json") w.value = "{}";
						if (w.name === "old_node_id") w.value = "";
						if (w.name === "new_node_id") w.value = "";
						if (w.name === "id_mapping") w.value = "{}";
						if (w.name === "modified_workflow") w.value = "";
						if (w.name === "normalized_workflow") w.value = "";
						w.callback && w.callback(w.value);
					});
				});
			};
		}
	}
};

app.registerExtension(extension);
