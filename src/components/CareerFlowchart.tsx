import React from 'react';
import ReactFlow, { 
  Background, 
  Controls,
  Handle,
  Position,
  Node,
  Edge
} from 'reactflow';
import 'reactflow/dist/style.css';

interface CareerNodeData {
  label: string;
  description?: string;
  skills?: string[];
  companies?: string[];
  salary?: string;
  growth?: string;
  icon?: React.ReactNode;
}

const CustomNode = ({ data }: { data: CareerNodeData }) => {
  return (
    <div className="px-4 py-2 shadow-lg rounded-lg bg-white border border-gray-200 min-w-[200px]">
      <Handle type="target" position={Position.Top} className="w-2 h-2" />
      <div className="flex items-center gap-2">
        {data.icon}
        <div className="font-medium text-sm">{data.label}</div>
      </div>
      {data.description && (
        <div className="text-xs text-gray-500 mt-1">{data.description}</div>
      )}
      {data.growth && (
        <div className="flex items-center gap-1 mt-1">
          <span className="text-xs text-emerald-600 font-medium">{data.growth}</span>
          <span className="text-xs text-gray-500">YoY Growth</span>
        </div>
      )}
      {data.salary && (
        <div className="text-xs text-gray-600 mt-1">{data.salary}</div>
      )}
      {data.skills && data.skills.length > 0 && (
        <div className="flex flex-wrap gap-1 mt-2">
          {data.skills.map((skill) => (
            <span 
              key={skill}
              className="px-1.5 py-0.5 bg-blue-50 text-blue-600 rounded text-[10px]"
            >
              {skill}
            </span>
          ))}
        </div>
      )}
      <Handle type="source" position={Position.Bottom} className="w-2 h-2" />
    </div>
  );
};

const nodeTypes = {
  custom: CustomNode,
};

interface CareerFlowchartProps {
  nodes: Node<CareerNodeData>[];
  edges: Edge[];
}

export function CareerFlowchart({ nodes, edges }: CareerFlowchartProps) {
  return (
    <div className="w-full h-[400px]">
      <ReactFlow
        nodes={nodes}
        edges={edges}
        nodeTypes={nodeTypes}
        fitView
        minZoom={0.5}
        maxZoom={1.5}
        defaultViewport={{ x: 0, y: 0, zoom: 0.8 }}
      >
        <Background color="#f1f5f9" gap={16} />
        <Controls />
      </ReactFlow>
    </div>
  );
}