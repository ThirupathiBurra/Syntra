"use client";

import { useEffect, useState } from "react";
import { ReactFlow, Background, Controls, Node, Edge, BackgroundVariant } from "@xyflow/react";
import "@xyflow/react/dist/style.css";
import { eventStream } from "@/lib/api/sse";



export function DAGViewer() {
  const [nodes, setNodes] = useState<Node[]>([]);
  const [edges, setEdges] = useState<Edge[]>([]);

  useEffect(() => {
    // We connect if not connected, though demo/page.tsx already connects it.
    eventStream.connect();

    let nodeIndex = 0;
    let prevNodeId: string | null = null;

    const addNode = (nodeName: string, status: 'running' | 'completed') => {
      setNodes(prev => {
        // If node already exists, update its style
        const existingIdx = prev.findIndex(n => n.data.label === nodeName);
        if (existingIdx >= 0) {
          const newNodes = [...prev];
          const isComplete = status === 'completed';
          newNodes[existingIdx] = {
            ...newNodes[existingIdx],
            style: { 
              ...newNodes[existingIdx].style, 
              border: isComplete ? "1px solid #10b981" : "1px solid #f59e0b",
              background: isComplete ? "#064e3b" : "#451a03",
              color: isComplete ? "#34d399" : "#fcd34d"
            }
          };
          return newNodes;
        }

        // Add new node
        nodeIndex++;
        const newNodeId = nodeIndex.toString();
        const newNode: Node = {
          id: newNodeId,
          position: { x: 250, y: 50 + (nodeIndex - 1) * 100 },
          data: { label: nodeName },
          style: { 
            background: status === 'completed' ? "#064e3b" : "#451a03", 
            color: status === 'completed' ? "#34d399" : "#fcd34d", 
            border: status === 'completed' ? "1px solid #10b981" : "1px solid #f59e0b", 
            borderRadius: "8px", 
            width: 180 
          },
        };

        if (prevNodeId) {
          setEdges(prevEdges => [
            ...prevEdges,
            { 
              id: `e${prevNodeId}-${newNodeId}`, 
              source: prevNodeId!, 
              target: newNodeId, 
              animated: true, 
              style: { stroke: "#4f46e5", strokeWidth: 2 } 
            }
          ]);
        }
        
        prevNodeId = newNodeId;
        return [...prev, newNode];
      });
    };

    const unsubscribeStarted = eventStream.on("NodeStarted", (data: unknown) => {
      const payload = data as { node: string };
      if (payload?.node) addNode(payload.node, 'running');
    });

    const unsubscribeCompleted = eventStream.on("NodeCompleted", (data: unknown) => {
      const payload = data as { node: string };
      if (payload?.node) addNode(payload.node, 'completed');
    });

    return () => {
      unsubscribeStarted();
      unsubscribeCompleted();
    };
  }, []);

  return (
    <div className="h-[400px] w-full rounded-xl border border-zinc-800 bg-zinc-950/50 backdrop-blur-md overflow-hidden relative">
      <ReactFlow
        nodes={nodes}
        edges={edges}
        fitView
        className="bg-transparent transition-opacity duration-500"
        proOptions={{ hideAttribution: true }}
      >
        <Background variant={BackgroundVariant.Dots} gap={16} size={1} color="#27272a" />
        <Controls className="fill-zinc-400 stroke-zinc-400 !bg-zinc-900 !border-zinc-800" />
      </ReactFlow>
    </div>
  );
}
