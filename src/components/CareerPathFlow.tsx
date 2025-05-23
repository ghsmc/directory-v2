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
import { Brain, Code, Cloud, Database, LineChart, Network } from 'lucide-react';

interface CareerNodeData {
  label: string;
  description?: string;
  skills?: string[];
  companies?: string[];
  salary?: string;
  growth?: string;
  icon?: React.ReactNode;
}

const initialNodes: Node<CareerNodeData>[] = [
  {
    id: '1',
    type: 'custom',
    position: { x: 250, y: 0 },
    data: {
      label: 'ML Engineer',
      description: 'Focus on AI/ML systems',
      growth: '+45%',
      salary: '$180K - $250K',
      skills: ['Python', 'PyTorch', 'MLOps'],
      icon: <Brain size={16} className="text-purple-500" />
    }
  },
  {
    id: '2',
    type: 'custom',
    position: { x: 0, y: 150 },
    data: {
      label: 'Full Stack Dev',
      description: 'Web & mobile apps',
      growth: '+28%',
      salary: '$150K - $220K',
      skills: ['React', 'Node.js', 'TypeScript'],
      icon: <Code size={16} className="text-blue-500" />
    }
  },
  {
    id: '3',
    type: 'custom',
    position: { x: 250, y: 150 },
    data: {
      label: 'Cloud Architect',
      description: 'Design scalable systems',
      growth: '+32%',
      salary: '$160K - $230K',
      skills: ['AWS', 'K8s', 'Terraform'],
      icon: <Cloud size={16} className="text-sky-500" />
    }
  },
  {
    id: '4',
    type: 'custom',
    position: { x: 500, y: 150 },
    data: {
      label: 'Data Engineer',
      description: 'Build data pipelines',
      growth: '+35%',
      salary: '$155K - $225K',
      skills: ['SQL', 'Spark', 'Airflow'],
      icon: <Database size={16} className="text-emerald-500" />
    }
  },
  {
    id: '5',
    type: 'custom',
    position: { x: 125, y: 300 },
    data: {
      label: 'Data Scientist',
      description: 'Analytics & insights',
      growth: '+30%',
      salary: '$145K - $215K',
      skills: ['Python', 'R', 'Statistics'],
      icon: <LineChart size={16} className="text-amber-500" />
    }
  },
  {
    id: '6',
    type: 'custom',
    position: { x: 375, y: 300 },
    data: {
      label: 'DevOps Engineer',
      description: 'CI/CD & automation',
      growth: '+38%',
      salary: '$155K - $225K',
      skills: ['Docker', 'Jenkins', 'Git'],
      icon: <Network size={16} className="text-rose-500" />
    }
  }
];

const initialEdges: Edge[] = [
  { id: 'e1-2', source: '1', target: '2', animated: true },
  { id: 'e1-3', source: '1', target: '3', animated: true },
  { id: 'e1-4', source: '1', target: '4', animated: true },
  { id: 'e2-5', source: '2', target: '5', animated: true },
  { id: 'e3-6', source: '3', target: '6', animated: true },
  { id: 'e4-6', source: '4', target: '6', animated: true }
];

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

export function CareerPathFlow() {
  return (
    <div className="w-full h-[500px]">
      <ReactFlow
        nodes={initialNodes}
        edges={initialEdges}
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